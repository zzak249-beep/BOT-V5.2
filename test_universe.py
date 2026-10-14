"""
Prueba sin red de universe.py y de su integración con bingx.load_contracts.
  python test_universe.py
"""
from universe import classify, is_tradfi, pretty

casos = {
    "BTC-USDT": ("cripto", "crypto"), "1000PEPE-USDT": ("cripto", "crypto"),
    "NCT-USDT": ("cripto", "crypto"),                       # cripto que empieza por NC: NO es TradFi
    "NCFXEUR2USD-USDT": ("forex", "forex"), "NCFXUSD2ILS-USDT": ("forex", "forex"),
    "NCSKDELL2USD-USDT": ("acción", "stock"), "NCCOGOLD2USD-USDT": ("materia prima", "commodity"),
    "NCSINASDAQ1002USD-USDT": ("índice", "index"), "NCXXABC2USD-USDT": ("TradFi", "tradfi"),
}
for sym, esperado in casos.items():
    assert classify(sym) == esperado, (sym, classify(sym), esperado)
assert not is_tradfi("NCT-USDT") and not is_tradfi("BTC-USDT") and is_tradfi("NCSKDELL2USD-USDT")
assert pretty("NCFXEUR2USD-USDT") == "EUR/USD" and pretty("NCSKDELL2USD-USDT") == "DELL" and pretty("BTC-USDT") == "BTC"
print("1 OK clasificación y nombres")

import bingx
ex = bingx.BingX("k", "s")
ex._req = lambda *a, **k: [
    {"symbol": "BTC-USDT", "status": 1, "pricePrecision": 1, "quantityPrecision": 4, "tradeMinQuantity": 0.0001, "tradeMinUSDT": 2},
    {"symbol": "NCFXEUR2USD-USDT", "status": 1, "pricePrecision": 5, "quantityPrecision": 1, "apiStateOpen": "true"},
    {"symbol": "OLD-USDT", "status": 0},
    {"symbol": "BTC-USD", "status": 1},
]
c = ex.load_contracts()
assert set(c) == {"BTC-USDT", "NCFXEUR2USD-USDT"}, set(c)
assert c["BTC-USDT"]["cls"] == "crypto" and c["NCFXEUR2USD-USDT"]["cls"] == "forex"
assert c["NCFXEUR2USD-USDT"]["name"] == "EUR/USD" and c["NCFXEUR2USD-USDT"]["cls_label"] == "forex"
print("2 OK integración con load_contracts")
print("TODO OK")
