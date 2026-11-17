"""Pomocné funkce pro získávání strukturovaných dat (JSON) z jazykového modelu."""
import json

import openai
from pydantic import ValidationError

from llm import MODEL, klient


def vytahni_json(text):
    """Najde v textu JSON (objekt nebo pole) a vrátí ho jako řetězec.
    Odstraní tak např. značky ```json nebo úvodní větu 'Tady je JSON:'."""
    zacatky = [i for i in (text.find("{"), text.find("[")) if i != -1]
    konec = max(text.rfind("}"), text.rfind("]"))
    if not zacatky or konec == -1:
        raise ValueError("V odpovědi není žádný JSON.")
    return text[min(zacatky):konec + 1]


def ziskej_data(prompt, trida, system=None, pokusy=3):
    """Zeptá se modelu a odpověď převede na objekt zadané Pydantic třídy.
    Když odpověď neodpovídá schématu, pošle modelu popis chyby a nechá ho
    odpověď opravit."""
    schema = trida.model_json_schema()
    pokyn = (
        "Odpověz pouze JSONem podle tohoto JSON schématu, bez dalšího textu:\n"
        + json.dumps(schema, ensure_ascii=False)
    )
    zpravy = [{"role": "system", "content": (system + "\n\n" if system else "") + pokyn},
              {"role": "user", "content": prompt}]

    for pokus in range(pokusy):
        try:
            odpoved = klient.chat.completions.create(
                model=MODEL,
                messages=zpravy,
                temperature=0,
                response_format={
                    "type": "json_schema",
                    "json_schema": {"name": trida.__name__, "schema": schema},
                },
            )
        except openai.BadRequestError:
            # server strukturovaný výstup nepodporuje: spolehneme se na pokyn v promptu
            odpoved = klient.chat.completions.create(model=MODEL, messages=zpravy, temperature=0)
        text = odpoved.choices[0].message.content or ""
        try:
            return trida.model_validate_json(vytahni_json(text))
        except (ValueError, ValidationError) as chyba:
            # chybnou odpověď i popis chyby přidáme do konverzace a zkusíme znovu
            zpravy.append({"role": "assistant", "content": text})
            zpravy.append({"role": "user",
                           "content": f"Tvoje odpověď není platná: {chyba}\nPošli opravený JSON."})
    raise ValueError(f"Model ani po {pokusy} pokusech nevrátil platná data.")
