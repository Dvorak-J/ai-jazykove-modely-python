# Měření rychlosti modelu: doba do prvního tokenu a rychlost generování
import time

from llm import MODEL, klient

PROMPT = "Popiš v pěti větách, jak funguje počítač."

start = time.perf_counter()
prvni = None
kousku = 0
proud = klient.chat.completions.create(
    model=MODEL, messages=[{"role": "user", "content": PROMPT}], stream=True
)
for kousek in proud:
    if kousek.choices and kousek.choices[0].delta.content:
        if prvni is None:
            prvni = time.perf_counter()   # okamžik, kdy dorazil první text
        kousku += 1
konec = time.perf_counter()

print(f"Model: {MODEL}")
if prvni is None:
    print("Model nevrátil žádný text.")
else:
    generovani = max(konec - prvni, 1e-9)
    print(f"Doba do prvního tokenu: {prvni - start:.2f} s")
    print(f"Generování: {kousku} kousků textu za {generovani:.2f} s")
    print(f"Rychlost: přibližně {kousku / generovani:.1f} tokenů za sekundu")
