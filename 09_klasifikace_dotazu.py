# ŠkolBot: rozpoznání druhu dotazu (klasifikace)
from typing import Literal

from pydantic import BaseModel, Field

from strukturovane import ziskej_data


class Dotaz(BaseModel):
    kategorie: Literal["rozvrh", "jidelna", "ucivo", "skolni_rad", "technicky_problem", "jine"]
    chce_hotovy_ukol: bool = Field(
        description="true, pokud student chce, aby za něj někdo vypracoval úkol nebo test"
    )


SYSTEM = (
    "Třídíš dotazy studentů střední školy. Kategorie: rozvrh (hodiny, suplování), "
    "jidelna (obědy, objednávky), ucivo (vysvětlení látky), skolni_rad (pravidla, "
    "omluvenky, docházka), technicky_problem (Wi-Fi, počítače, přihlášení), jine."
)

DOTAZY = [
    "Kdy dnes končí odpolední vyučování?",
    "Jak si odhlásím zítřejší oběd?",
    "Můžeš mi vysvětlit, co je rekurze?",
    "Napiš mi celý referát o Karlu IV., ať ho můžu odevzdat.",
    "Nejde mi přihlásit se do Teams.",
    "Do kdy musím donést omluvenku?",
]

for text in DOTAZY:
    dotaz = ziskej_data(text, Dotaz, system=SYSTEM)
    znacka = "  <- chce hotový úkol!" if dotaz.chce_hotovy_ukol else ""
    print(f"{dotaz.kategorie:18} {text}{znacka}")
