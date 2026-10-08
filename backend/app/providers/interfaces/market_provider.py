from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from backend.app.models.domain.market import Quote, OHLCV, MarketStatus

class MarketDataProvider(ABC):
    @property
    @abstractmethod
    def provider_name(self) -> str:
        pass
        
    @abstractmethod
    async def capabilities(self) -> dict:
        pass
        
    @abstractmethod
    async def quote(self, symbol: str) -> Quote:
        pass
        
    @abstractmethod
    async def ohlcv(self, symbol: str, timeframe: str, start: datetime, end: datetime) -> List[OHLCV]:
        pass

    @abstractmethod
    async def intraday(self, symbol: str) -> List[OHLCV]:
        pass

    @abstractmethod
    async def historical(self, symbol: str) -> List[OHLCV]:
        pass

    @abstractmethod
    async def search_symbols(self, query: str) -> List[dict]:
        pass

    @abstractmethod
    async def company_profile(self, symbol: str) -> dict:
        pass

    @abstractmethod
    async def fundamentals(self, symbol: str) -> dict:
        pass

    @abstractmethod
    async def corporate_events(self, symbol: str) -> List[dict]:
        pass

    @abstractmethod
    async def forex(self, pair: str) -> Quote:
        pass

    @abstractmethod
    async def indices(self, index_symbol: str) -> Quote:
        pass

    @abstractmethod
    async def market_status(self, market: str) -> MarketStatus:
        pass
