import httpx
import os
from datetime import datetime
from typing import List
from backend.app.models.domain.market import Quote, OHLCV, DataMetadata, MarketStatus
from backend.app.providers.interfaces.market_provider import MarketDataProvider

class AlphaVantageAdapter(MarketDataProvider):
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("ALPHAVANTAGE_API_KEY", "")
        self.base_url = "https://www.alphavantage.co/query"

    @property
    def provider_name(self) -> str:
        return "alphavantage"

    async def capabilities(self) -> dict:
        return {
            "supports_realtime": False,
            "supports_delayed": True,
            "supports_public_display": False,
            "supports_commercial_use": False
        }

    async def quote(self, symbol: str) -> Quote:
        async with httpx.AsyncClient() as client:
            resp = await client.get(self.base_url, params={
                "function": "GLOBAL_QUOTE",
                "symbol": symbol,
                "apikey": self.api_key
            })
            resp.raise_for_status()
            data = resp.json()
            
            if "Global Quote" not in data or not data["Global Quote"]:
                raise ValueError(f"AlphaVantage Error: {data.get('Note', data)}")
            
            quote_data = data["Global Quote"]
            price = float(quote_data.get("05. price", 0.0))
            change = float(quote_data.get("09. change", 0.0))
            change_percent = float(quote_data.get("10. change percent", "0%").strip('%'))
            
            meta = DataMetadata(
                symbol=symbol,
                provider=self.provider_name,
                market="UNKNOWN",
                currency="USD",
                timestamp=datetime.now(),
                retrieved_at=datetime.now(),
                data_status="DELAYED",
                source="alphavantage",
                is_market_open=False
            )
            
            return Quote(
                price=price,
                change=change,
                change_percent=change_percent,
                high=float(quote_data.get("03. high", price)),
                low=float(quote_data.get("04. low", price)),
                volume=float(quote_data.get("06. volume", 0)),
                meta=meta
            )

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
            meta=DataMetadata(symbol=market, provider=self.provider_name, market=market, currency="USD", timestamp=datetime.now(), retrieved_at=datetime.now(), data_status="DELAYED", source="alphavantage", is_market_open=False))
