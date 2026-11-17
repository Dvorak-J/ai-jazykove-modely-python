# Filtr spamu založený na ručně napsaných pravidlech

PODEZRELA_SLOVA = ["výhra", "zdarma", "klikněte", "bitcoin", "ihned", "vyhrál"]


def je_spam(text):
    """Zpráva je spam, pokud obsahuje aspoň dvě podezřelá slova."""
    text = text.lower()
    pocet = 0
    for slovo in PODEZRELA_SLOVA:
        if slovo in text:
            pocet += 1
    return pocet >= 2


zpravy = [
    "Gratulujeme, vyhrál jste iPhone ZDARMA! Klikněte ihned.",
    "Ahoj, zítra nezapomeň na písemku z matiky.",
    "Získejte bitcoin zdarma, stačí kliknout.",
    "V-Ý-H-R-A! Z.d.a.r.m.a. iPhone jen pro tebe!",
    "Zdarma ti pošlu poznámky, výhra v soutěži mi nevadí :)",
]

for zprava in zpravy:
    oznaceni = "SPAM" if je_spam(zprava) else "ok  "
    print(oznaceni, "|", zprava)
