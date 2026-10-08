import httpx
from datetime import datetime
from backend.app.models.domain.market import Quote, DataMetadata
from backend.app.providers.interfaces.macro_provider import MacroProvider

class FrankfurterAdapter(MacroProvider):
    """
    Adapter for the free open-source Frankfurter FX API (European Central Bank data).
    Provides unlimited daily and historical FX rates without API keys.
    """
    def __init__(self):
        self.base_url = "https://api.frankfurter.app"

    @property
    def provider_name(self) -> str:
        return "frankfurter"

    async def get_fx_rate(self, base: str = "USD", symbol: str = "EUR") -> dict:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{self.base_url}/latest", params={"from": base, "to": symbol})
            resp.raise_for_status()
            data = resp.json()
            
            rate = data["rates"].get(symbol, 0.0)
            return {
                "base": base,
                "symbol": symbol,
                "rate": rate,
                "date": data.get("date"),
                "provider": self.provider_name
            }

    async def get_historical_fx(self, start_date: str, end_date: str, base: str = "USD", symbol: str = "EUR") -> dict:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{self.base_url}/{start_date}..{end_date}", params={"from": base, "to": symbol})
            resp.raise_for_status()
            return resp.json()

    async def get_indicator(self, indicator_code: str) -> dict:
        # Not applicable for Frankfurter (FX only), mock or raise NotImplementedError
        return {}

    async def get_yield_curve(self) -> dict:
        # Not applicable for Frankfurter (FX only)
        return {}
