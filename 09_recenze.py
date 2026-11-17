# Analýza recenzí školní jídelny: strukturovaný výstup s Pydanticem
from collections import Counter
from typing import Literal

from pydantic import BaseModel, Field

from strukturovane import ziskej_data


class Hodnoceni(BaseModel):
    sentiment: Literal["pozitivni", "neutralni", "negativni"]
    skore: int = Field(ge=1, le=5, description="1 = velmi špatné, 5 = výborné")
    temata: list[str] = Field(description="o čem recenze mluví, např. chuť, porce, fronta")
    shrnuti: str = Field(description="shrnutí recenze jednou krátkou větou")


RECENZE = [
    "Svíčková byla výborná, jen bylo málo knedlíků. Paní kuchařky jsou milé.",
    "Fronta na oběd byla zase dvacet minut a polévka studená. Hrůza.",
    "Normální oběd, nic extra. Kompot dobrý.",
    "Konečně vegetariánské jídlo, které chutná! Rizoto bylo skvělé.",
    "Řízek jako podrážka, brambory rozvařené. Za tu cenu bych čekal víc.",
]

SYSTEM = "Analyzuješ recenze školní jídelny, které napsali studenti."

vysledky = []
for text in RECENZE:
    hodnoceni = ziskej_data(f"Recenze: {text}", Hodnoceni, system=SYSTEM)
    vysledky.append(hodnoceni)
    print(f"{hodnoceni.skore}/5  {hodnoceni.sentiment:10}  {hodnoceni.shrnuti}")

print()
prumer = sum(h.skore for h in vysledky) / len(vysledky)
print(f"Průměrné skóre: {prumer:.1f}")
print("Sentiment:", dict(Counter(h.sentiment for h in vysledky)))
temata = Counter(tema.lower() for h in vysledky for tema in h.temata)
print("Nejčastější témata:", ", ".join(t for t, _ in temata.most_common(3)))
