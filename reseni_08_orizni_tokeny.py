# Řešení: omezení historie podle odhadovaného počtu tokenů

ZNAKU_NA_TOKEN = 3  # hrubý odhad pro češtinu


def odhad_tokenu(zpravy):
    return sum(len(z["content"] or "") for z in zpravy) // ZNAKU_NA_TOKEN


def orizni_podle_tokenu(zpravy, limit=3000):
    """Ponechá systémovou zprávu a odebírá nejstarší zprávy, dokud se
    konverzace nevejde do limitu. Poslední zprávu (aktuální otázku) nikdy
    neodebere."""
    system, zbytek = zpravy[:1], list(zpravy[1:])
    while len(zbytek) > 1 and odhad_tokenu(system + zbytek) > limit:
        zbytek.pop(0)
    return system + zbytek


if __name__ == "__main__":
    konverzace = [{"role": "system", "content": "Jsi ŠkolBot." * 10}]
    for i in range(30):
        konverzace.append({"role": "user", "content": f"Otázka {i} " + "slovo " * 40})
        konverzace.append({"role": "assistant", "content": f"Odpověď {i} " + "slovo " * 80})
    kratsi = orizni_podle_tokenu(konverzace, limit=3000)
    print(f"Původně {len(konverzace)} zpráv (~{odhad_tokenu(konverzace)} tokenů), "
          f"po oříznutí {len(kratsi)} zpráv (~{odhad_tokenu(kratsi)} tokenů)")
