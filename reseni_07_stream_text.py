# Řešení: streamování se skládáním celé odpovědi
from llm import MODEL, klient

proud = klient.chat.completions.create(
    model=MODEL,
    messages=[{"role": "user", "content": "Napiš krátkou báseň o programátorovi, který hledá chybu."}],
    stream=True,
)

casti = []
for kousek in proud:
    if not kousek.choices:
        continue
    text = kousek.choices[0].delta.content
    if text:
        print(text, end="", flush=True)
        casti.append(text)
print()

cela_odpoved = "".join(casti)
print(f"\nZnaků: {len(cela_odpoved)}, slov: {len(cela_odpoved.split())}")
