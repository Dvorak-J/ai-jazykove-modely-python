"""Nástroje (funkce), které může ŠkolBot používat."""
import ast
import operator
from datetime import datetime

DNY = ["pondělí", "úterý", "středa", "čtvrtek", "pátek", "sobota", "neděle"]

ROZVRH = {
    "pondělí": ["matematika", "čeština", "programování", "programování", "angličtina", "fyzika"],
    "úterý": ["angličtina", "sítě", "sítě", "matematika", "tělocvik"],
    "středa": ["databáze", "databáze", "čeština", "dějepis", "matematika", "angličtina"],
    "čtvrtek": ["programování", "elektrotechnika", "matematika", "AI a jazykové modely", "AI a jazykové modely"],
    "pátek": ["čeština", "angličtina", "hardware", "hardware"],
}

JIDELNICEK = {
    "pondělí": "kuřecí vývar; 1) svíčková, knedlík  2) zeleninové rizoto",
    "úterý": "česnečka; 1) smažený sýr, brambory  2) těstoviny s pestem",
    "středa": "hrachová; 1) guláš, chléb  2) čočkový salát",
    "čtvrtek": "rajská; 1) kuře na paprice, rýže  2) zapečené brambory",
    "pátek": "bramboračka; 1) rybí filé, bramborová kaše  2) palačinky",
}


def aktualni_cas():
    ted = datetime.now()
    return {"den": DNY[ted.weekday()], "datum": f"{ted:%d. %m. %Y}", "cas": f"{ted:%H:%M}"}


def rozvrh(den):
    hodiny = ROZVRH.get(den.lower())
    if hodiny is None:
        return {"chyba": f"Pro den '{den}' rozvrh nemám (vyučuje se pondělí až pátek)."}
    return {"den": den, "hodiny": [f"{i}. hodina: {p}" for i, p in enumerate(hodiny, 1)]}


def jidelnicek(den):
    return {"den": den, "menu": JIDELNICEK.get(den.lower(), "V tento den se nevaří.")}


def objednej_obed(den, varianta):
    """Simulace objednávky oběda (skutečně nic neobjednává)."""
    return {"stav": "objednáno", "den": den, "jidlo": JIDELNICEK.get(den, "?"), "varianta": varianta}


# Bezpečná kalkulačka: povolíme jen čísla a základní operace.
# Funkci eval() nikdy nepoužívejte na text od modelu ani od uživatele!
OPERACE = {
    ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
    ast.Div: operator.truediv, ast.Pow: operator.pow, ast.USub: operator.neg,
}


def _vyhodnot(uzel):
    if isinstance(uzel, ast.Constant) and isinstance(uzel.value, (int, float)):
        return uzel.value
    if isinstance(uzel, ast.BinOp) and type(uzel.op) in OPERACE:
        levy, pravy = _vyhodnot(uzel.left), _vyhodnot(uzel.right)
        if isinstance(uzel.op, ast.Pow) and abs(pravy) > 100:
            raise ValueError("Příliš velký exponent")  # ochrana před 9**9**9
        return OPERACE[type(uzel.op)](levy, pravy)
    if isinstance(uzel, ast.UnaryOp) and type(uzel.op) in OPERACE:
        return OPERACE[type(uzel.op)](_vyhodnot(uzel.operand))
    raise ValueError("Nepovolený výraz")


def kalkulacka(vyraz):
    try:
        vysledek = _vyhodnot(ast.parse(vyraz.replace(",", "."), mode="eval").body)
        return {"vyraz": vyraz, "vysledek": vysledek}
    except (ValueError, SyntaxError, ZeroDivisionError, OverflowError) as chyba:
        return {"chyba": f"Výraz nelze spočítat: {chyba}"}


def popis(nazev, text, parametry=None):
    """Pomocná funkce: sestaví popis nástroje ve formátu, který očekává API."""
    vlastnosti = parametry or {}
    return {"type": "function", "function": {
        "name": nazev, "description": text,
        "parameters": {"type": "object", "properties": vlastnosti,
                       "required": list(vlastnosti)},
    }}


DEN = {"type": "string", "enum": DNY[:5], "description": "den v týdnu malými písmeny"}

NASTROJE = [
    popis("aktualni_cas", "Vrátí dnešní den v týdnu, datum a aktuální čas."),
    popis("rozvrh", "Vrátí rozvrh hodin třídy 3.A pro zadaný den.", {"den": DEN}),
    popis("jidelnicek", "Vrátí jídelníček školní jídelny pro zadaný den.", {"den": DEN}),
    popis("objednej_obed", "Objedná studentovi oběd na zadaný den.",
          {"den": DEN, "varianta": {"type": "integer", "enum": [1, 2]}}),
    popis("kalkulacka", "Přesně spočítá matematický výraz, např. '(17 + 4) * 3.5'.",
          {"vyraz": {"type": "string", "description": "výraz s čísly a operátory + - * / **"}}),
]

FUNKCE = {"aktualni_cas": aktualni_cas, "rozvrh": rozvrh, "jidelnicek": jidelnicek,
          "objednej_obed": objednej_obed, "kalkulacka": kalkulacka}

# nástroje, které něco mění ve skutečném světě: před provedením se zeptáme uživatele
VYZADUJI_POTVRZENI = {"objednej_obed"}
