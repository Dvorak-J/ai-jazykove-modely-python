# Vliv teploty: stejný dotaz třikrát při nízké a vysoké teplotě
from llm import MODEL, klient

PROMPT = "Vymysli originální název pro školní rockovou kapelu. Napiš jen název."

for teplota in [0.0, 1.2]:
    print(f"Teplota {teplota}:")
    for pokus in range(3):
        odpoved = klient.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": PROMPT}],
            temperature=teplota,
        )
        print("  -", odpoved.choices[0].message.content.strip())
