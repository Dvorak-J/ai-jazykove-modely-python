# První dotaz na jazykový model pomocí knihovny openai
from llm import MODEL, klient

odpoved = klient.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "user", "content": "Vysvětli jednou větou, co je proměnná v programování."}
    ],
)

print(odpoved.choices[0].message.content)
print()
print("Model:", odpoved.model)
print("Důvod ukončení:", odpoved.choices[0].finish_reason)
print("Tokeny vstupu:", odpoved.usage.prompt_tokens)
print("Tokeny odpovědi:", odpoved.usage.completion_tokens)
