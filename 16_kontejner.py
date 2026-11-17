# Spuštění skriptu v kontejneru Dockeru: bez sítě a jen se složkou pískoviště.
# Vyžaduje nainstalovaný Docker (ve Windows Docker Desktop).
import os
import shutil
import subprocess
import uuid
from pathlib import Path

PISKOVISTE = (Path(__file__).parent / "piskoviste").resolve()
OBRAZ = os.getenv("DOCKER_OBRAZ", "python:3.12-slim")


def spust_v_kontejneru(nazev, limit=30):
    if shutil.which("docker") is None:
        return {"chyba": "Docker není nainstalovaný."}
    if Path(nazev).name != nazev or not (PISKOVISTE / nazev).is_file():
        return {"chyba": "Zadejte jméno existujícího souboru v pracovní složce."}
    jmeno = f"agent-{uuid.uuid4().hex[:8]}"
    prikaz = ["docker", "run", "--rm", "--name", jmeno,
              "--network", "none",                     # žádná síť
              "--read-only", "--tmpfs", "/tmp",        # systém kontejneru jen pro čtení
              "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
              "--memory", "512m", "--cpus", "1", "--pids-limit", "100",
              "-v", f"{PISKOVISTE}:/prace", "-w", "/prace",
              OBRAZ, "python", "-I", nazev]
    if os.name == "posix":            # Linux a macOS: soubory vznikají pod naším uživatelem
        prikaz[3:3] = ["--user", f"{os.getuid()}:{os.getgid()}"]
    try:
        v = subprocess.run(prikaz, capture_output=True, text=True, timeout=limit)
    except subprocess.TimeoutExpired:
        subprocess.run(["docker", "kill", jmeno], capture_output=True)
        return {"chyba": f"Program běžel déle než {limit} s a byl ukončen."}
    return {"kod": v.returncode, "vystup": v.stdout[-2000:], "chyby": v.stderr[-2000:]}


if __name__ == "__main__":
    PISKOVISTE.mkdir(exist_ok=True)
    (PISKOVISTE / "test_izolace.py").write_text(
        "import os, urllib.request\n"
        "print('Kořen systému:', sorted(os.listdir('/'))[:6])\n"
        "try:\n"
        "    urllib.request.urlopen('https://example.com', timeout=3)\n"
        "except OSError as chyba:\n"
        "    print('Síť:', type(chyba).__name__)\n"
        "try:\n"
        "    open('/etc/neco.txt', 'w')\n"
        "except OSError as chyba:\n"
        "    print('Zápis mimo složku:', chyba.strerror)\n", encoding="utf-8")
    print(spust_v_kontejneru("test_izolace.py"))
    print(spust_v_kontejneru("../llm.py"))
