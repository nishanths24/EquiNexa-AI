from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
from pydantic import BaseModel
from app.providers.core.provider_manager import ProviderManager
from app.providers.adapters.yfinance_adapter import YFinanceAdapter
from app.models.domain.market import Quote

router = APIRouter()

# Dependency injection
def get_provider_manager() -> ProviderManager:
    pm = ProviderManager()
    # For Phase 4, we use the yfinance adapter as a functional stub. 
    # Real adapters require API keys configured via env.
    pm.register_provider(YFinanceAdapter())
    return pm

@router.get("/markets/overview", response_model=Dict[str, List[Quote]])
async def get_market_overview(pm: ProviderManager = Depends(get_provider_manager)):
    """E1. Market overview: Indices by region"""
    regions = {
        "India": ["^NSEI", "^NSEBANK"],
        "USA": ["^GSPC", "^IXIC", "^DJI"],
        "Europe": ["^FTSE", "^GDAXI"],
        "Asia": ["^N225", "^HSI"],
        "Global": ["DX-Y.NYB", "GC=F", "CL=F"]
    }
    
    result = {}
    for region, symbols in regions.items():
        region_quotes = []
        for sym in symbols:
            try:
                # This naturally validates "UNAVAILABLE" states if provider fails
                quote = await pm.get_quote(sym)
                region_quotes.append(quote)
            except Exception:
                # Omit unavailable symbols
                pass
        result[region] = region_quotes
        
    return result

@router.get("/markets/forex", response_model=List[Quote])
async def get_forex_overview(pm: ProviderManager = Depends(get_provider_manager)):
    """E14. Forex dashboard"""
    pairs = ["EURUSD=X", "GBPUSD=X", "USDJPY=X", "INR=X"]
    results = []
    for pair in pairs:
        try:
            quote = await pm.get_quote(pair)
            results.append(quote)
        except:
            pass
    return results

@router.get("/markets/macro", response_model=List[Quote])
async def get_macro_overview(pm: ProviderManager = Depends(get_provider_manager)):
    """E15. Macro dashboard"""
    macros = ["DX-Y.NYB", "^TNX", "GC=F", "CL=F"]
    results = []
    for m in macros:
        try:
            quote = await pm.get_quote(m)
            results.append(quote)
        except:
            pass
    return results
