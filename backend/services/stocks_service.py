import time
from typing import List, Dict, Any, Optional
import requests


# MVP dataset (cresce depois)
_STOCKS: List[Dict[str, str]] = [
    {"ticker": "PETR4", "name": "Petrobras PN"},
    {"ticker": "PETR3", "name": "Petrobras ON"},
    {"ticker": "VALE3", "name": "Vale ON"},
    {"ticker": "ITUB4", "name": "Itaú Unibanco PN"},
    {"ticker": "BBDC4", "name": "Bradesco PN"},
    {"ticker": "ABEV3", "name": "Ambev ON"},
    {"ticker": "WEGE3", "name": "WEG ON"},
    {"ticker": "BBAS3", "name": "Banco do Brasil ON"},
    {"ticker": "B3SA3", "name": "B3 ON"},
    {"ticker": "MGLU3", "name": "Magazine Luiza ON"},
    {"ticker": "SUZB3", "name": "Suzano ON"},
    {"ticker": "GGBR4", "name": "Gerdau PN"},
]


def search_stocks(query: str, limit: int = 6) -> List[Dict[str, str]]:
    q = (query or "").strip().upper()
    if len(q) < 2:
        return []

    results = []
    for item in _STOCKS:
        ticker = item["ticker"].upper()
        name = item["name"].upper()

        if q in ticker or q in name:
            results.append(item)

    # prioridade: ticker começa com a query
    results.sort(key=lambda x: (0 if x["ticker"].upper().startswith(q) else 1, x["ticker"]))
    return results[:limit]

import time
from typing import Dict, Any, Optional
import requests


_YAHOO_QUOTE_URL = "https://query1.finance.yahoo.com/v7/finance/quote"
_YAHOO_CHART_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"


def _to_yahoo_symbol(ticker: str) -> str:
    """
    MVP: assume ações BR (B3) -> sufixo .SA.
    - PETR4 => PETR4.SA
    - VALE3.SA => VALE3.SA
    - ^BVSP, USD/BRL etc: se já tiver caractere especial ou '.', não mexe.
    """
    t = (ticker or "").strip().upper()
    if not t:
        return t

    if "." in t or "=" in t or "^" in t:
        return t

    # B3 default
    return f"{t}.SA"


def _yahoo_headers() -> Dict[str, str]:
    return {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json,text/plain,*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
    }


def get_stock_quote(ticker: str) -> Dict[str, Any]:
    """
    Returns a neutral quote payload for one symbol.
    Tries v7 quote endpoint first, then falls back to v8 chart meta.
    """
    symbol = _to_yahoo_symbol(ticker)
    if not symbol:
        return {"ok": False, "error": "ticker_required"}

    # 1) Try v7 quote
    try:
        params = {
            "symbols": symbol,
            "formatted": "false",
            # fields are optional; keeping formatted=false reduces noise
        }
        r = requests.get(_YAHOO_QUOTE_URL, params=params, headers=_yahoo_headers(), timeout=8)
        if r.ok:
            data = r.json()
            result = (data.get("quoteResponse", {}) or {}).get("result", []) or []
            if result:
                q = result[0]
                return {
                    "ok": True,
                    "ticker": ticker.upper(),
                    "symbol": q.get("symbol"),
                    "name": q.get("shortName") or q.get("longName") or q.get("displayName"),
                    "currency": q.get("currency") or q.get("financialCurrency"),
                    "price": q.get("regularMarketPrice"),
                    "change": q.get("regularMarketChange"),
                    "change_percent": q.get("regularMarketChangePercent"),
                    "market_time": q.get("regularMarketTime"),
                    "market_state": q.get("marketState"),
                    "source": "yahoo_v7_quote",
                    "fetched_at": int(time.time()),
                }
        # if not ok or empty, fall through to chart
    except Exception:
        pass

    # 2) Fallback v8 chart (often works when quote blocks)
    try:
        url = _YAHOO_CHART_URL.format(symbol=symbol)
        params = {"interval": "1d", "range": "1d"}
        r = requests.get(url, params=params, headers=_yahoo_headers(), timeout=8)
        if r.ok:
            data = r.json()
            chart = (data.get("chart") or {})
            err = chart.get("error")
            if err:
                return {"ok": False, "error": "yahoo_error", "details": err}

            result = (chart.get("result") or [])
            if result:
                meta = (result[0].get("meta") or {})
                price = meta.get("regularMarketPrice")
                prev = meta.get("previousClose")
                change = None
                change_pct = None
                if isinstance(price, (int, float)) and isinstance(prev, (int, float)) and prev != 0:
                    change = price - prev
                    change_pct = (change / prev) * 100.0

                return {
                    "ok": True,
                    "ticker": ticker.upper(),
                    "symbol": meta.get("symbol") or symbol,
                    "name": meta.get("shortName") or meta.get("longName"),
                    "currency": meta.get("currency"),
                    "price": price,
                    "change": change,
                    "change_percent": change_pct,
                    "market_time": meta.get("regularMarketTime"),
                    "market_state": meta.get("marketState"),
                    "exchange": meta.get("exchangeName"),
                    "source": "yahoo_v8_chart",
                    "fetched_at": int(time.time()),
                }
    except Exception:
        pass

    return {"ok": False, "error": "quote_unavailable", "symbol": symbol}