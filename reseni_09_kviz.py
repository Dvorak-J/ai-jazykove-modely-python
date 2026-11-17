# Řešení: generátor kvízu se strukturovaným výstupem
from pydantic import BaseModel, Field

from strukturovane import ziskej_data


class Otazka(BaseModel):
    zneni: str
    moznosti: list[str] = Field(min_length=4, max_length=4)
    spravna: int = Field(ge=0, le=3, description="index správné možnosti (0 až 3)")
    vysvetleni: str


class Kviz(BaseModel):
    otazky: list[Otazka] = Field(min_length=1)


tema = input("Téma kvízu: ").strip() or "základy Pythonu"
kviz = ziskej_data(
    f"Vytvoř kvíz o 3 otázkách na téma: {tema}. Úroveň: střední škola. "
    "Každá otázka má právě čtyři možnosti, jedna je správná.",
    Kviz,
)

body = 0
for cislo, otazka in enumerate(kviz.otazky, 1):
    print(f"\n{cislo}. {otazka.zneni}")
    for pismeno, moznost in zip("ABCD", otazka.moznosti):
        print(f"   {pismeno}) {moznost}")
    odpoved = input("Tvoje odpověď (A–D): ").strip().upper()
    if odpoved in ("A", "B", "C", "D") and "ABCD".index(odpoved) == otazka.spravna:
        body += 1
        print("Správně!")
    else:
        print(f"Špatně, správně je {'ABCD'[otazka.spravna]}. {otazka.vysvetleni}")
print(f"\nVýsledek: {body} z {len(kviz.otazky)}")
