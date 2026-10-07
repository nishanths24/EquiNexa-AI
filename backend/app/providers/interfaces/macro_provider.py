from abc import ABC, abstractmethod
from typing import List

class MacroProvider(ABC):
    @property
    @abstractmethod
    def provider_name(self) -> str:
        pass
        
    @abstractmethod
    async def get_indicator(self, indicator_code: str) -> dict:
        pass
        
    @abstractmethod
    async def get_yield_curve(self) -> dict:
        pass
