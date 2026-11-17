# Odolné volání modelu: opakování při dočasných chybách
import time

import openai

from llm import MODEL, klient


def zeptej_se(otazka, system=None, teplota=0.7, pokusy=4):
    """Pošle otázku modelu a vrátí text odpovědi.
    Při dočasné chybě (limit požadavků, výpadek spojení) to zkusí znovu,
    pokaždé s delší pauzou (1 s, 2 s, 4 s, ...)."""
    zpravy = []
    if system:
        zpravy.append({"role": "system", "content": system})
    zpravy.append({"role": "user", "content": otazka})

    for pokus in range(pokusy):
        try:
            odpoved = klient.chat.completions.create(
                model=MODEL, messages=zpravy, temperature=teplota
            )
            return odpoved.choices[0].message.content
        except (openai.RateLimitError, openai.APIConnectionError) as chyba:
            if pokus == pokusy - 1:
                raise                       # došly pokusy, chybu předáme dál
            pauza = 2 ** pokus
            print(f"(dočasná chyba: {type(chyba).__name__}, zkusím to znovu za {pauza} s)")
            time.sleep(pauza)


if __name__ == "__main__":
    print(zeptej_se("Kolik nohou má pavouk? Odpověz číslem.", teplota=0))
