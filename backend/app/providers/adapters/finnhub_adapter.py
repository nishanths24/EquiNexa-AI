import httpx
import os
from datetime import datetime
from typing import List, Dict, Any
from backend.app.providers.interfaces.news_provider import NewsProvider
from backend.app.providers.interfaces.fundamental_provider import FundamentalProvider
from backend.app.providers.core.circuit_breaker import CircuitBreakerOpenException

class FinnhubAdapter(NewsProvider, FundamentalProvider):
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("FINNHUB_API_KEY", "")
        self.base_url = "https://finnhub.io/api/v1"

    @property
    def provider_name(self) -> str:
        return "finnhub"

    async def get_news(self, category: str = "general", limit: int = 10) -> List[dict]:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{self.base_url}/news", params={"category": category, "token": self.api_key})
            resp.raise_for_status()
            data = resp.json()
            return data[:limit] if isinstance(data, list) else []

    async def get_company_news(self, symbol: str, limit: int = 10) -> List[dict]:
        from datetime import timedelta
        # Finnhub requires from/to dates for company news
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{self.base_url}/company-news", params={
                "symbol": symbol, 
                "from": start_date.strftime('%Y-%m-%d'),
                "to": end_date.strftime('%Y-%m-%d'),
                "token": self.api_key
            })
            resp.raise_for_status()
            data = resp.json()
            return data[:limit] if isinstance(data, list) else []

    async def get_company_profile(self, symbol: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{self.base_url}/stock/profile2", params={"symbol": symbol, "token": self.api_key})
            resp.raise_for_status()
            return resp.json()

    async def get_basic_financials(self, symbol: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{self.base_url}/stock/metric", params={"symbol": symbol, "metric": "all", "token": self.api_key})
            resp.raise_for_status()
            return resp.json()
