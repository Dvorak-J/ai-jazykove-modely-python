"""Pomocné funkce pro osobní zdravotní deník (kapitola 15).

Jazykový model zde jen převádí text laboratorní zprávy na data a píše souhrn.
Porovnání s referenčními mezemi, kontrolu převzatých čísel a bezpečnostní
pravidla zajišťuje program."""
import json
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

from pydantic import BaseModel, Field

from strukturovane import ziskej_data


class Vysledek(BaseModel):
    nazev: str = Field(description="název vyšetření přesně jako ve zprávě, např. S-Ferritin")
    hodnota: float
    jednotka: str
    dolni_mez: float | None = Field(description="dolní referenční mez ze zprávy, jinak None")
    horni_mez: float | None = Field(description="horní referenční mez ze zprávy, jinak None")


class Rozbor(BaseModel):
    datum_odberu: date
    vysledky: list[Vysledek]


def je_lokalni(url):
    """Běží model na tomto počítači nebo v místní síti?"""
    host = urlparse(url).hostname or ""
    return host in ("localhost", "127.0.0.1", "::1") or host.startswith(("192.168.", "10."))


def nacti_rozbor(soubor):
    """Převede laboratorní zprávu na data. Výsledek uloží vedle zprávy (.json),
    takže model se volá pro každou zprávu jen jednou."""
    soubor = Path(soubor)
    ulozeny = soubor.with_suffix(".json")
    if ulozeny.exists():
        return Rozbor.model_validate_json(ulozeny.read_text(encoding="utf-8"))
    prompt = ("Převeď výsledky z laboratorní zprávy ve značkách na data. Čísla opiš "
              "přesně tak, jak jsou ve zprávě, nic nepřidávej ani nedopočítávej.\n\n"
              f"<zprava>\n{soubor.read_text(encoding='utf-8')}\n</zprava>")
    rozbor = ziskej_data(prompt, Rozbor)
    ulozeny.write_text(rozbor.model_dump_json(indent=2), encoding="utf-8")
    return rozbor


def cislo_v_textu(cislo, text):
    """Ověří, že se číslo ve zprávě opravdu vyskytuje (v libovolném zápisu)."""
    for des in range(4):
        zapis = f"{cislo:.{des}f}".replace(".", ",")
        if re.search(rf"(?<![\d,]){re.escape(zapis)}(?![\d,])", text):
            return True
    return False


def zkontroluj_prevzeti(rozbor, text):
    """Vrátí seznam čísel, která model uvedl, ale ve zprávě nejsou."""
    chyby = []
    for v in rozbor.vysledky:
        for cislo in (v.hodnota, v.dolni_mez, v.horni_mez):
            if cislo is not None and not cislo_v_textu(cislo, text):
                chyby.append(f"{v.nazev}: {cislo}")
    return chyby


def vyhodnot(v):
    """Porovnání s referenčními mezemi ze zprávy (žádné vlastní meze)."""
    if v.dolni_mez is not None and v.hodnota < v.dolni_mez:
        stav = "pod mezí"
        vyrazne = v.hodnota < v.dolni_mez / 2
    elif v.horni_mez is not None and v.hodnota > v.horni_mez:
        stav = "nad mezí"
        vyrazne = v.hodnota > v.horni_mez * 2
    else:
        return "v mezích"
    return stav + (" (VÝRAZNĚ)" if vyrazne else "")


# Bezpečnostní pravidla pro text souhrnu: žádné dávky a žádné pokyny k užívání
ZAKAZANE = [
    (r"\d+(?:[.,]\d+)?\s*"
     r"(?:mg|µg|μg|ug|mcg|IU|I\.U\.|m\.\s?j\.|tablet|kapsl|kapk)(?!\s*/)",
     "dávka"),                         # (?!\s*/) vynechá koncentrace jako 28 µg/l
    (r"\b(?:užívejte|užijte|berte|vezměte|vysaďte|přestaňte|zvyšte|snižte|začněte)\b",
     "pokyn k léčbě"),
    (r"\b(?:máte|trpíte)\s+(?:nedostat|anémi|chudokrevnost|cukrovk|hypo|hyper)\w*",
     "diagnóza"),
]


def poruseni(text):
    """Najde v textu porušení pravidel. Vrací seznam dvojic (druh, úryvek)."""
    nalezene = []
    for vzor, druh in ZAKAZANE:
        for shoda in re.finditer(vzor, text, re.IGNORECASE):
            nalezene.append((druh, shoda.group(0)))
    return nalezene


if __name__ == "__main__":
    print(cislo_v_textu(2.1, "S-TSH  2,10  mIU/l"), cislo_v_textu(38.0, "D 38 nmol/l"))
    print(poruseni("Užívejte 2000 IU vitaminu D denně."))
    print(poruseni("Zeptejte se lékaře, zda je vhodné doplňovat vitamin D."))
    print(json.dumps(je_lokalni("http://localhost:11434/v1")))
