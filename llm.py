"""Společné nastavení pro všechny programy: připojení k jazykovému modelu.

Hodnoty se načítají ze souboru .env. Při změně poskytovatele modelu
proto stačí upravit .env a programy zůstanou beze změny.
"""
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # načte proměnné ze souboru .env, pokud existuje

BASE_URL = os.getenv("LLM_BASE_URL", "http://localhost:11434/v1")
API_KEY = os.getenv("LLM_API_KEY", "ollama")
MODEL = os.getenv("LLM_MODEL", "gemma3:4b")
EMBED_MODEL = os.getenv("EMBED_MODEL", "embeddinggemma")

klient = OpenAI(base_url=BASE_URL, api_key=API_KEY)
