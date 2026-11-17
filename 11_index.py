# Krok 1: rozdělí dokument na úseky, spočítá embeddingy a uloží index
from pathlib import Path

from rag import vytvor_index

SLOZKA = Path(__file__).parent
index = vytvor_index(SLOZKA / "data" / "skolni_rad.md", SLOZKA / "index.json")

print(f"Počet úseků: {len(index)}")
print(f"Rozměr embeddingu: {len(index[0]['vektor'])}")
for i, usek in enumerate(index):
    print(f"  [{i}] {usek['nadpis']} ({len(usek['text'])} znaků)")
