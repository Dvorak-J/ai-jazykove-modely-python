# Volání Ollamy její vlastní knihovnou (pip install ollama)
import ollama

from llm import BASE_URL, MODEL

# Nativní API Ollamy je na stejném serveru, jen bez koncovky /v1
klient = ollama.Client(host=BASE_URL.rstrip("/").removesuffix("/v1"))

odpoved = klient.chat(
    model=MODEL,
    messages=[{"role": "user", "content": "Napiš jednu větu o tom, proč je dobré učit se programovat."}],
    options={"temperature": 0.7, "num_ctx": 8192},  # num_ctx = velikost kontextového okna
)
print(odpoved.message.content)
print(f"Tokeny vstupu: {odpoved.prompt_eval_count}, tokeny odpovědi: {odpoved.eval_count}")
