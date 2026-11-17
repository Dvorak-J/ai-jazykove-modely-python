# Řešení: vysvětlovač chybových hlášek
from llm import MODEL, klient

SYSTEM = """Jsi trpělivý učitel programování v Pythonu pro středoškoláky.
Uživatel ti pošle chybovou hlášku. Odpověz česky ve třech částech:
1. Co chyba znamená (jednou až dvěma větami, bez odborného žargonu).
2. Nejčastější příčiny (nejvýše tři odrážky).
3. Kde v kódu hledat (na který řádek se podívat a co zkontrolovat).
Nepiš opravený program, student má chybu najít sám."""

print("Vložte chybovou hlášku a ukončete ji prázdným řádkem:")
radky = []
while (radek := input()) != "":
    radky.append(radek)

odpoved = klient.chat.completions.create(
    model=MODEL,
    temperature=0.3,
    messages=[{"role": "system", "content": SYSTEM},
              {"role": "user", "content": "\n".join(radky)}],
)
print(odpoved.choices[0].message.content)
