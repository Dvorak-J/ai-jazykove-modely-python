# Řešení: trigramový model a porovnání s trénovacím textem
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

random.seed(1)


def rozdel_na_slova(text):
    return re.findall(r"\w+|[.,!?]", text.lower())


def natrenuj_trigramy(slova):
    model = defaultdict(Counter)
    for prvni, druhe, treti in zip(slova, slova[1:], slova[2:]):
        model[(prvni, druhe)][treti] += 1
    return model


def generuj_vetu(model, max_slov=25):
    zacatky = [klic for klic in model if klic[0] == "."]
    predchozi, slovo = random.choice(zacatky)
    veta = [slovo]
    for _ in range(max_slov):
        moznosti = model[(predchozi, slovo)]
        if not moznosti:
            break
        dalsi = random.choices(list(moznosti), weights=list(moznosti.values()))[0]
        if dalsi == ".":
            break
        veta.append(dalsi)
        predchozi, slovo = slovo, dalsi
    return " ".join(veta).replace(" ,", ",")


text = (Path(__file__).parent / "data" / "korpus.txt").read_text(encoding="utf-8")
slova = rozdel_na_slova(text)
model = natrenuj_trigramy(slova)

# věty trénovacího textu ve stejné podobě, jakou generuje model
puvodni = {v.strip().replace(" ,", ",") for v in " ".join(slova).split(".") if v.strip()}

pocet_kopii = 0
for _ in range(20):
    veta = generuj_vetu(model)
    kopie = veta in puvodni
    pocet_kopii += kopie
    print(("[kopie] " if kopie else "[nová]  ") + veta.capitalize() + ".")
print(f"\nDoslovných kopií: {pocet_kopii} z 20")
