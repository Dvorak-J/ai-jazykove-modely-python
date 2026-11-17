# Perceptron: jeden umělý neuron, který se učí logické funkce

def skok(z):
    """Aktivační funkce: neuron 'vystřelí' (1), když je vstup kladný."""
    return 1 if z > 0 else 0


def natrenuj(data, epochy=20, krok=0.1):
    w1, w2, b = 0.0, 0.0, 0.0
    for epocha in range(epochy):
        chyb = 0
        for (x1, x2), cil in data:
            vystup = skok(w1 * x1 + w2 * x2 + b)
            rozdil = cil - vystup          # 0, když neuron odpověděl správně
            if rozdil != 0:
                chyb += 1
                # pravidlo perceptronu: posuneme váhy směrem ke správné odpovědi
                w1 += krok * rozdil * x1
                w2 += krok * rozdil * x2
                b += krok * rozdil
        if chyb == 0:
            print(f"  naučeno po {epocha + 1} epochách")
            break
    else:
        print(f"  ani po {epochy} epochách se nepodařilo naučit všechny případy")
    return w1, w2, b


def otestuj(data, w1, w2, b):
    for (x1, x2), cil in data:
        vystup = skok(w1 * x1 + w2 * x2 + b)
        znacka = "ok" if vystup == cil else "CHYBA"
        print(f"  {x1} {x2} -> {vystup}  (správně {cil})  {znacka}")


FUNKCE = {
    "AND": [((0, 0), 0), ((0, 1), 0), ((1, 0), 0), ((1, 1), 1)],
    "OR":  [((0, 0), 0), ((0, 1), 1), ((1, 0), 1), ((1, 1), 1)],
    "XOR": [((0, 0), 0), ((0, 1), 1), ((1, 0), 1), ((1, 1), 0)],
}

for nazev, data in FUNKCE.items():
    print(nazev)
    w1, w2, b = natrenuj(data)
    print(f"  váhy: w1 = {w1:.1f}, w2 = {w2:.1f}, b = {b:.1f}")
    otestuj(data, w1, w2, b)
    print()
