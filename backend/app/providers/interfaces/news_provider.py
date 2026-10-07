from abc import ABC, abstractmethod
from typing import List

class NewsProvider(ABC):
    @property
    @abstractmethod
    def provider_name(self) -> str:
        pass
        
    @abstractmethod
    async def get_news(self, category: str = "general", limit: int = 10) -> List[dict]:
        pass
        
    @abstractmethod
    async def get_company_news(self, symbol: str, limit: int = 10) -> List[dict]:
        pass
