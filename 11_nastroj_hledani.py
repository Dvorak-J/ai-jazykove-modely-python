# Vyhledávání ve školním řádu jako nástroj pro agenta (kapitola 10)
from pathlib import Path

from nastroje import popis
from rag import nacti_index, vyhledej

INDEX = nacti_index(Path(__file__).parent / "index.json")


def hledej_ve_skolnim_radu(dotaz):
    nalezene = vyhledej(dotaz, INDEX, pocet=3)
    return {"useky": [{"nadpis": u["nadpis"], "text": u["text"]} for _, u in nalezene]}


NASTROJ_HLEDANI = popis(
    "hledej_ve_skolnim_radu",
    "Vyhledá ve školním řádu úseky související s dotazem. Použij pro otázky "
    "o pravidlech školy, omluvenkách, jídelně, knihovně, praxi a provozu školy.",
    {"dotaz": {"type": "string", "description": "co hledat, celou větou"}},
)

if __name__ == "__main__":
    for usek in hledej_ve_skolnim_radu("Jak dlouho si můžu půjčit knihu?")["useky"]:
        print("-", usek["nadpis"])
