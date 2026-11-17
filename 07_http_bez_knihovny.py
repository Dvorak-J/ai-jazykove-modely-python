# Dotaz na jazykový model "ručně": jen standardní knihovna Pythonu
import json
import os
import urllib.request

from dotenv import load_dotenv

load_dotenv()
adresa = os.getenv("LLM_BASE_URL", "http://localhost:11434/v1").rstrip("/")
klic = os.getenv("LLM_API_KEY", "ollama")
model = os.getenv("LLM_MODEL", "gemma3:4b")

# 1) Sestavíme tělo požadavku jako slovník a převedeme ho na JSON
pozadavek = {
    "model": model,
    "messages": [
        {"role": "user", "content": "Jaké je hlavní město Slovenska? Odpověz jednou větou."}
    ],
}
data = json.dumps(pozadavek).encode("utf-8")

# 2) Pošleme HTTP POST na endpoint /chat/completions
http_pozadavek = urllib.request.Request(
    adresa + "/chat/completions",
    data=data,
    headers={
        "Content-Type": "application/json",
        "Authorization": "Bearer " + klic,
    },
)
with urllib.request.urlopen(http_pozadavek) as http_odpoved:
    odpoved = json.loads(http_odpoved.read().decode("utf-8"))

# 3) Odpověď je opět JSON; vypíšeme ji celou a pak jen text
print(json.dumps(odpoved, indent=2, ensure_ascii=False))
print()
print("Text odpovědi:", odpoved["choices"][0]["message"]["content"])
