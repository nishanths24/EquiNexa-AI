from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from backend.app.providers.adapters.finnhub_adapter import FinnhubAdapter

router = APIRouter()

def get_news_provider() -> FinnhubAdapter:
    return FinnhubAdapter()

@router.get("/news/global", summary="Get Real-time Global and Business News")
async def get_global_news(
    category: str = Query("general", description="News category: general, forex, crypto, merger"),
    limit: int = Query(20, description="Number of articles to fetch")
):
    """
    Retrieves global news from Finnhub, used to populate the platform's news timeline.
    """
    provider = get_news_provider()
    try:
        news = await provider.get_news(category=category, limit=limit)
        return {"status": "ok", "count": len(news), "articles": news}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/news/company/{symbol}", summary="Get Company-Specific News")
async def get_company_news(
    symbol: str,
    limit: int = Query(10, description="Number of articles to fetch")
):
    """
    Retrieves news specifically related to a stock symbol (BSE/NSE/Global) 
    for the fundamental analysis view.
    """
    provider = get_news_provider()
    try:
        news = await provider.get_company_news(symbol=symbol, limit=limit)
        return {"symbol": symbol, "count": len(news), "articles": news}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
