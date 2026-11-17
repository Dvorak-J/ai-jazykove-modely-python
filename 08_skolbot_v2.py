# ŠkolBot verze 2: chatbot s pamětí konverzace
import json
from datetime import datetime
from pathlib import Path

import openai

from llm import MODEL, klient

SLOZKA = Path(__file__).parent
SYSTEM = (SLOZKA / "system_prompt.txt").read_text(encoding="utf-8")
MAX_ZPRAV = 20  # kolik posledních zpráv (kromě systémové) posíláme modelu


def nova_konverzace():
    return [{"role": "system", "content": SYSTEM}]


def orizni(zpravy, max_zprav=MAX_ZPRAV):
    """Vrátí systémovou zprávu a jen posledních max_zprav zpráv."""
    return zpravy[:1] + zpravy[1:][-max_zprav:]


def odpovez(zpravy):
    """Pošle konverzaci modelu, odpověď průběžně vypisuje a vrátí ji celou."""
    proud = klient.chat.completions.create(
        model=MODEL, messages=orizni(zpravy), stream=True
    )
    casti = []
    for kousek in proud:
        if kousek.choices and kousek.choices[0].delta.content:
            text = kousek.choices[0].delta.content
            print(text, end="", flush=True)
            casti.append(text)
    print()
    return "".join(casti)


def uloz(zpravy):
    soubor = SLOZKA / f"konverzace_{datetime.now():%Y-%m-%d_%H-%M-%S}.json"
    soubor.write_text(json.dumps(zpravy, ensure_ascii=False, indent=2), encoding="utf-8")
    return soubor.name


def vypis_historii(zpravy):
    for i, zprava in enumerate(zpravy):
        zacatek = zprava["content"][:60].replace("\n", " ")
        print(f"  {i:2}. {zprava['role']:9} {zacatek}")
    znaku = sum(len(z["content"]) for z in zpravy)
    print(f"  Zpráv: {len(zpravy)}, znaků: {znaku} (přibližně {znaku // 3} tokenů)")


zpravy = nova_konverzace()
print("ŠkolBot v2. Příkazy: /historie, /reset, /ulozit, /konec")

while True:
    vstup = input("\nTy: ").strip()
    if not vstup:
        continue
    if vstup == "/konec":
        break
    if vstup == "/reset":
        zpravy = nova_konverzace()
        print("(Konverzace smazána.)")
        continue
    if vstup == "/ulozit":
        print(f"(Uloženo do souboru {uloz(zpravy)})")
        continue
    if vstup == "/historie":
        vypis_historii(zpravy)
        continue

    zpravy.append({"role": "user", "content": vstup})
    print("ŠkolBot: ", end="")
    try:
        odpoved = odpovez(zpravy)
    except openai.APIError as chyba:
        print(f"\n(Chyba při komunikaci s modelem: {chyba})")
        zpravy.pop()  # neúspěšnou otázku z historie odebereme
        continue
    zpravy.append({"role": "assistant", "content": odpoved})
