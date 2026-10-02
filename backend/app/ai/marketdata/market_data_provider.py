from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime
import pandas as pd

class PriceFrame(pd.DataFrame):
    # A pandas DataFrame with columns: [ts_utc, ts_local, open, high, low, close, volume]
    pass

class MarketDataProvider(ABC):
    @abstractmethod
    def fetch_ohlcv(self, symbol: str, start: datetime, end: datetime, interval: str = '1d') -> PriceFrame:
        pass
    
    @abstractmethod
    def get_metadata(self, symbol: str) -> dict:
        pass
