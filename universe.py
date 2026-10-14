"""Clasificación de los perpetuos de BingX (RECONSTRUIDO: si tu repo ya tiene un universe.py propio y ajustado, conserva el tuyo).

Contrato que usa el bot:
    classify(symbol) -> (etiqueta, clave)   clave ∈ crypto | forex | commodity | stock | index | tradfi
    pretty(symbol)   -> nombre legible
    is_tradfi(symbol)-> True si NO es cripto

Los perpetuos TradFi de BingX tienen la forma  NC<TIPO><ACTIVO>2<DIVISA>-USDT :
    NCFXEUR2USD-USDT (forex) · NCSKDELL2USD-USDT (acción) · NCCOGOLD2USD-USDT (materia prima) · NCSI…2USD-USDT (índice)
El patrón es estricto a propósito: una cripto como NCT-USDT empieza por «NC» y NO debe tratarse como TradFi.
"""
import re

_TRADFI = re.compile(r"^NC([A-Z]{2})(.+)2([A-Z]{3})-USDT$")

_KINDS = {
    "FX": ("forex", "forex"),
    "CO": ("materia prima", "commodity"),
    "SK": ("acción", "stock"),
    "SI": ("índice", "index"),
}


def _parts(symbol):
    m = _TRADFI.match((symbol or "").upper())
    return m.groups() if m else None


def classify(symbol):
    p = _parts(symbol)
    if not p:
        return "cripto", "crypto"
    return _KINDS.get(p[0], ("TradFi", "tradfi"))


def pretty(symbol):
    s = (symbol or "").upper()
    p = _parts(s)
    if not p:
        return s[:-5] if s.endswith("-USDT") else s
    kind, asset, quote = p
    return f"{asset}/{quote}" if kind == "FX" else asset


def is_tradfi(symbol):
    return classify(symbol)[1] != "crypto"
