# Kartičky s opakováním podle Leitnerova systému.
# Jazykový model kartičky jen vytvoří, plán opakování řídí program.
import json
import random
from datetime import date, timedelta
from pathlib import Path

from pydantic import BaseModel, Field

from strukturovane import ziskej_data

SLOZKA = Path(__file__).parent
SOUBOR = SLOZKA / "karticky.json"
INTERVALY = {1: 1, 2: 2, 3: 4, 4: 8, 5: 16}   # přihrádka: za kolik dní znovu


class Karticka(BaseModel):
    otazka: str = Field(description="krátká otázka, na kterou lze odpovědět jednou větou")
    odpoved: str = Field(description="správná odpověď, nejvýše dvě věty")


class Balicek(BaseModel):
    karticky: list[Karticka] = Field(min_length=3, max_length=12)


def vytvor_karticky(poznamky):
    prompt = ("Z poznámek ve značkách vytvoř 6 až 10 kartiček pro opakování. Každá "
              "kartička zkouší jednu myšlenku. Používej jen informace z poznámek.\n\n"
              f"<poznamky>\n{poznamky}\n</poznamky>")
    balicek = ziskej_data(prompt, Balicek)
    dnes = date.today().isoformat()
    return [{"otazka": k.otazka, "odpoved": k.odpoved, "prihradka": 1, "kdy": dnes}
            for k in balicek.karticky]


def k_opakovani(karticky, dnes):
    return [k for k in karticky if date.fromisoformat(k["kdy"]) <= dnes]


def ohodnot(karticka, umel, dnes):
    """Správná odpověď posune kartičku o přihrádku výš, chybná zpět do první."""
    karticka["prihradka"] = min(karticka["prihradka"] + 1, 5) if umel else 1
    za_dni = INTERVALY[karticka["prihradka"]]
    karticka["kdy"] = (dnes + timedelta(days=za_dni)).isoformat()


if SOUBOR.exists():
    karticky = json.loads(SOUBOR.read_text(encoding="utf-8"))
else:
    poznamky = (SLOZKA / "data" / "poznamky_slovniky.md").read_text(encoding="utf-8")
    karticky = vytvor_karticky(poznamky)
    print(f"Vytvořeno {len(karticky)} kartiček.")

dnes = date.today()
dnesni = k_opakovani(karticky, dnes)
random.shuffle(dnesni)
print(f"Dnes k opakování: {len(dnesni)}. Napište 'konec' pro ukončení.\n")
for karticka in dnesni:
    print("Otázka:", karticka["otazka"])
    if input("Vaše odpověď: ").strip().lower() == "konec":
        break
    print("Správně:", karticka["odpoved"])
    umel = input("Věděli jste to? (a/n): ").strip().lower().startswith("a")
    ohodnot(karticka, umel, dnes)
    print()

SOUBOR.write_text(json.dumps(karticky, ensure_ascii=False, indent=2), encoding="utf-8")
pocty = [sum(k["prihradka"] == p for k in karticky) for p in INTERVALY]
print("Kartiček v přihrádkách 1 až 5:", pocty)
