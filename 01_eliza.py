# Zjednodušená česká verze ELIZY (Joseph Weizenbaum, 1966)
import random
import re

# Každé pravidlo: (regulární výraz, seznam možných odpovědí).
# {0} v odpovědi se nahradí textem, který zachytila závorka ve vzoru.
PRAVIDLA = [
    (r"\b(ahoj|čau|dobrý den)\b",
     ["Dobrý den. Co vás trápí?", "Ahoj. O čem si chcete povídat?"]),
    (r"\bjsem (.+)",
     ["Proč si myslíte, že jste {0}?", "Jak dlouho už jste {0}?"]),
    (r"\bmám rád[a]? (.+)",
     ["Co se vám na tom líbí?", "Proč máte rád(a) {0}?"]),
    (r"\bnemůžu (.+)",
     ["Co vám brání {0}?", "Opravdu nemůžete {0}?"]),
    (r"\b(škol\w*|test\w*|písemk\w*)\b",
     ["Je pro vás škola teď důležité téma?", "Jak se ve škole cítíte?"]),
    (r"\bprotože\b",
     ["Je to opravdu ten hlavní důvod?", "Napadají vás i jiné důvody?"]),
    (r"\?$",
     ["Proč se ptáte?", "Co si o tom myslíte vy?"]),
]

NAHODNE = [
    "Pokračujte, prosím.",
    "Zajímavé. Řekněte mi o tom víc.",
    "Rozumím. A jak se u toho cítíte?",
]


def odpovez(veta):
    veta = veta.strip()
    for vzor, odpovedi in PRAVIDLA:
        shoda = re.search(vzor, veta, re.IGNORECASE)
        if shoda:
            sablona = random.choice(odpovedi)
            casti = [cast.rstrip(".!?") for cast in shoda.groups()]
            return sablona.format(*casti)
    return random.choice(NAHODNE)


print("ELIZA: Dobrý den, jsem ELIZA. Pro ukončení napište 'konec'.")
while True:
    vstup = input("Vy: ")
    if vstup.strip().lower() == "konec":
        print("ELIZA: Na shledanou.")
        break
    print("ELIZA:", odpovez(vstup))
