# Krok 3: odpovědi podle dokumentu (RAG) s uvedením zdrojů
from pathlib import Path

from llm import MODEL, klient
from rag import nacti_index, vyhledej

index = nacti_index(Path(__file__).parent / "index.json")

SYSTEM = """Jsi ŠkolBot. Odpovídáš na otázky studentů výhradně podle úseků
školního řádu, které dostaneš v kontextu. Za každé tvrzení uveď v hranatých
závorkách číslo úseku, ze kterého pochází, např. [2]. Pokud odpověď v úsecích
není, napiš: "Tohle ve školním řádu nemám, zeptej se třídního učitele."
Nic si nedomýšlej. Odpovídej česky a stručně."""


def odpovez(otazka):
    nalezene = vyhledej(otazka, index, pocet=3)
    kontext = "\n\n".join(
        f"[{i}] {usek['nadpis']}\n{usek['text']}"
        for i, (_, usek) in enumerate(nalezene, 1)
    )
    odpoved = klient.chat.completions.create(
        model=MODEL,
        temperature=0.2,
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": f"Kontext:\n{kontext}\n\nOtázka: {otazka}"},
        ],
    )
    zdroje = [f"[{i}] {usek['nadpis']}" for i, (_, usek) in enumerate(nalezene, 1)]
    return odpoved.choices[0].message.content, zdroje


while True:
    otazka = input("\nTy: ").strip()
    if not otazka or otazka.lower() == "konec":
        break
    text, zdroje = odpovez(otazka)
    print("ŠkolBot:", text)
    print("Zdroje:", "; ".join(zdroje))
