# Zkrácení dlouhé konverzace pomocí shrnutí starších zpráv
from llm import MODEL, klient

PONECHAT = 6  # kolik posledních zpráv necháme beze změny


def zkrat_historii(zpravy):
    """Starší zprávy nahradí jejich shrnutím. Systémovou zprávu
    a posledních PONECHAT zpráv zachová."""
    system, starsi, nove = zpravy[0], zpravy[1:-PONECHAT], zpravy[-PONECHAT:]
    if not starsi:
        return zpravy
    prepis = "\n".join(f"{z['role']}: {z['content']}" for z in starsi)
    odpoved = klient.chat.completions.create(
        model=MODEL,
        temperature=0,
        messages=[{
            "role": "user",
            "content": "Shrň následující část rozhovoru do nejvýše pěti odrážek. "
                       "Zachovej fakta o uživateli (jméno, třída, plány) "
                       "a důležité dohody.\n\n" + prepis,
        }],
    )
    shrnuti = odpoved.choices[0].message.content
    # shrnutí připojíme k systémové zprávě (některá API nedovolují víc systémových zpráv)
    novy_system = {
        "role": "system",
        "content": system["content"] + "\n\nShrnutí dřívější části rozhovoru:\n" + shrnuti,
    }
    return [novy_system] + nove


if __name__ == "__main__":
    konverzace = [{"role": "system", "content": "Jsi ŠkolBot."}]
    for i in range(5):
        konverzace.append({"role": "user", "content": f"Otázka číslo {i + 1}"})
        konverzace.append({"role": "assistant", "content": f"Odpověď číslo {i + 1}"})
    kratsi = zkrat_historii(konverzace)
    print(f"Před zkrácením: {len(konverzace)} zpráv, po zkrácení: {len(kratsi)} zpráv")
    print(kratsi[0]["content"])
