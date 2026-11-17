# Extrakce školních akcí z volného textu do tabulky (CSV)
import csv
from datetime import date
from pathlib import Path

from pydantic import BaseModel, Field

from strukturovane import ziskej_data


class Akce(BaseModel):
    nazev: str = Field(description="krátký název akce")
    datum: date = Field(description="datum konání")
    cas: str | None = Field(description="čas začátku ve formátu HH:MM, pokud je uveden")
    misto: str | None = Field(description="místo konání, pokud je uvedeno")
    tridy: list[str] = Field(description="kterých tříd se akce týká; prázdný seznam = všech")


class SeznamAkci(BaseModel):
    akce: list[Akce]


OZNAMENI = """
Milí studenti, ve středu 21. října proběhne od 8:00 v aule beseda s absolventy
oboru IT. Účast je povinná pro třídy 3.A a 4.A. Následující pátek nás čeká
Den otevřených dveří, začínáme v 9 hodin, dobrovolníci z řad studentů
se mohou hlásit u paní Novákové. Upozorňujeme také, že 2. listopadu je
ředitelské volno. Exkurze 2.B do Dolních Vítkovic se přesouvá na 12. 11.
"""

prompt = (
    f"Dnešní datum je {date.today():%d. %m. %Y}. Vypiš všechny akce "
    f"z tohoto oznámení:\n\n{OZNAMENI}"
)
vysledek = ziskej_data(prompt, SeznamAkci)

for akce in vysledek.akce:
    tridy = ", ".join(akce.tridy) if akce.tridy else "všichni"
    print(f"{akce.datum:%d. %m.}  {akce.cas or '':5}  {akce.nazev}  ({tridy})")

# uložení do CSV, které otevřete v Excelu (středník jako oddělovač)
soubor = Path(__file__).parent / "akce.csv"
with open(soubor, "w", newline="", encoding="utf-8-sig") as f:
    zapisovac = csv.DictWriter(f, fieldnames=list(Akce.model_fields), delimiter=";")
    zapisovac.writeheader()
    for akce in vysledek.akce:
        radek = akce.model_dump()
        radek["tridy"] = ", ".join(radek["tridy"])
        zapisovac.writerow(radek)
print(f"\nUloženo do {soubor.name}")
