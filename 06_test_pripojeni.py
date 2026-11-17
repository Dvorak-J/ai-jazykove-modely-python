# Ověří, že se program dokáže spojit s jazykovým modelem
import openai

from llm import BASE_URL, MODEL, klient

print(f"Server: {BASE_URL}")
print(f"Model:  {MODEL}")

try:
    modely = [m.id for m in klient.models.list()]
    print("Dostupné modely:", ", ".join(modely[:10]))
except openai.APIError:
    print("(Seznam modelů se nepodařilo načíst, nevadí.)")

try:
    odpoved = klient.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": "Odpověz jednou krátkou větou: slyšíš mě?"}],
    )
    print("Model odpověděl:", odpoved.choices[0].message.content)
    print("Spojení funguje.")
except openai.APIConnectionError:
    print("Nepodařilo se spojit se serverem. Běží Ollama? Je správná adresa LLM_BASE_URL?")
except openai.AuthenticationError:
    print("Server odmítl API klíč. Zkontrolujte LLM_API_KEY v souboru .env.")
except openai.NotFoundError:
    print(f"Model '{MODEL}' nebyl nalezen. U Ollamy ho stáhněte: ollama pull {MODEL}")
except openai.RateLimitError:
    print("Byl překročen limit požadavků. Chvíli počkejte a zkuste to znovu.")
