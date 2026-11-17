# Slovníky v Pythonu

Slovník (dict) ukládá dvojice klíč–hodnota. Zapisuje se do složených závorek:
znamky = {"matematika": 2, "čeština": 1}.

K hodnotě se dostaneme přes klíč: znamky["matematika"] vrátí 2. Pokud klíč
neexistuje, Python vyvolá výjimku KeyError. Bezpečnější je metoda get:
znamky.get("fyzika") vrátí None, znamky.get("fyzika", 0) vrátí 0.

Novou dvojici přidáme přiřazením: znamky["fyzika"] = 3. Stejným zápisem
změníme hodnotu existujícího klíče. Dvojici odstraníme příkazem del znamky["fyzika"].

Klíčem může být jen neměnitelný typ: řetězec, číslo nebo n-tice. Seznam klíčem
být nemůže. Hodnotou může být cokoli, i další slovník nebo seznam.

Cyklus for prochází klíče: for predmet in znamky. Metoda items() vrací dvojice:
for predmet, znamka in znamky.items(). Metoda keys() vrací klíče, values() hodnoty.

Operátor in zjistí, zda slovník obsahuje klíč: "matematika" in znamky.
Funkce len vrátí počet dvojic. Od Pythonu 3.7 si slovník pamatuje pořadí,
v jakém byly klíče vloženy.
