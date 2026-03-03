from datetime import datetime, timedelta
import requests

BASE = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata"


def _get_json(url: str) -> dict:
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    return r.json()


def get_dolar_ptax_for_date(date: datetime) -> dict:
    date_str = date.strftime("%m-%d-%Y")
    url = f"{BASE}/CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao='{date_str}'&$format=json"
    data = _get_json(url)
    values = data.get("value", [])
    if not values:
        return {"error": "no_data_for_date", "date": date_str}
    row = values[0]
    return {
        "label": "USD/BRL",
        "rate": row.get("cotacaoVenda"),
        "as_of": date_str,
        "timestamp": row.get("dataHoraCotacao"),
        "source": "BCB PTAX",
        "extras": {
        "buy": row.get("cotacaoCompra"),
        "sell": row.get("cotacaoVenda"),
    },
}

def get_currency_ptax_for_date(moeda: str, date: datetime) -> dict:
    date_str = date.strftime("%m-%d-%Y")
    url = (
        f"{BASE}/CotacaoMoedaDia(moeda=@moeda,dataCotacao=@dataCotacao)?"
        f"@moeda='{moeda}'&@dataCotacao='{date_str}'&$format=json"
    )
    data = _get_json(url)
    values = data.get("value", [])
    if not values:
        return {"error": "no_data_for_date", "date": date_str, "currency": moeda}
    row = values[0]
    return {
        "label": f"{moeda}/BRL",
        "rate": row.get("cotacaoVenda"),
        "as_of": date_str,
        "timestamp": row.get("dataHoraCotacao"),
        "source": "BCB PTAX",
        "extras": {
        "buy": row.get("cotacaoCompra"),
        "sell": row.get("cotacaoVenda"),
    },
}

def get_latest_quote(fetch_fn, max_days_back: int = 7) -> dict:
    """
    Attempts to fetch the latest available quote.
    Falls back up to `max_days_back` days if no data is available.
    """
    today = datetime.now()
    for i in range(max_days_back + 1):
        d = today - timedelta(days=i)
        result = fetch_fn(d)
        if "error" not in result:
            result["stale"] = (i != 0)
            result["days_back"] = i
            return result
    return {"error": "no_data_in_range", "checked_days": max_days_back}