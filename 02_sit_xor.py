# Malá neuronová síť (2 vstupy -> 3 skryté neurony -> 1 výstup),
# která se naučí funkci XOR algoritmem zpětného šíření chyby.
import math
import random

random.seed(42)


def sigmoida(z):
    return 1 / (1 + math.exp(-z))


SKRYTE = 3
# váhy vstup -> skrytá vrstva (pro každý skrytý neuron dvě váhy a bias)
w_skryta = [[random.uniform(-1, 1), random.uniform(-1, 1)] for _ in range(SKRYTE)]
b_skryta = [random.uniform(-1, 1) for _ in range(SKRYTE)]
# váhy skrytá vrstva -> výstup
w_vystup = [random.uniform(-1, 1) for _ in range(SKRYTE)]
b_vystup = random.uniform(-1, 1)

data = [((0, 0), 0), ((0, 1), 1), ((1, 0), 1), ((1, 1), 0)]
krok = 0.5


def dopredu(x):
    """Průchod sítí: vrací výstupy skryté vrstvy a výstup sítě."""
    h = [sigmoida(w_skryta[j][0] * x[0] + w_skryta[j][1] * x[1] + b_skryta[j])
         for j in range(SKRYTE)]
    y = sigmoida(sum(w_vystup[j] * h[j] for j in range(SKRYTE)) + b_vystup)
    return h, y


for epocha in range(10001):
    celkova_chyba = 0.0
    for x, cil in data:
        h, y = dopredu(x)
        celkova_chyba += (y - cil) ** 2

        # zpětné šíření: kolik "viny" za chybu nese který neuron
        delta_y = (y - cil) * y * (1 - y)
        delta_h = [delta_y * w_vystup[j] * h[j] * (1 - h[j]) for j in range(SKRYTE)]

        # úprava vah proti směru gradientu
        for j in range(SKRYTE):
            w_vystup[j] -= krok * delta_y * h[j]
            w_skryta[j][0] -= krok * delta_h[j] * x[0]
            w_skryta[j][1] -= krok * delta_h[j] * x[1]
            b_skryta[j] -= krok * delta_h[j]
        b_vystup -= krok * delta_y

    if epocha % 2000 == 0:
        print(f"epocha {epocha:5d}: chyba = {celkova_chyba:.4f}")

print()
for x, cil in data:
    _, y = dopredu(x)
    print(f"{x[0]} XOR {x[1]} = {y:.3f}  (zaokrouhleno {round(y)}, správně {cil})")
