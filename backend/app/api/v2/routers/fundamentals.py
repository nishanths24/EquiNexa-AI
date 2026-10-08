from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from backend.app.providers.adapters.finnhub_adapter import FinnhubAdapter

router = APIRouter()

def get_fundamental_provider() -> FinnhubAdapter:
    return FinnhubAdapter()

@router.get("/fundamentals/{symbol}/profile", summary="Get Company Profile")
async def get_company_profile(symbol: str):
    """
    Retrieves static company profile data (industry, market cap, website) 
    for fundamental analysis views beneath the stock chart.
    """
    provider = get_fundamental_provider()
    try:
        data = await provider.get_company_profile(symbol)
        return {"symbol": symbol, "profile": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/fundamentals/{symbol}/metrics", summary="Get Basic Financials")
async def get_basic_financials(symbol: str):
    """
    Retrieves trailing valuation ratios and basic financials 
    for fundamental analysis.
    """
    provider = get_fundamental_provider()
    try:
        data = await provider.get_basic_financials(symbol)
        return {"symbol": symbol, "metrics": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
