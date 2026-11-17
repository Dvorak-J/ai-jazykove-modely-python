# Řešení: agent, který píše a spouští programy jen v pískovišti
import importlib
import json
import shutil

from llm import MODEL, klient

piskoviste = importlib.import_module("16_piskoviste")      # jméno začíná číslicí
kontejner = importlib.import_module("16_kontejner")

FUNKCE = dict(piskoviste.FUNKCE)
if shutil.which("docker"):                         # kód od agenta raději v kontejneru
    FUNKCE["spust_python"] = kontejner.spust_v_kontejneru
VYZADUJI_POTVRZENI = {"spust_python"}
MAX_KROKU = 8
SYSTEM = ("Jsi programátorský pomocník. Pracuješ jen se soubory v pracovní složce "
          "a máš k dispozici nástroje. Po napsání programu ho vždy spusť a ověř výsledek.")


def proved_volani(volani):
    nazev = volani.function.name
    if nazev not in FUNKCE:
        return {"chyba": f"Nástroj '{nazev}' neexistuje."}
    try:
        argumenty = json.loads(volani.function.arguments or "{}")
    except json.JSONDecodeError:
        return {"chyba": "Argumenty nejsou platný JSON."}
    if nazev in VYZADUJI_POTVRZENI:
        if input(f"   Agent chce provést {nazev}({argumenty}). Povolit? (a/n) ").lower() != "a":
            return {"chyba": "Uživatel akci nepovolil."}
    try:
        return FUNKCE[nazev](**argumenty)
    except TypeError as chyba:
        return {"chyba": f"Špatné argumenty: {chyba}"}


ukol = input("Úkol pro agenta: ").strip()
zpravy = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": ukol}]
for krok in range(MAX_KROKU):
    zprava = klient.chat.completions.create(
        model=MODEL, messages=zpravy, tools=piskoviste.NASTROJE).choices[0].message
    if not zprava.tool_calls:
        print("Agent:", zprava.content)
        break
    zpravy.append({"role": "assistant", "content": zprava.content or "",
                   "tool_calls": [v.model_dump() for v in zprava.tool_calls]})
    for volani in zprava.tool_calls:
        vysledek = proved_volani(volani)
        print(f"   [{volani.function.name}] -> {str(vysledek)[:120]}")
        zpravy.append({"role": "tool", "tool_call_id": volani.id,
                       "content": json.dumps(vysledek, ensure_ascii=False)})
else:
    print("Agent nedokončil úkol v povoleném počtu kroků.")
