"""Jednoduchý systém RAG: rozdělení dokumentu, embeddingy, vyhledávání."""
import json
import math
import re
from pathlib import Path

from llm import EMBED_MODEL, klient

MAX_ZNAKU = 700  # přibližná maximální délka jednoho úseku


def rozdel_na_useky(text):
    """Rozdělí dokument ve formátu Markdown na úseky podle nadpisů '## '.
    Příliš dlouhé oddíly rozdělí ještě po odstavcích."""
    useky = []
    for oddil in re.split(r"\n(?=## )", text):
        radky = oddil.strip().splitlines()
        if not radky or not radky[0].startswith("## "):
            continue                          # úvod před prvním nadpisem přeskočíme
        nadpis = radky[0][3:].strip()
        obsah = "\n".join(radky[1:]).strip()
        kus = ""
        for odstavec in obsah.split("\n\n"):
            if kus and len(kus) + len(odstavec) > MAX_ZNAKU:
                useky.append({"nadpis": nadpis, "text": kus.strip()})
                kus = ""
            kus += odstavec + "\n\n"
        if kus.strip():
            useky.append({"nadpis": nadpis, "text": kus.strip()})
    return useky


def embeddingy(texty):
    """Vrátí seznam embeddingů (vektorů) pro seznam textů."""
    odpoved = klient.embeddings.create(model=EMBED_MODEL, input=texty)
    return [polozka.embedding for polozka in odpoved.data]


def kosinova_podobnost(a, b):
    soucin = sum(x * y for x, y in zip(a, b))
    return soucin / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))


def vytvor_index(cesta_dokumentu, cesta_indexu):
    useky = rozdel_na_useky(Path(cesta_dokumentu).read_text(encoding="utf-8"))
    vektory = embeddingy([f"{u['nadpis']}\n{u['text']}" for u in useky])
    for usek, vektor in zip(useky, vektory):
        usek["vektor"] = vektor
    Path(cesta_indexu).write_text(json.dumps(useky, ensure_ascii=False), encoding="utf-8")
    return useky


def nacti_index(cesta_indexu):
    return json.loads(Path(cesta_indexu).read_text(encoding="utf-8"))


def vyhledej(dotaz, index, pocet=3):
    """Vrátí `pocet` úseků, které jsou významem nejbližší dotazu."""
    vektor_dotazu = embeddingy([dotaz])[0]
    hodnoceni = [(kosinova_podobnost(vektor_dotazu, u["vektor"]), u) for u in index]
    hodnoceni.sort(key=lambda dvojice: dvojice[0], reverse=True)
    return hodnoceni[:pocet]
