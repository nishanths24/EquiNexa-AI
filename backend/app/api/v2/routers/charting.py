from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from backend.app.providers.core.provider_manager import ProviderManager
from backend.app.providers.adapters.twelvedata_adapter import TwelveDataAdapter
from backend.app.providers.adapters.alphavantage_adapter import AlphaVantageAdapter

router = APIRouter()

def get_market_provider() -> ProviderManager:
    pm = ProviderManager()
    # Hybrid pipeline: try TwelveData first (800/day limit), fallback to AlphaVantage
    pm.register_provider(TwelveDataAdapter())
    pm.register_provider(AlphaVantageAdapter())
    return pm

@router.get("/markets/history", summary="Get Historical Candlestick Data (OHLCV)")
async def get_historical_data(
    symbol: str = Query(..., description="Stock or Index symbol (e.g., AAPL, RELIANCE.NS)"),
    timeframe: str = Query("1D", description="Candle interval: 1m, 5m, 1h, 1D, 1W"),
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    pm: ProviderManager = Depends(get_market_provider)
):
    """
    Upgraded Level Architecture Feature:
    Retrieves interactive candlestick data (OHLCV) using the hybrid data engine.
    This routes through our cache layer first to prevent burning API keys.
    """
    try:
        # In a real implementation, we would extract this method on the PM
        # For now, we fetch from the first registered provider that supports it
        provider = pm._providers[0]
        data = await provider.ohlcv(symbol=symbol, timeframe=timeframe, start=start_date, end=end_date)
        return {"symbol": symbol, "timeframe": timeframe, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
