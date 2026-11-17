# Rozbor laboratorních výsledků: převzetí dat, kontrola a vývoj v čase
from pathlib import Path

from llm import BASE_URL
from zdravi import je_lokalni, nacti_rozbor, vyhodnot, zkontroluj_prevzeti

DATA = Path(__file__).parent / "data"


def cz(cislo):
    return f"{cislo:g}".replace(".", ",")


def datum(d):
    return f"{d.day}. {d.month}. {d.year}"


if not je_lokalni(BASE_URL):
    print(f"Pozor: zdravotní údaje by se odeslaly na server {BASE_URL}.")
    if input("Opravdu pokračovat? (ano/ne): ").strip().lower() != "ano":
        raise SystemExit("Ukončeno. Pro zdravotní data použijte lokální model.")

rozbory = []
for zprava in sorted(DATA.glob("krev_*.txt")):
    rozbor = nacti_rozbor(zprava)
    chyby = zkontroluj_prevzeti(rozbor, zprava.read_text(encoding="utf-8"))
    if chyby:
        print(f"{zprava.name}: tato čísla ve zprávě nejsou, zkontrolujte je: {chyby}")
    rozbory.append(rozbor)

posledni = rozbory[-1]
predchozi = {v.nazev: v for v in rozbory[-2].vysledky} if len(rozbory) > 1 else {}
print(f"\nOdběr {datum(posledni.datum_odberu)}"
      + (f" (srovnání s odběrem {datum(rozbory[-2].datum_odberu)})" if predchozi else ""))
for v in posledni.vysledky:
    meze = f"{cz(v.dolni_mez)}–{cz(v.horni_mez)}" if None not in (v.dolni_mez, v.horni_mez) else "?"
    vyvoj = ""
    if v.nazev in predchozi:
        rozdil = round(v.hodnota - predchozi[v.nazev].hodnota, 2)
        vyvoj = ("+" if rozdil > 0 else "") + cz(rozdil)
    print(f"  {v.nazev:22} {cz(v.hodnota):>6} {v.jednotka:7} {meze:11} {vyvoj:>6}  {vyhodnot(v)}")

print("\nHodnoty mimo meze a jejich význam vždy posoudí lékař.")
