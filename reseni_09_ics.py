# Řešení: rozšířená extrakce akcí a export do kalendáře (formát iCalendar)
import re
from datetime import date, datetime
from pathlib import Path

from pydantic import BaseModel, Field

from strukturovane import ziskej_data


class Akce(BaseModel):
    nazev: str = Field(description="krátký název akce")
    datum: date | None = Field(description="datum konání; None, pokud v textu není")
    cas: str | None = Field(description="čas začátku ve formátu HH:MM, pokud je uveden")
    misto: str | None = Field(description="místo konání, pokud je uvedeno")
    tridy: list[str] = Field(description="kterých tříd se akce týká; prázdný seznam = všech")
    povinna: bool = Field(description="je účast povinná?")
    kontaktni_osoba: str | None = Field(description="na koho se obrátit, pokud je uveden")
    zrusena: bool = Field(description="True, pokud oznámení akci ruší")


class SeznamAkci(BaseModel):
    akce: list[Akce]


OZNAMENI = """
Ve středu 21. října proběhne od 8:00 v aule beseda s absolventy oboru IT,
účast je povinná pro 3.A a 4.A. V pátek 23. 10. je Den otevřených dveří
od 9:00, dobrovolníci se hlásí u paní Novákové. Exkurze 2.B do Dolních
Vítkovic se přesouvá na 12. 11. Plánovaný koncert školního sboru se ruší.
Termín lyžařského kurzu pro první ročníky upřesníme.
"""


def na_ics(seznam):
    """Sestaví text souboru .ics. Řádky musí končit znaky CRLF."""
    radky = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Skola//Akce//CS"]
    razitko = datetime.now().strftime("%Y%m%dT%H%M%S")
    for i, akce in enumerate(seznam):
        if akce.datum is None or akce.zrusena:
            continue                      # bez data nebo zrušené akce do kalendáře nedáváme
        radky += ["BEGIN:VEVENT", f"UID:akce-{i}-{razitko}@skola", f"DTSTAMP:{razitko}",
                  f"SUMMARY:{akce.nazev}"]
        cas = re.fullmatch(r"(\d{1,2})[:.](\d{2})", akce.cas or "")
        if cas:
            hodiny, minuty = int(cas[1]), int(cas[2])
            radky.append(f"DTSTART:{akce.datum:%Y%m%d}T{hodiny:02d}{minuty:02d}00")
        else:
            radky.append(f"DTSTART;VALUE=DATE:{akce.datum:%Y%m%d}")   # celodenní akce
        if akce.misto:
            radky.append(f"LOCATION:{akce.misto}")
        radky.append("END:VEVENT")
    radky.append("END:VCALENDAR")
    return "\r\n".join(radky) + "\r\n"


prompt = (f"Dnešní datum je {date.today():%d. %m. %Y}. Vypiš všechny akce "
          f"z tohoto oznámení, včetně zrušených a akcí bez data:\n\n{OZNAMENI}")
vysledek = ziskej_data(prompt, SeznamAkci)

for akce in vysledek.akce:
    stav = "ZRUŠENO" if akce.zrusena else ("povinná" if akce.povinna else "")
    datum = f"{akce.datum:%d. %m.}" if akce.datum else "??. ??."
    print(f"{datum}  {akce.cas or '':5}  {akce.nazev}  {stav}")

soubor = Path(__file__).parent / "akce.ics"
soubor.write_text(na_ics(vysledek.akce), encoding="utf-8", newline="")
print(f"\nUloženo do {soubor.name}")
