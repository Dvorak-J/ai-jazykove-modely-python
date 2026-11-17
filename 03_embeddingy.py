# Embeddingy: slova jako vektory čísel (ručně vymyšlený příklad)
import math

# Každé slovo popíšeme pěti čísly (0 až 1). Význam jednotlivých složek:
#             zvíře  domácí  jídlo  technika  velikost
VEKTORY = {
    "pes":      [0.9,  0.9,   0.0,   0.0,      0.4],
    "kočka":    [0.9,  1.0,   0.0,   0.0,      0.25],
    "křeček":   [0.9,  0.8,   0.0,   0.0,      0.1],
    "tygr":     [1.0,  0.0,   0.0,   0.0,      0.7],
    "slon":     [1.0,  0.0,   0.0,   0.0,      1.0],
    "jablko":   [0.0,  0.3,   1.0,   0.0,      0.1],
    "hruška":   [0.0,  0.3,   1.0,   0.0,      0.1],
    "pizza":    [0.0,  0.4,   1.0,   0.1,      0.3],
    "počítač":  [0.0,  0.5,   0.0,   1.0,      0.3],
    "telefon":  [0.0,  0.6,   0.0,   1.0,      0.1],
}


def kosinova_podobnost(a, b):
    """1 = stejný směr (velmi podobné), 0 = kolmé vektory (nesouvisející)."""
    skalarni_soucin = sum(x * y for x, y in zip(a, b))
    delka_a = math.sqrt(sum(x * x for x in a))
    delka_b = math.sqrt(sum(y * y for y in b))
    return skalarni_soucin / (delka_a * delka_b)


def nejpodobnejsi(slovo, pocet=3):
    vysledky = []
    for jine, vektor in VEKTORY.items():
        if jine != slovo:
            podobnost = kosinova_podobnost(VEKTORY[slovo], vektor)
            vysledky.append((podobnost, jine))
    vysledky.sort(reverse=True)
    return vysledky[:pocet]


for slovo in ["pes", "slon", "jablko", "telefon"]:
    sousede = ", ".join(f"{s} ({p:.2f})" for p, s in nejpodobnejsi(slovo))
    print(f"{slovo:8} je nejpodobnější: {sousede}")

print()
print(f"pes – kočka:   {kosinova_podobnost(VEKTORY['pes'], VEKTORY['kočka']):.2f}")
print(f"pes – telefon: {kosinova_podobnost(VEKTORY['pes'], VEKTORY['telefon']):.2f}")

# Analogie: s vektory lze počítat. Co vyjde z výpočtu král - muž + žena?
#               královský  mužský  ženský
ROD = {
    "král":      [1.0,      1.0,    0.0],
    "královna":  [1.0,      0.0,    1.0],
    "princ":     [0.7,      1.0,    0.0],
    "princezna": [0.7,      0.0,    1.0],
    "muž":       [0.0,      1.0,    0.0],
    "žena":      [0.0,      0.0,    1.0],
}
vysledek = [k - m + z for k, m, z in zip(ROD["král"], ROD["muž"], ROD["žena"])]
print()
print("král - muž + žena =", vysledek)
for slovo, vektor in ROD.items():
    print(f"  podobnost se slovem {slovo:10} {kosinova_podobnost(vysledek, vektor):.2f}")
