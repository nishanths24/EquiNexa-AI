from abc import ABC, abstractmethod
from typing import List

class FundamentalProvider(ABC):
    @property
    @abstractmethod
    def provider_name(self) -> str:
        pass
        
    @abstractmethod
    async def get_profile(self, symbol: str) -> dict:
        pass
        
    @abstractmethod
    async def get_financial_statements(self, symbol: str) -> dict:
        pass
        
    @abstractmethod
    async def get_valuation_metrics(self, symbol: str) -> dict:
        pass
