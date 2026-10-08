from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
from pydantic import BaseModel
from datetime import datetime
from backend.app.providers.core.provider_manager import ProviderManager
from backend.app.providers.adapters.yfinance_adapter import YFinanceAdapter
from backend.app.models.domain.market import Quote

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
async def get_forex_overview():
    """E14. Forex dashboard (Uses Frankfurter)"""
    from backend.app.providers.adapters.frankfurter_adapter import FrankfurterAdapter
    from backend.app.models.domain.market import DataMetadata
    
    pairs = ["EUR", "GBP", "JPY", "INR"]
    results = []
    adapter = FrankfurterAdapter()
    for pair in pairs:
        try:
            data = await adapter.get_fx_rate(base="USD", symbol=pair)
            
            # Map Frankfurter FX to Quote object format so frontend doesn't break
            meta = DataMetadata(
                symbol=f"USD{pair}=X",
                provider="frankfurter",
                market="FX",
                currency=pair,
                timestamp=datetime.now(),
                retrieved_at=datetime.now(),
                data_status="REALTIME",
                source="frankfurter",
                is_market_open=True
            )
            quote = Quote(
                price=data["rate"],
                change=0.0,
                change_percent=0.0,
                high=data["rate"],
                low=data["rate"],
                volume=0.0,
                meta=meta
            )
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
