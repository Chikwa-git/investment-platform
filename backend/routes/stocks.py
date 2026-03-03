from fastapi import APIRouter, Query
from services.stocks_service import search_stocks, get_stock_quote

router = APIRouter(prefix="/api/stocks", tags=["stocks"])

@router.get("/search")
def search(q: str = Query(..., min_length=2), limit: int = 6):
    return {"items": search_stocks(q, limit=limit)}

@router.get("/quote")
def quote(ticker: str = Query(..., min_length=2)):
    return get_stock_quote(ticker)