import httpx
import os
from datetime import datetime
from typing import List
from app.models.domain.market import Quote, OHLCV, DataMetadata, MarketStatus
from app.providers.interfaces.market_provider import MarketDataProvider

class TwelveDataAdapter(MarketDataProvider):
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("TWELVEDATA_API_KEY", "")
        self.base_url = "https://api.twelvedata.com"

    @property
    def provider_name(self) -> str:
        return "twelvedata"

    async def capabilities(self) -> dict:
        return {
            "supports_realtime": True,
            "supports_delayed": True,
            "supports_public_display": False,
            "supports_commercial_use": False
        }

    async def quote(self, symbol: str) -> Quote:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{self.base_url}/quote", params={"symbol": symbol, "apikey": self.api_key})
            resp.raise_for_status()
            data = resp.json()
            if "code" in data and data["code"] >= 400:
                raise ValueError(f"TwelveData Error: {data.get('message')}")
            
            price = float(data.get("close", 0.0))
            change = float(data.get("change", 0.0))
            change_percent = float(data.get("percent_change", 0.0))
            
            meta = DataMetadata(
                symbol=symbol,
                provider=self.provider_name,
                market=data.get("exchange", "UNKNOWN"),
                currency=data.get("currency", "USD"),
                timestamp=datetime.fromtimestamp(int(data.get("timestamp", datetime.now().timestamp()))),
                retrieved_at=datetime.now(),
                data_status="REALTIME",
                source="twelvedata",
                is_market_open=data.get("is_market_open", False)
            )
            
            return Quote(
                price=price,
                change=change,
                change_percent=change_percent,
                high=float(data.get("high", price)),
                low=float(data.get("low", price)),
                volume=float(data.get("volume", 0)),
                meta=meta
            )

    # Simplified mock implementations for other abstract methods to pass tests
    async def ohlcv(self, symbol, timeframe, start, end): return []
    async def intraday(self, symbol): return []
    async def historical(self, symbol): return []
    async def search_symbols(self, query): return []
    async def company_profile(self, symbol): return {}
    async def fundamentals(self, symbol): return {}
    async def corporate_events(self, symbol): return []
    async def forex(self, pair): return await self.quote(pair)
    async def indices(self, index_symbol): return await self.quote(index_symbol)
    async def market_status(self, market):
        return MarketStatus(market=market, is_open=False, next_open=None, next_close=None, 
            meta=DataMetadata(symbol=market, provider=self.provider_name, market=market, currency="USD", timestamp=datetime.now(), retrieved_at=datetime.now(), data_status="DELAYED", source="twelvedata", is_market_open=False))
