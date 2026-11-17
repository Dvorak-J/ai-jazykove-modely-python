# Generátor diferencovaného pracovního listu pro vyučující (export do Wordu).
# Spuštění: python 14_pracovni_list.py   (vyžaduje pip install python-docx)
from pathlib import Path

from docx import Document
from docx.shared import Pt
from pydantic import BaseModel, Field

from strukturovane import ziskej_data


class Priklad(BaseModel):
    zadani: str
    reseni: str = Field(description="výsledek a stručný postup pro vyučujícího")


class Uroven(BaseModel):
    nazev: str = Field(description="Základ, Rozšíření, nebo Výzva")
    priklady: list[Priklad] = Field(min_length=2, max_length=5)


class PracovniList(BaseModel):
    nadpis: str
    uvod: str = Field(description="jedna až dvě věty pro žáky, co si procvičí")
    urovne: list[Uroven] = Field(min_length=3, max_length=3)


def vytvor_list(tema, rocnik, zajmy, pocet):
    prompt = (
        f"Vytvoř pracovní list na téma: {tema}. Žáci: {rocnik}. Ve třídě je baví: {zajmy}. "
        f"Připrav tři úrovně (Základ, Rozšíření, Výzva), v každé {pocet} příklady. "
        "Zadání zasaď do situací, které žáky baví, ale matematický obsah musí být přesný. "
        "Každý příklad musí mít jednoznačný výsledek.")
    return ziskej_data(prompt, PracovniList)


def uloz_docx(prac_list, soubor):
    doc = Document()
    doc.styles["Normal"].font.size = Pt(11)
    doc.add_heading(prac_list.nadpis, level=1)
    doc.add_paragraph("Jméno: ______________________   Třída: ________   Datum: ________")
    doc.add_paragraph(prac_list.uvod)
    for uroven in prac_list.urovne:
        doc.add_heading(uroven.nazev, level=2)
        for priklad in uroven.priklady:
            doc.add_paragraph(priklad.zadani, style="List Number")
            doc.add_paragraph("\n")                       # místo na odpověď
    doc.add_page_break()
    doc.add_heading("Řešení pro vyučujícího", level=2)
    cislo = 0                          # příklady jsou číslované průběžně
    for uroven in prac_list.urovne:
        doc.add_paragraph(uroven.nazev).runs[0].bold = True
        for priklad in uroven.priklady:
            cislo += 1
            doc.add_paragraph(f"{cislo}. {priklad.reseni}")
    doc.save(soubor)


prac_list = vytvor_list(
    tema="procenta: výpočet procentové části a základu",
    rocnik="1. ročník střední průmyslové školy",
    zajmy="počítačové hry, fotbal, nakupování elektroniky",
    pocet=3,
)
soubor = Path(__file__).parent / "pracovni_list.docx"
uloz_docx(prac_list, soubor)
print(f"Pracovní list '{prac_list.nadpis}' uložen do {soubor.name}")
for uroven in prac_list.urovne:
    print(f"  {uroven.nazev}: {len(uroven.priklady)} příklady")
