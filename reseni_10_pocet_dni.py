# Řešení: nástroj pocet_dni_do pro ŠkolBota
from datetime import date

from nastroje import popis


def pocet_dni_do(datum):
    try:
        cil = date.fromisoformat(datum)
    except ValueError:
        return {"chyba": "Datum musí být ve formátu RRRR-MM-DD."}
    return {"datum": datum, "zbyva_dni": (cil - date.today()).days}


NASTROJ = popis(
    "pocet_dni_do",
    "Spočítá, kolik dní zbývá od dneška do zadaného data. Pro dny v minulosti "
    "vrátí záporné číslo.",
    {"datum": {"type": "string", "description": "datum ve formátu RRRR-MM-DD"}},
)

# Do ŠkolBota: NASTROJE.append(NASTROJ) a FUNKCE["pocet_dni_do"] = pocet_dni_do

if __name__ == "__main__":
    print(pocet_dni_do(f"{date.today().year}-12-24"))
    print(pocet_dni_do("24. 12."))
