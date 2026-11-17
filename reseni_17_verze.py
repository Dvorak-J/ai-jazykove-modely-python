# Řešení: ukládání verzí modelu a příkaz 'zpet' (doplněk k programu 17_openscad.py)
import shutil
from pathlib import Path

SLOZKA = Path(__file__).parent / "model3d"
SCAD = SLOZKA / "model.scad"


def uloz_verzi():
    """Zkopíruje aktuální model jako další očíslovanou verzi a vrátí její číslo."""
    cislo = len(list(SLOZKA.glob("model_v*.scad"))) + 1
    shutil.copy(SCAD, SLOZKA / f"model_v{cislo}.scad")
    return cislo


def zpet(zpravy):
    """Obnoví předchozí verzi a z historie odebere poslední požadavek i odpovědi."""
    verze = sorted(SLOZKA.glob("model_v*.scad"), key=lambda p: int(p.stem[7:]))
    if len(verze) < 2:
        return "Není k čemu se vrátit."
    verze[-1].unlink()                         # zahodíme poslední verzi
    shutil.copy(verze[-2], SCAD)               # a obnovíme předposlední
    while len(zpravy) > 1:                     # systémovou zprávu ponecháme
        zprava = zpravy.pop()
        if zprava["role"] == "user" and not zprava["content"].startswith("OpenSCAD hlásí"):
            break                              # odebrali jsme poslední požadavek
    return f"Obnovena verze {len(verze) - 1}."


if __name__ == "__main__":                     # krátký test bez jazykového modelu
    SLOZKA.mkdir(exist_ok=True)
    zpravy = [{"role": "system", "content": "..."}]
    for i, tvar in enumerate(["cube(10);", "sphere(5);"], 1):
        zpravy += [{"role": "user", "content": f"požadavek {i}"},
                   {"role": "assistant", "content": tvar}]
        SCAD.write_text(tvar, encoding="utf-8")
        print("Uložena verze", uloz_verzi())
    print(zpet(zpravy), "| model:", SCAD.read_text(encoding="utf-8"),
          "| zpráv v historii:", len(zpravy))
    shutil.rmtree(SLOZKA)
