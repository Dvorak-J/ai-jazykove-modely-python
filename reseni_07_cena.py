# Řešení: dotaz od uživatele, spotřeba tokenů a cena dotazu
from llm import MODEL, klient

CENA_VSTUP = 0.30    # USD za milion vstupních tokenů (smyšlená cena z příkladu)
CENA_VYSTUP = 2.50   # USD za milion výstupních tokenů

otazka = input("Na co se chcete zeptat? ")
odpoved = klient.chat.completions.create(
    model=MODEL,
    messages=[{"role": "user", "content": otazka}],
)

print(odpoved.choices[0].message.content)
vstup = odpoved.usage.prompt_tokens
vystup = odpoved.usage.completion_tokens
cena = vstup / 1_000_000 * CENA_VSTUP + vystup / 1_000_000 * CENA_VYSTUP
print(f"\nTokeny: {vstup} vstup, {vystup} výstup")
print(f"Cena dotazu: {cena:.6f} USD, tedy asi {cena * 1000:.2f} USD za tisíc takových dotazů")
