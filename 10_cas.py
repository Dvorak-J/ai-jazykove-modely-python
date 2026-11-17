# První nástroj: model se může zeptat našeho programu na aktuální čas
import json
from datetime import datetime

from llm import MODEL, klient


DNY = ["pondělí", "úterý", "středa", "čtvrtek", "pátek", "sobota", "neděle"]


def aktualni_cas():
    """Skutečná funkce v Pythonu, kterou může model 'zavolat'."""
    ted = datetime.now()
    return f"{DNY[ted.weekday()]} {ted:%d. %m. %Y, %H:%M}"


# Popis nástroje pro model: název, k čemu slouží a jaké má parametry
NASTROJE = [{
    "type": "function",
    "function": {
        "name": "aktualni_cas",
        "description": "Vrátí aktuální datum, den v týdnu a čas.",
        "parameters": {"type": "object", "properties": {}},
    },
}]

zpravy = [{"role": "user", "content": "Kolik je teď hodin a jaký je dnes den?"}]

# 1) první dotaz: model dostane otázku i seznam nástrojů
odpoved = klient.chat.completions.create(model=MODEL, messages=zpravy, tools=NASTROJE)
zprava = odpoved.choices[0].message

if zprava.tool_calls:
    # 2) model nechce odpovídat, ale žádá o zavolání nástroje
    # žádost modelu o zavolání nástroje musí zůstat v historii
    zpravy.append({
        "role": "assistant",
        "content": zprava.content or "",
        "tool_calls": [volani.model_dump() for volani in zprava.tool_calls],
    })
    for volani in zprava.tool_calls:
        print(f"Model volá nástroj: {volani.function.name}({volani.function.arguments})")
        vysledek = aktualni_cas()
        print(f"Výsledek nástroje: {vysledek}")
        # 3) výsledek pošleme zpět jako zprávu s rolí "tool"
        zpravy.append({
            "role": "tool",
            "tool_call_id": volani.id,
            "content": json.dumps(vysledek, ensure_ascii=False),
        })
    # 4) druhý dotaz: model už zná výsledek a odpoví
    odpoved = klient.chat.completions.create(model=MODEL, messages=zpravy, tools=NASTROJE)
    zprava = odpoved.choices[0].message

print("Odpověď:", zprava.content)
