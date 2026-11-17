# Učení modelu y = w * x + b metodou gradientního sestupu
# Data: kolik hodin se student připravoval (x) a kolik bodů získal (y).
# Data jsou smyšlená, slouží jen pro ukázku.

hodiny = [1, 2, 3, 4, 5, 6, 7, 8]
body = [12, 19, 31, 38, 52, 57, 68, 79]

w = 0.0        # sklon přímky (váha)
b = 0.0        # posun přímky (bias)
krok = 0.01    # učící krok (learning rate)
n = len(hodiny)

for epocha in range(2001):
    # 1) spočítáme, jak moc se odchylujeme (střední kvadratická chyba)
    chyba = 0.0
    grad_w = 0.0
    grad_b = 0.0
    for x, y in zip(hodiny, body):
        predpoved = w * x + b
        rozdil = predpoved - y
        chyba += rozdil ** 2
        # 2) jakým směrem upravit w a b, aby chyba klesla
        grad_w += 2 * rozdil * x
        grad_b += 2 * rozdil
    chyba /= n
    grad_w /= n
    grad_b /= n

    # 3) uděláme malý krok proti směru růstu chyby
    w -= krok * grad_w
    b -= krok * grad_b

    if epocha in (0, 1, 2, 5, 10, 100, 500, 1000, 2000):
        print(f"epocha {epocha:4d}: chyba = {chyba:8.2f}, w = {w:5.2f}, b = {b:5.2f}")

print()
print(f"Naučený model: body = {w:.2f} * hodiny + {b:.2f}")
for nove_hodiny in [2.5, 10]:
    print(f"Odhad pro {nove_hodiny} h přípravy: {w * nove_hodiny + b:.0f} bodů")
