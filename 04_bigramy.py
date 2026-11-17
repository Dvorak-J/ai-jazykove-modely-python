# Bigramový jazykový model: předpovídá další slovo podle jednoho předchozího
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

random.seed(7)  # aby výsledky byly stejné jako v učebnici; zkuste řádek smazat


def rozdel_na_slova(text):
    """Jednoduchá 'tokenizace': slova a interpunkce jako samostatné tokeny."""
    return re.findall(r"\w+|[.,!?]", text.lower())


def natrenuj(slova):
    """Pro každé slovo spočítá, která slova po něm následují a kolikrát."""
    model = defaultdict(Counter)
    for aktualni, dalsi in zip(slova, slova[1:]):
        model[aktualni][dalsi] += 1
    return model


def pravdepodobnosti(model, slovo):
    pocty = model[slovo]
    celkem = sum(pocty.values())
    return {dalsi: pocet / celkem for dalsi, pocet in pocty.most_common()}


def generuj_vetu(model, max_slov=25):
    slovo = "."          # věta začíná po tečce
    veta = []
    for _ in range(max_slov):
        moznosti = model[slovo]
        slovo = random.choices(list(moznosti), weights=list(moznosti.values()))[0]
        if slovo == ".":
            break
        veta.append(slovo)
    text = " ".join(veta).replace(" ,", ",")
    return text.capitalize() + "."


# soubor hledáme ve složce data vedle tohoto programu
cesta = Path(__file__).parent / "data" / "korpus.txt"
slova = rozdel_na_slova(cesta.read_text(encoding="utf-8"))

model = natrenuj(slova)
print(f"Počet slov v textu: {len(slova)}, různých slov: {len(model)}")
print()

for slovo in ["kočka", "program", "do"]:
    print(f"Po slově '{slovo}' následuje:")
    for dalsi, p in list(pravdepodobnosti(model, slovo).items())[:5]:
        print(f"   {dalsi:12} {p:.2f}")
print()

print("Vygenerované věty:")
for _ in range(6):
    print(" -", generuj_vetu(model))
