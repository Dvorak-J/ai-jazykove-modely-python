# Miniaturní tokenizér metodou BPE (Byte Pair Encoding)
from collections import Counter

TEXT = """
Programování je tvůrčí činnost. Programátor píše program a program dělá,
co programátor naprogramoval. Dobrý programátor programuje s rozmyslem.
Počítač provádí program rychle. Počítače dnes najdeme všude a programy
v počítačích řídí auta, telefony i pračky. Učíme se programovat,
protože programování nás baví. Kdo umí programovat, umí přemýšlet.
Programovací jazyk Python je jednoduchý. V jazyce Python se dobře
programuje a programy v Pythonu jsou čitelné.
"""


def priprav_slova(text):
    """Rozdělí text na slova, každé slovo rozloží na znaky.
    Mezera před slovem se označí znakem '▁' (tak to dělá i řada skutečných tokenizérů)."""
    slova = text.lower().replace(".", " ").replace(",", " ").split()
    return Counter(tuple("▁" + slovo) for slovo in slova)


def spocitej_dvojice(slova):
    dvojice = Counter()
    for slovo, pocet in slova.items():
        for i in range(len(slovo) - 1):
            dvojice[(slovo[i], slovo[i + 1])] += pocet
    return dvojice


def spoj(slova, dvojice):
    a, b = dvojice
    nova = Counter()
    for slovo, pocet in slova.items():
        vysledek = []
        i = 0
        while i < len(slovo):
            if i < len(slovo) - 1 and slovo[i] == a and slovo[i + 1] == b:
                vysledek.append(a + b)   # dvojici nahradíme jedním tokenem
                i += 2
            else:
                vysledek.append(slovo[i])
                i += 1
        nova[tuple(vysledek)] += pocet
    return nova


def natrenuj(text, pocet_spojeni):
    slova = priprav_slova(text)
    pravidla = []
    for _ in range(pocet_spojeni):
        dvojice = spocitej_dvojice(slova)
        if not dvojice:
            break
        nejcastejsi = dvojice.most_common(1)[0][0]
        pravidla.append(nejcastejsi)
        slova = spoj(slova, nejcastejsi)
    return pravidla


def tokenizuj(slovo, pravidla):
    casti = list("▁" + slovo.lower())
    for a, b in pravidla:              # pravidla používáme ve stejném pořadí,
        i = 0                          # v jakém vznikla
        while i < len(casti) - 1:
            if casti[i] == a and casti[i + 1] == b:
                casti[i:i + 2] = [a + b]
            else:
                i += 1
    return casti


pravidla = natrenuj(TEXT, 40)
print("Prvních 12 naučených spojení:")
for a, b in pravidla[:12]:
    print(f"  {a!r} + {b!r} -> {a + b!r}")

print()
for slovo in ["programování", "programátor", "přeprogramovat", "počítačový", "pes"]:
    tokeny = tokenizuj(slovo, pravidla)
    print(f"{slovo:15} -> {tokeny}  (počet: {len(tokeny)})")
