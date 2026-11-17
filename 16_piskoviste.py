# Nástroje pro agenta, které smějí pracovat jen uvnitř jedné složky (pískoviště).
# Kontrola v programu je jen první vrstva ochrany, ne náhrada virtuálního počítače.
import os
import subprocess
import sys
from pathlib import Path

from nastroje import popis

PISKOVISTE = (Path(__file__).parent / "piskoviste").resolve()
PISKOVISTE.mkdir(exist_ok=True)
MAX_ZNAKU = 100_000
TAJNE = ("KEY", "TOKEN", "SECRET", "PASSWORD", "HESLO")


def bezpecna_cesta(nazev):
    """Převede jméno souboru na cestu a ověří, že leží uvnitř pískoviště."""
    cesta = (PISKOVISTE / nazev).resolve()     # vyřeší i '..' a zástupce (symlinky)
    if not cesta.is_relative_to(PISKOVISTE):
        raise PermissionError(f"Cesta '{nazev}' vede mimo pískoviště.")
    return cesta


def seznam_souboru():
    soubory = [p for p in PISKOVISTE.rglob("*") if p.is_file()]
    return {"soubory": sorted(str(p.relative_to(PISKOVISTE)) for p in soubory)}


def precti_soubor(nazev):
    try:
        return {"obsah": bezpecna_cesta(nazev).read_text(encoding="utf-8")[:MAX_ZNAKU]}
    except (PermissionError, FileNotFoundError) as chyba:
        return {"chyba": str(chyba)}


def zapis_soubor(nazev, obsah):
    try:
        cesta = bezpecna_cesta(nazev)
    except PermissionError as chyba:
        return {"chyba": str(chyba)}
    if len(obsah) > MAX_ZNAKU:
        return {"chyba": "Obsah je příliš dlouhý."}
    if cesta.exists():                         # nic nepřepíšeme bez zálohy
        zaloha = cesta.with_name(cesta.name + ".zaloha")
        zaloha.write_text(cesta.read_text(encoding="utf-8"), encoding="utf-8")
    cesta.parent.mkdir(parents=True, exist_ok=True)
    cesta.write_text(obsah, encoding="utf-8")
    return {"stav": "uloženo", "soubor": nazev}


def spust_python(nazev, limit=10):
    """Spustí skript z pískoviště s časovým limitem a bez tajných proměnných."""
    try:
        cesta = bezpecna_cesta(nazev)
    except PermissionError as chyba:
        return {"chyba": str(chyba)}
    prostredi = {k: v for k, v in os.environ.items()
                 if not any(slovo in k.upper() for slovo in TAJNE)}
    try:
        vysledek = subprocess.run([sys.executable, "-I", str(cesta)], cwd=PISKOVISTE,
                                  env=prostredi, capture_output=True, text=True, timeout=limit)
    except subprocess.TimeoutExpired:
        return {"chyba": f"Program běžel déle než {limit} s a byl ukončen."}
    return {"kod": vysledek.returncode, "vystup": vysledek.stdout[-2000:],
            "chyby": vysledek.stderr[-2000:]}


SOUBOR = {"nazev": {"type": "string", "description": "cesta k souboru uvnitř pracovní složky"}}
NASTROJE = [
    popis("seznam_souboru", "Vypíše soubory v pracovní složce."),
    popis("precti_soubor", "Vrátí obsah textového souboru.", SOUBOR),
    popis("zapis_soubor", "Uloží text do souboru (existující soubor se zazálohuje).",
          {**SOUBOR, "obsah": {"type": "string", "description": "nový obsah souboru"}}),
    popis("spust_python", "Spustí skript v Pythonu z pracovní složky a vrátí jeho výstup.", SOUBOR),
]
FUNKCE = {"seznam_souboru": seznam_souboru, "precti_soubor": precti_soubor,
          "zapis_soubor": zapis_soubor, "spust_python": spust_python}

if __name__ == "__main__":
    print(zapis_soubor("ahoj.py", "print('Ahoj z pískoviště')"))
    print(spust_python("ahoj.py"))
    print(precti_soubor("../llm.py"))                 # pokus dostat se ven
    print(zapis_soubor("/tmp/utok.txt", "x"))          # absolutní cesta
    # Kontrola cest ale neomezuje, co udělá spuštěný kód:
    zapis_soubor("pruzkum.py", "import os\nprint(sorted(os.listdir('..'))[:5])")
    print(spust_python("pruzkum.py"))
