# Stejná otázka, různé systémové prompty
from llm import MODEL, klient

OTAZKA = "Co je to cyklus v programování?"

SYSTEMOVE_PROMPTY = [
    "Odpovídej stručně, nejvýše jednou větou.",
    "Jsi trpělivý učitel. Vysvětluj pro dvanáctileté dítě a použij přirovnání z běžného života.",
    "Odpovídej jako pirát z 18. století, ale věcně správně. Nejvýše tři věty.",
]

for system in SYSTEMOVE_PROMPTY:
    odpoved = klient.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": OTAZKA},
        ],
    )
    print(f"### {system}")
    print(odpoved.choices[0].message.content)
    print()
