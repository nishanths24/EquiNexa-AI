from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class RawArticle(BaseModel):
    title: str
    source: str
    url: str
    published_at: datetime
    content: str
    updated_at: Optional[datetime] = None
    author: Optional[str] = None
    tickers: List[str] = []

class NewsSource(ABC):
    @abstractmethod
    def fetch(self, query_or_ticker: str, since: datetime, until: datetime) -> List[RawArticle]:
        pass
