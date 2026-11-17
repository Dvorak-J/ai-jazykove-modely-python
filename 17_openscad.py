# Modelování ve 3D rozhovorem: jazykový model píše kód pro OpenSCAD,
# program ho uloží, nechá OpenSCAD model ověřit a vytvoří soubor STL pro 3D tisk.
# V OpenSCADu otevřete model3d/model.scad a zapněte Design > Automatic Reload
# and Preview: každou změnu pak uvidíte hned.
import os
import re
import shutil
import subprocess
from pathlib import Path

from llm import MODEL, klient

OPENSCAD = os.getenv("OPENSCAD") or shutil.which("openscad")
SLOZKA = Path(__file__).parent / "model3d"
SCAD = SLOZKA / "model.scad"
MAX_OPRAV = 3

SYSTEM = """Jsi konstruktér, který navrhuje 3D modely v jazyce OpenSCAD pro 3D tisk.
Pravidla:
- Rozměry jsou v milimetrech. Důležité rozměry dej na začátek souboru jako
  pojmenované proměnné s komentářem, aby je šlo snadno upravit.
- Model musí stát na podložce (z = 0) a pokud to jde, dát se vytisknout bez podpěr.
- Pro oblé tvary nastav $fn = 64.
- Vždy odpověz celým kódem v jednom bloku ```openscad a pod něj napiš jednou
  větou, co jsi udělal nebo změnil."""


def vytahni_kod(text):
    shoda = re.search(r"```(?:openscad|scad)?[ \t]*\n(.*?)```", text, re.S)
    return shoda.group(1).strip() if shoda else None


def over_model(kod):
    """Uloží kód a nechá OpenSCAD vytvořit STL. Vrátí text chyby, nebo None."""
    SCAD.write_text(kod, encoding="utf-8")
    try:
        vysledek = subprocess.run([OPENSCAD, "-o", str(SLOZKA / "model.stl"), str(SCAD)],
                                  capture_output=True, text=True, timeout=180)
    except subprocess.TimeoutExpired:
        return "Výpočet modelu trval příliš dlouho, zjednoduš ho."
    # varování o neznámém modulu nebo proměnné bereme jako chybu: OpenSCAD by
    # takovou část modelu tiše vynechal
    chyby = [r for r in vysledek.stderr.splitlines() if "ERROR" in r or "unknown" in r]
    if vysledek.returncode != 0 or chyby:
        return "\n".join(chyby[:5]) or vysledek.stderr[-600:]
    return None


if OPENSCAD is None:
    raise SystemExit("OpenSCAD nebyl nalezen. Nainstalujte ho z openscad.org a případně "
                     "nastavte cestu v .env, např. OPENSCAD=C:\\Program Files\\OpenSCAD\\openscad.exe")
SLOZKA.mkdir(exist_ok=True)
zpravy = [{"role": "system", "content": SYSTEM}]
print(f"Model se ukládá do {SCAD}. Popište, co chcete vymodelovat ('konec' = konec).")

while (pozadavek := input("\nVy: ").strip()).lower() != "konec":
    zpravy.append({"role": "user", "content": pozadavek})
    for pokus in range(MAX_OPRAV):
        odpoved = klient.chat.completions.create(model=MODEL, messages=zpravy, temperature=0.2)
        text = odpoved.choices[0].message.content or ""
        zpravy.append({"role": "assistant", "content": text})
        kod = vytahni_kod(text)
        chyba = over_model(kod) if kod else "V odpovědi chybí blok s kódem OpenSCAD."
        if chyba is None:
            print("Model:", text.rsplit("```", 1)[-1].strip() or "Hotovo.")
            print("Uloženo: model.scad a model.stl (pro 3D tisk)")
            break
        print(f"  (OpenSCAD hlásí chybu, oprava {pokus + 1}/{MAX_OPRAV})")
        zpravy.append({"role": "user", "content": f"OpenSCAD hlásí:\n{chyba}\nOprav kód."})
    else:
        print("Model se nepodařilo opravit. Zkuste požadavek popsat jinak nebo jednodušeji.")
