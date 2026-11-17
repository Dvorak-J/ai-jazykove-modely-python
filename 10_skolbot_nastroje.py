# ŠkolBot verze 4: model sám rozhoduje, které nástroje použije (smyčka agenta)
import json
from pathlib import Path

from llm import MODEL, klient
from nastroje import FUNKCE, NASTROJE, VYZADUJI_POTVRZENI

SYSTEM = (Path(__file__).parent / "system_prompt.txt").read_text(encoding="utf-8")
SYSTEM += ("\nÚdaje o čase, rozvrhu a jídelníčku zjišťuj vždy pomocí nástrojů, "
           "nic si nedomýšlej. Pro výpočty používej kalkulačku.")
MAX_KROKU = 6


def proved_volani(volani):
    """Provede jedno volání nástroje a vrátí výsledek (slovník)."""
    nazev = volani.function.name
    if nazev not in FUNKCE:
        return {"chyba": f"Nástroj '{nazev}' neexistuje."}
    try:
        argumenty = json.loads(volani.function.arguments or "{}")
    except json.JSONDecodeError:
        return {"chyba": "Argumenty nejsou platný JSON."}
    if nazev in VYZADUJI_POTVRZENI:
        souhlas = input(f"   ŠkolBot chce provést {nazev}({argumenty}). Souhlasíš? (a/n) ")
        if souhlas.strip().lower() != "a":
            return {"chyba": "Uživatel akci nepovolil."}
    try:
        return FUNKCE[nazev](**argumenty)
    except TypeError as chyba:
        return {"chyba": f"Špatné argumenty: {chyba}"}


def odpovez(zpravy):
    """Smyčka agenta: model volá nástroje, dokud nemá dost informací k odpovědi."""
    for krok in range(MAX_KROKU):
        odpoved = klient.chat.completions.create(model=MODEL, messages=zpravy, tools=NASTROJE)
        zprava = odpoved.choices[0].message
        if not zprava.tool_calls:                    # model odpověděl textem: hotovo
            zpravy.append({"role": "assistant", "content": zprava.content})
            return zprava.content
        zpravy.append({
            "role": "assistant",
            "content": zprava.content or "",
            "tool_calls": [volani.model_dump() for volani in zprava.tool_calls],
        })
        for volani in zprava.tool_calls:
            vysledek = proved_volani(volani)
            print(f"   [nástroj] {volani.function.name}({volani.function.arguments}) -> {vysledek}")
            zpravy.append({
                "role": "tool",
                "tool_call_id": volani.id,
                "content": json.dumps(vysledek, ensure_ascii=False),
            })
    return "Promiň, s touhle otázkou si neporadím (bylo potřeba příliš mnoho kroků)."


zpravy = [{"role": "system", "content": SYSTEM}]
print("ŠkolBot v4 s nástroji (pro ukončení napiš 'konec')")
while True:
    vstup = input("\nTy: ").strip()
    if vstup.lower() == "konec":
        break
    if not vstup:
        continue
    zpravy.append({"role": "user", "content": vstup})
    print("ŠkolBot:", odpovez(zpravy))
