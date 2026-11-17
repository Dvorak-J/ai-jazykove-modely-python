# Streamování: odpověď vypisujeme postupně, jak ji model generuje
from llm import MODEL, klient

proud = klient.chat.completions.create(
    model=MODEL,
    messages=[{"role": "user", "content": "Napiš krátkou báseň o programátorovi, který hledá chybu."}],
    stream=True,
)

for kousek in proud:
    if not kousek.choices:          # některé servery posílají i kousky bez textu
        continue
    text = kousek.choices[0].delta.content
    if text:
        print(text, end="", flush=True)
print()
