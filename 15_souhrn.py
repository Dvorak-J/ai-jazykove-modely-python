# Souhrn před návštěvou lékaře: deník pocitů + laboratorní výsledky.
# Program vypočítá fakta, model z nich napíše srozumitelný souhrn a otázky.
import csv
import statistics
from datetime import date
from pathlib import Path

from pydantic import BaseModel, Field

from llm import BASE_URL
from strukturovane import ziskej_data
from zdravi import je_lokalni, nacti_rozbor, poruseni, vyhodnot

DATA = Path(__file__).parent / "data"


def cz(cislo, des=None):
    text = f"{cislo:.{des}f}" if des is not None else f"{cislo:g}"
    return text.replace(".", ",")


PRAVIDLA = """Pomáháš člověku připravit se na návštěvu lékaře.
Pravidla, která nesmíš porušit:
- Nestanovuj diagnózy a nepiš, čím člověk trpí.
- Nedoporučuj léky ani doplňky stravy, neuváděj žádné dávky a množství.
- Neraď začít, přestat nebo změnit užívání čehokoli. To rozhoduje lékař.
- Pracuj jen s fakty, která dostaneš. Nic nedomýšlej.
- U hodnot mimo referenční meze napiš, že je vhodné je probrat s lékařem."""


class Souhrn(BaseModel):
    shrnuti: str = Field(description="3 až 5 vět, jen fakta z podkladů")
    otazky_pro_lekare: list[str] = Field(min_length=2, max_length=6)
    co_sledovat: list[str] = Field(description="co si zapisovat do deníku", max_length=4)


def fakta_z_deniku(soubor):
    with open(soubor, encoding="utf-8") as f:
        dny = list(csv.DictReader(f, delimiter=";"))
    energie = [int(d["energie"]) for d in dny]
    spanek = [float(d["spanek_hodin"].replace(",", ".")) for d in dny]
    nalada = [int(d["nalada"]) for d in dny]
    slabe = [d for d in dny if int(d["energie"]) <= 3]
    od, do = (date.fromisoformat(dny[i]["datum"]) for i in (0, -1))
    return [
        f"Deník: {len(dny)} dní ({od.day}. {od.month}. až {do.day}. {do.month}. {do.year}).",
        f"Průměrná energie {cz(statistics.mean(energie), 1)} z 10, nálada "
        f"{cz(statistics.mean(nalada), 1)} z 10, spánek {cz(statistics.mean(spanek), 1)} h.",
        f"Souvislost spánku a energie (korelace): {cz(statistics.correlation(spanek, energie), 2)}.",
        f"Dny s energií 3 a méně: {len(slabe)}; poznámky k nim: "
        + ", ".join(sorted({d['poznamka'] for d in slabe if d['poznamka']}) or ["žádné"]) + ".",
    ]


def fakta_z_krve():
    rozbory = [nacti_rozbor(z) for z in sorted(DATA.glob("krev_*.txt"))]
    fakta = []
    for v in rozbory[-1].vysledky:
        stav = vyhodnot(v)
        if stav != "v mezích":
            historie = [cz(w.hodnota) for r in rozbory for w in r.vysledky if w.nazev == v.nazev]
            fakta.append(f"{v.nazev}: {cz(v.hodnota)} {v.jednotka}, {stav} (meze "
                         f"{cz(v.dolni_mez)} až {cz(v.horni_mez)}; vývoj: {' → '.join(historie)}).")
    return fakta or ["Všechny hodnoty posledního odběru jsou v referenčních mezích."]


if not je_lokalni(BASE_URL):
    raise SystemExit("Zdravotní údaje zpracovávejte jen lokálním modelem (kapitola 12).")

fakta = fakta_z_deniku(DATA / "denik.csv") + fakta_z_krve()
prompt = "Podklady:\n- " + "\n- ".join(fakta)

for pokus in range(3):
    souhrn = ziskej_data(prompt, Souhrn, system=PRAVIDLA)
    text = "\n".join([souhrn.shrnuti, *souhrn.otazky_pro_lekare, *souhrn.co_sledovat])
    problemy = poruseni(text)
    if not problemy:
        break
    prompt += f"\n\nPředchozí verze porušila pravidla ({problemy}). Napiš ji znovu bez toho."
else:
    raise SystemExit("Model opakovaně porušil pravidla, souhrn nebyl vytvořen.")

dnes = date.today()
radky = [f"SOUHRN PRO NÁVŠTĚVU LÉKAŘE ({dnes.day}. {dnes.month}. {dnes.year})",
         "Vytvořeno programem z vlastních záznamů. Nejde o lékařské vyšetření ani radu.", ""]
if any("VÝRAZNĚ" in f for f in fakta):          # o tomhle nerozhoduje model
    radky += ["!!! Některá hodnota je výrazně mimo referenční meze. Nečekejte na",
              "!!! plánovanou kontrolu a domluvte se s lékařem co nejdříve.", ""]
radky += ["Fakta:", *[f"- {f}" for f in fakta], "", souhrn.shrnuti, "",
          "Otázky pro lékaře:",
          *[f"{i}. {o}" for i, o in enumerate(souhrn.otazky_pro_lekare, 1)], "",
          "Co sledovat do příští návštěvy:", *[f"- {c}" for c in souhrn.co_sledovat]]
vystup = Path(__file__).parent / "souhrn_pro_lekare.txt"
vystup.write_text("\n".join(radky), encoding="utf-8")
print("\n".join(radky))
