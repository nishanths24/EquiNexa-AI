from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class DataMetadata(BaseModel):
    symbol: str
    provider: str
    market: str
    currency: str
    timestamp: datetime
    retrieved_at: datetime
    data_status: str = Field(..., description="REALTIME | DELAYED | EOD | STALE | UNAVAILABLE")
    delay_minutes: int = 0
    latency_ms: int = 0
    source: str
    is_market_open: bool
    from_cache: bool = False
    cache_age_s: int = 0

class Quote(BaseModel):
    price: float
    change: float
    change_percent: float
    high: float
    low: float
    volume: float
    meta: DataMetadata

class OHLCV(BaseModel):
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    meta: DataMetadata

class MarketStatus(BaseModel):
    market: str
    is_open: bool
    next_open: Optional[datetime]
    next_close: Optional[datetime]
    meta: DataMetadata
