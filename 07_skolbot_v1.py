# ŠkolBot verze 1: odpovídá na otázky podle systémového promptu (zatím bez paměti)
from pathlib import Path

from llm import MODEL, klient

SYSTEM = (Path(__file__).parent / "system_prompt.txt").read_text(encoding="utf-8")

print("ŠkolBot v1 (pro ukončení napiš 'konec')")
while True:
    otazka = input("\nTy: ").strip()
    if otazka.lower() == "konec":
        break
    if not otazka:
        continue
    odpoved = klient.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": otazka},
        ],
    )
    print("ŠkolBot:", odpoved.choices[0].message.content)
