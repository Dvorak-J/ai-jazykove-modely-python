# Ukázkové programy k učebnímu textu „Umělá inteligence a jazykové modely v Pythonu“

## Jak začít

1. Nainstalujte Python 3.10 nebo novější.
2. V této složce vytvořte virtuální prostředí a nainstalujte knihovny:

       python -m venv .venv
       .venv\Scripts\activate          (Windows)
       source .venv/bin/activate       (macOS, Linux)
       pip install -r requirements.txt

3. Zkopírujte soubor `.env.example` jako `.env` a nastavte v něm, ke kterému
   jazykovému modelu se programy připojují (kapitola 6).
4. Ověřte spojení: `python 06_test_pripojeni.py`
   (když něco nefunguje, pomůže kapitola 22).

Programy z kapitol 1–4 nepotřebují žádný jazykový model ani knihovny,
stačí jakýkoli Python (i online kompilátor).

## Přehled souborů

| Kapitola | Soubory |
|---|---|
| 1 Co je umělá inteligence | `01_spam_pravidla.py`, `01_eliza.py` |
| 2 Jak se stroje učí | `02_primka.py`, `02_perceptron.py`, `02_sit_xor.py` |
| 3 Jak funguje velký jazykový model | `03_tokenizer_bpe.py`, `03_embeddingy.py` |
| 4 Mini jazykový model | `04_bigramy.py`, `04_teplota.py`, `data/korpus.txt` |
| 6 Pracovní prostředí | `llm.py` (společné nastavení), `.env.example`, `06_test_pripojeni.py` |
| 7 První program | `07_*.py`, `system_prompt.txt` |
| 8 Chatbot s pamětí | `08_skolbot_v2.py`, `08_shrnuti_historie.py`, `08_skolbot_web.py` (spouští se příkazem `streamlit run 08_skolbot_web.py`) |
| 9 Strukturovaný výstup | `strukturovane.py`, `09_*.py` |
| 10 Nástroje a agenti | `nastroje.py`, `10_cas.py`, `10_skolbot_nastroje.py` |
| 11 RAG | `rag.py`, `11_index.py` (spusťte jako první), `11_vyhledavani.py`, `11_rag.py`, `11_nastroj_hledani.py`, `data/skolni_rad.md` |
| 12 Lokální modely | `12_rychlost.py`, `12_ollama_nativne.py` (vyžaduje `pip install ollama`), `Modelfile` |
| 13 Etika a bezpečnost | `13_prompt_injection.py` |
| 14 Učení na míru | `14_karticky.py`, `14_tutor.py`, `14_pracovni_list.py`, `data/poznamky_slovniky.md` |
| 15 Osobní zdravotní deník | `zdravi.py`, `15_rozbor_krve.py`, `15_souhrn.py`, `data/krev_*.txt`, `data/denik.csv` (smyšlená data) |
| 16 Sandbox a virtuální počítač | `16_piskoviste.py`, `16_kontejner.py`, `sandbox/agent.wsb`, `sandbox/Dockerfile` |
| 17 Modelování ve 3D | `17_openscad.py` (vyžaduje program OpenSCAD), `data/stojanek.scad` |
| 18 Agent v prohlížeči | `18_prohlizec.py`, `oznac_prvky.js`, složka `web` (ukázkový web) |
| Řešení úloh (na konci kapitol) | `reseni_*.py` |

Soubory `llm.py`, `strukturovane.py`, `nastroje.py`, `rag.py` a `zdravi.py` jsou
moduly, které ostatní programy importují. Musí být ve stejné složce jako programy.

## Programy třetí části

Některé programy potřebují další software:

- kapitola 17: modelovací program OpenSCAD (openscad.org). Ve Windows zapište
  cestu k programu do `.env`, např. `OPENSCAD=C:\Program Files\OpenSCAD\openscad.exe`.
- kapitola 18: po instalaci knihoven spusťte ještě `playwright install chromium`.
- kapitola 16: pro spouštění kódu v kontejneru Docker (ve Windows Docker Desktop),
  případně Windows Sandbox nebo VirtualBox.

Programy, které pracují se soubory na disku nebo ovládají prohlížeč, zkoušejte
nejlépe ve virtuálním počítači nebo ve Windows Sandbox (kapitola 16).

## Testovací server

Složka `test` obsahuje jednoduchý testovací server (`mock_server.py`), který
napodobuje API jazykového modelu a vrací předvídatelné odpovědi. Slouží
k ověření, že programy správně komunikují s API, když skutečný model není
k dispozici. Spuštění: `python test/mock_server.py` (poslouchá na portu 11434,
nesmí současně běžet Ollama).

Upozornění: data ve školním řádu (`data/skolni_rad.md`), rozvrh a jídelníček
v `nastroje.py`, laboratorní zprávy a deník v kapitole 15 i ubytování na
ukázkovém webu jsou smyšlená a slouží jen pro ukázku. Programy z kapitoly 15
nenahrazují lékaře.
