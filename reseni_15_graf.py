# Řešení: graf spánku a energie z deníku
import csv
from datetime import date
from pathlib import Path

import matplotlib
matplotlib.use("Agg")              # kreslíme do souboru, nepotřebujeme okno
import matplotlib.pyplot as plt

soubor = Path(__file__).parent / "data" / "denik.csv"
with open(soubor, encoding="utf-8") as f:
    dny = list(csv.DictReader(f, delimiter=";"))

x = [date.fromisoformat(d["datum"]) for d in dny]
spanek = [float(d["spanek_hodin"].replace(",", ".")) for d in dny]
energie = [int(d["energie"]) for d in dny]
barvy = ["black" if d["poznamka"] else "lightgray" for d in dny]

fig, (horni, dolni) = plt.subplots(2, 1, figsize=(8, 5), sharex=True)
horni.plot(x, spanek, marker="o")
horni.set_ylabel("spánek (h)")
dolni.bar(x, energie, color=barvy)
dolni.set_ylabel("energie (1–10)")
dolni.set_title("tmavé sloupce = dny s poznámkou", fontsize=9, loc="left")
fig.autofmt_xdate()
fig.tight_layout()
fig.savefig(Path(__file__).parent / "denik.png", dpi=150)
print("Graf uložen do souboru denik.png")
