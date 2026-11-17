# Řešení: nástroje suplovani, poznamka a precti_poznamky
from pathlib import Path

from nastroje import DEN, popis

SUPLOVANI = {
    "pondělí": ["3. hodina: programování odpadá, místo něj matematika (učebna 214)"],
    "středa": ["5. hodina: matematika se přesouvá do učebny 105"],
}
POZNAMKY = Path(__file__).parent / "poznamky.txt"


def suplovani(den):
    zmeny = SUPLOVANI.get(den.lower(), [])
    return {"den": den, "zmeny": zmeny or ["žádné změny"]}


def poznamka(text):
    with open(POZNAMKY, "a", encoding="utf-8") as f:
        f.write(text.strip() + "\n")
    return {"stav": "uloženo"}


def precti_poznamky():
    if not POZNAMKY.exists():
        return {"poznamky": []}
    return {"poznamky": POZNAMKY.read_text(encoding="utf-8").splitlines()}


NOVE_NASTROJE = [
    popis("suplovani", "Vrátí změny v rozvrhu (suplování) pro zadaný den.", {"den": DEN}),
    popis("poznamka", "Uloží krátkou poznámku uživatele, například co nesmí zapomenout.",
          {"text": {"type": "string", "description": "text poznámky"}}),
    popis("precti_poznamky", "Vrátí všechny uložené poznámky uživatele."),
]
NOVE_FUNKCE = {"suplovani": suplovani, "poznamka": poznamka,
               "precti_poznamky": precti_poznamky}

# Do ŠkolBota: NASTROJE.extend(NOVE_NASTROJE) a FUNKCE.update(NOVE_FUNKCE)

if __name__ == "__main__":
    print(suplovani("pondělí"))
    print(poznamka("Vrátit knihu do knihovny"))
    print(precti_poznamky())
