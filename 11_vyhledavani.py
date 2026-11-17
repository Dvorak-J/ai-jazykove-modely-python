# Krok 2: vyhledávání podle významu (bez generování odpovědi)
from pathlib import Path

from rag import nacti_index, vyhledej

index = nacti_index(Path(__file__).parent / "index.json")

while True:
    dotaz = input("\nHledat (prázdný řádek = konec): ").strip()
    if not dotaz:
        break
    for podobnost, usek in vyhledej(dotaz, index):
        print(f"  {podobnost:.3f}  {usek['nadpis']}: {usek['text'][:70]}…")
