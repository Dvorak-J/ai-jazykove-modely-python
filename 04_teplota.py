# Bigramový model s teplotou: jak náhodnost ovlivňuje generovaný text
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

random.seed(3)


def rozdel_na_slova(text):
    return re.findall(r"\w+|[.,!?]", text.lower())


def natrenuj(slova):
    model = defaultdict(Counter)
    for aktualni, dalsi in zip(slova, slova[1:]):
        model[aktualni][dalsi] += 1
    return model


def s_teplotou(pocty, teplota):
    """Převede počty na pravděpodobnosti upravené teplotou.
    Každý počet umocníme na 1/teplota a výsledky znovu normalizujeme."""
    upravene = {slovo: pocet ** (1 / teplota) for slovo, pocet in pocty.items()}
    celkem = sum(upravene.values())
    return {slovo: hodnota / celkem for slovo, hodnota in upravene.items()}


def generuj_vetu(model, teplota=1.0, max_slov=20):
    slovo = "."
    veta = []
    for _ in range(max_slov):
        p = s_teplotou(model[slovo], teplota)
        slovo = random.choices(list(p), weights=list(p.values()))[0]
        if slovo == ".":
            break
        veta.append(slovo)
    return (" ".join(veta).replace(" ,", ",")).capitalize() + "."


cesta = Path(__file__).parent / "data" / "korpus.txt"
model = natrenuj(rozdel_na_slova(cesta.read_text(encoding="utf-8")))

# Jak teplota mění pravděpodobnosti slov na začátku věty (po tečce)
for teplota in [0.2, 1.0, 5.0]:
    p = s_teplotou(model["."], teplota)
    nejlepsi = sorted(p.items(), key=lambda x: x[1], reverse=True)[:4]
    popis = ", ".join(f"{slovo} {pst:.2f}" for slovo, pst in nejlepsi)
    print(f"teplota {teplota}: {popis}")

for teplota in [0.2, 1.0, 5.0]:
    print(f"\nVěty při teplotě {teplota}:")
    for _ in range(3):
        print(" -", generuj_vetu(model, teplota))
