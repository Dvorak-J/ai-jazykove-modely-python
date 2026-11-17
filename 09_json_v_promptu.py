# Naivní přístup: požádáme o JSON jen v promptu
import json

from llm import MODEL, klient

PROMPT = """Z následujícího inzerátu vytáhni údaje a vrať je jako JSON
s klíči "predmet" (text), "cena" (číslo v Kč) a "mesto" (text).

Inzerát: Prodám grafickou kalkulačku Casio, jen rok používaná, v krabici.
Cena 1 200 Kč, osobní předání v Brně u hlavního nádraží."""

odpoved = klient.chat.completions.create(
    model=MODEL,
    messages=[{"role": "user", "content": PROMPT}],
    temperature=0,
)
text = odpoved.choices[0].message.content
print("Odpověď modelu:")
print(text)

try:
    data = json.loads(text)
    print("\nPodařilo se převést na slovník:", data)
    print("Cena s DPH by byla", data["cena"] * 1.21)
except (json.JSONDecodeError, KeyError, TypeError) as chyba:
    print("\nOdpověď nejde zpracovat:", chyba)
