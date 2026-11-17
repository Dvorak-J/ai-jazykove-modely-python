"""Testovací server napodobující OpenAI-kompatibilní API (a část Ollama API).

Slouží jen k ověření, že ukázkové programy z textu jsou syntakticky i logicky
v pořádku (správné volání API, zpracování odpovědí, nástrojů, JSON, streamingu).
Odpovědi nejsou "inteligentní", jsou deterministické.
"""
import hashlib
import json
import math
import re
import sys
import threading
import time
import unicodedata
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 11434
POCITADLO = {"pozadavky": 0, "chyby_429": 0}
ZAMEK = threading.Lock()
LOG = []

DIM = 256


def bez_diakritiky(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def embedding(text):
    v = [0.0] * DIM
    slova = re.findall(r"\w+", bez_diakritiky(text.lower()))
    for s in slova:
        if len(s) < 3:
            continue
        kmen = s[:5]
        h = int(hashlib.md5(kmen.encode()).hexdigest(), 16)
        v[h % DIM] += 1.0
        v[(h // DIM) % DIM] += 0.5
    n = math.sqrt(sum(x * x for x in v)) or 1.0
    return [x / n for x in v]


def priklad_ze_schematu(schema, defs=None, nazev=""):
    defs = defs or schema.get("$defs", {}) or schema.get("definitions", {})
    if "$ref" in schema:
        jmeno = schema["$ref"].split("/")[-1]
        return priklad_ze_schematu(defs[jmeno], defs, jmeno)
    if "anyOf" in schema:
        for moznost in schema["anyOf"]:
            if moznost.get("type") != "null":
                return priklad_ze_schematu(moznost, defs, nazev)
        return None
    if "enum" in schema:
        return schema["enum"][0]
    typ = schema.get("type")
    if isinstance(typ, list):
        typ = [t for t in typ if t != "null"][0]
    if typ == "object":
        return {k: priklad_ze_schematu(v, defs, k) for k, v in schema.get("properties", {}).items()}
    if typ == "array":
        polozka = schema.get("items", {"type": "string"})
        pocet = max(1, schema.get("minItems", 1))
        return [priklad_ze_schematu(polozka, defs, nazev) for _ in range(pocet)]
    if typ == "integer":
        mn = schema.get("minimum", 1)
        mx = schema.get("maximum", max(mn, 3))
        return min(max(3, mn), mx)
    if typ == "number":
        return 4.5
    if typ == "boolean":
        return True
    if schema.get("format") == "date" or "date" in nazev:
        return "2026-10-20"
    if schema.get("format") == "date-time":
        return "2026-10-20T08:00:00"
    return f"ukázka {nazev}".strip()


def text_posledni(messages, role="user"):
    for m in reversed(messages):
        if m.get("role") == role:
            c = m.get("content")
            if isinstance(c, list):
                return " ".join(p.get("text", "") for p in c if isinstance(p, dict))
            return c or ""
    return ""


def vyber_nastroj(tools, dotaz):
    d = bez_diakritiky(dotaz.lower())
    nejlepsi, skore_max = None, -1
    for t in tools:
        f = t["function"]
        slova = re.findall(r"\w+", bez_diakritiky((f["name"] + " " + f.get("description", "")).lower()))
        skore = sum(1 for s in set(slova) if len(s) > 3 and s[:5] in d)
        if skore > skore_max:
            nejlepsi, skore_max = f, skore
    return nejlepsi if skore_max > 0 else tools[0]["function"]


def argumenty(funkce, dotaz):
    params = funkce.get("parameters", {})
    vysledek = {}
    for nazev, sch in params.get("properties", {}).items():
        if nazev in ("vyraz", "priklad", "expression"):
            m = re.search(r"[\d\.\s\+\-\*/\(\)]{3,}", dotaz)
            vysledek[nazev] = m.group(0).strip() if m else "2 + 2"
        elif "enum" in sch:
            d = bez_diakritiky(dotaz.lower())
            vysledek[nazev] = next((e for e in sch["enum"] if bez_diakritiky(str(e).lower())[:4] in d), sch["enum"][0])
        elif nazev in ("den",):
            d = bez_diakritiky(dotaz.lower())
            dny = ["pondeli", "utery", "streda", "ctvrtek", "patek"]
            vysledek[nazev] = next((x for x in dny if x[:4] in d), "pondeli")
        else:
            vysledek[nazev] = priklad_ze_schematu(sch, nazev=nazev)
    return vysledek


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *a):
        pass

    def _json(self, kod, data):
        b = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(kod)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        if self.path.rstrip("/").endswith("/v1/models"):
            self._json(200, {"object": "list", "data": [
                {"id": "gemma3:4b", "object": "model", "owned_by": "test"},
                {"id": "embeddinggemma:latest", "object": "model", "owned_by": "test"}]})
        elif self.path.startswith("/api/tags"):
            self._json(200, {"models": [{"name": "gemma3:4b", "size": 3300000000}]})
        else:
            self._json(404, {"error": "not found"})

    def do_POST(self):
        delka = int(self.headers.get("Content-Length", 0))
        telo = json.loads(self.rfile.read(delka) or b"{}")
        with ZAMEK:
            POCITADLO["pozadavky"] += 1
            LOG.append({"path": self.path, "body": telo})
        auth = self.headers.get("Authorization", "")
        if "spatny-klic" in auth:
            return self._json(401, {"error": {"message": "Incorrect API key provided", "type": "invalid_request_error", "code": "invalid_api_key"}})
        if self.path.endswith("/chat/completions"):
            return self.chat(telo)
        if self.path.endswith("/embeddings"):
            vstup = telo.get("input")
            if isinstance(vstup, str):
                vstup = [vstup]
            data = [{"object": "embedding", "index": i, "embedding": embedding(t)} for i, t in enumerate(vstup)]
            return self._json(200, {"object": "list", "data": data, "model": telo.get("model"),
                                    "usage": {"prompt_tokens": sum(len(t.split()) for t in vstup), "total_tokens": sum(len(t.split()) for t in vstup)}})
        if self.path.startswith("/api/chat"):
            dotaz = text_posledni(telo.get("messages", []))
            return self._json(200, {"model": telo.get("model"), "created_at": "2026-10-12T10:00:00Z",
                                    "message": {"role": "assistant", "content": f"[test] Odpověď na: {dotaz[:60]}"},
                                    "done": True, "done_reason": "stop", "prompt_eval_count": 12, "eval_count": 8})
        if self.path.startswith("/api/embed"):
            vstup = telo.get("input")
            if isinstance(vstup, str):
                vstup = [vstup]
            return self._json(200, {"model": telo.get("model"), "embeddings": [embedding(t) for t in vstup]})
        self._json(404, {"error": "not found"})

    def chat(self, telo):
        model = telo.get("model", "")
        if model == "neexistujici-model":
            return self._json(404, {"error": {"message": f"model '{model}' not found", "type": "not_found_error", "code": "model_not_found"}})
        zpravy = telo.get("messages", [])
        dotaz = text_posledni(zpravy)
        if "VYVOLEJ_429" in dotaz:
            with ZAMEK:
                POCITADLO["chyby_429"] += 1
                n = POCITADLO["chyby_429"]
            if n % 3 != 0:
                return self._json(429, {"error": {"message": "Rate limit exceeded", "type": "rate_limit_error", "code": "rate_limit_exceeded"}})
        tools = telo.get("tools")
        posledni_role = zpravy[-1]["role"] if zpravy else "user"
        tool_calls = None
        obsah = None
        if tools and posledni_role == "user":
            f = vyber_nastroj(tools, dotaz)
            if f:
                tool_calls = [{"id": f"call_{POCITADLO['pozadavky']}", "type": "function",
                               "function": {"name": f["name"], "arguments": json.dumps(argumenty(f, dotaz), ensure_ascii=False)}}]
        if tool_calls is None:
            rf = telo.get("response_format") or {}
            if rf.get("type") == "json_schema":
                schema = rf["json_schema"]["schema"]
                obsah = json.dumps(priklad_ze_schematu(schema), ensure_ascii=False)
            elif rf.get("type") == "json_object":
                obsah = json.dumps({"odpoved": "test", "kategorie": "jine", "sentiment": "pozitivni", "skore": 4}, ensure_ascii=False)
            elif posledni_role == "tool":
                vysledky = [m.get("content") for m in zpravy if m.get("role") == "tool"]
                obsah = "[test] Podle nástroje: " + "; ".join(str(v) for v in vysledky[-3:])
            elif "OpenSCAD" in text_posledni(zpravy, "system"):
                if "OpenSCAD hlásí" in dotaz:
                    obsah = "```openscad\ncube([20, 20, 10]);\n```\nOpravil jsem chybu."
                else:   # první pokus obsahuje chybu, aby se otestovala oprava
                    obsah = "```openscad\ncube([20, 20, 10]\n```\nVytvořil jsem kvádr."
            else:
                system = text_posledni(zpravy, "system")
                obsah = f"[test] Odpověď na: {dotaz[:80]}"
                if "Kontext:" in dotaz or "KONTEXT" in dotaz or "Kontext" in system:
                    obsah += " (použit kontext)"
            mt = telo.get("max_tokens") or telo.get("max_completion_tokens")
            if mt:
                obsah = " ".join(obsah.split()[:mt])
        prompt_tokens = sum(len(str(m.get("content", "")).split()) for m in zpravy) + 5
        completion_tokens = len((obsah or "").split()) + (10 if tool_calls else 0)
        zprava = {"role": "assistant", "content": obsah}
        if tool_calls:
            zprava["tool_calls"] = tool_calls
        finish = "tool_calls" if tool_calls else "stop"
        if telo.get("stream"):
            return self.stream(model, obsah or "", finish, prompt_tokens, completion_tokens,
                               (telo.get("stream_options") or {}).get("include_usage"))
        self._json(200, {
            "id": "chatcmpl-test", "object": "chat.completion", "created": int(time.time()), "model": model,
            "choices": [{"index": 0, "message": zprava, "finish_reason": finish}],
            "usage": {"prompt_tokens": prompt_tokens, "completion_tokens": completion_tokens,
                      "total_tokens": prompt_tokens + completion_tokens}})

    def stream(self, model, text, finish, pt, ct, usage):
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "close")
        self.end_headers()

        def posli(obj):
            self.wfile.write(f"data: {json.dumps(obj, ensure_ascii=False)}\n\n".encode())
            self.wfile.flush()

        zaklad = {"id": "chatcmpl-test", "object": "chat.completion.chunk", "created": int(time.time()), "model": model}
        posli({**zaklad, "choices": [{"index": 0, "delta": {"role": "assistant", "content": ""}, "finish_reason": None}]})
        for i, slovo in enumerate(text.split(" ")):
            posli({**zaklad, "choices": [{"index": 0, "delta": {"content": ("" if i == 0 else " ") + slovo}, "finish_reason": None}]})
        posli({**zaklad, "choices": [{"index": 0, "delta": {}, "finish_reason": finish}]})
        if usage:
            posli({**zaklad, "choices": [], "usage": {"prompt_tokens": pt, "completion_tokens": ct, "total_tokens": pt + ct}})
        self.wfile.write(b"data: [DONE]\n\n")
        self.wfile.flush()
        self.close_connection = True


if __name__ == "__main__":
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"Testovací server běží na portu {PORT}", flush=True)
    srv.serve_forever()
