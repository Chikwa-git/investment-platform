from fastapi import APIRouter
from services.market_service import (
    get_latest_quote,
    get_dolar_ptax_for_date,
    get_currency_ptax_for_date,
)

router = APIRouter(prefix="/api/market", tags=["market"])


@router.get("/summary")
def market_summary():
    usd = get_latest_quote(get_dolar_ptax_for_date)
    eur = get_latest_quote(lambda d: get_currency_ptax_for_date("EUR", d))
    return {"usd": usd, "eur": eur}