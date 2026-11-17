# Řešení: výběr dalšího slova metodou top-k
import random
from collections import Counter


def vyber_top_k(pocty, k):
    """Vybere náhodně jedno z k nejčastějších slov (podle jejich četnosti)."""
    nejcastejsi = pocty.most_common(k)            # seznam dvojic (slovo, počet)
    slova = [slovo for slovo, _ in nejcastejsi]
    vahy = [pocet for _, pocet in nejcastejsi]
    return random.choices(slova, weights=vahy)[0]


if __name__ == "__main__":
    po_tecce = Counter({"kočka": 4, "když": 3, "ve": 2, "náš": 2, "robot": 2, "data": 1})
    for k in (1, 3, 6):
        vyber = Counter(vyber_top_k(po_tecce, k) for _ in range(1000))
        print(f"k = {k}: {dict(vyber)}")
