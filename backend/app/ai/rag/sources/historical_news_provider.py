from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class HistoricalArticle(BaseModel):
    article_id: str
    url: str
    source: str
    title: str
    content: str
    ticker: str
    published_at: datetime
    ingested_at: datetime
    content_hash: str
    language: str = "en"
    embedding_version: str = "v1"

class HistoricalNewsProvider(ABC):
    """
    Abstraction for a legitimate historical financial news dataset.
    Due to zero-budget constraints, full 2022 historical news datasets 
    (e.g., Bloomberg, Reuters, historical AlphaVantage) are unavailable.
    
    This interface defines the required ingestion format. Users with access
    to premium historical datasets should implement this provider to 
    yield HistoricalArticle objects for ingestion into ChromaDB.
    """
    
    @abstractmethod
    def fetch_historical_news(self, ticker: str, start_date: datetime, end_date: datetime) -> List[HistoricalArticle]:
        """
        Fetch historical news for a specific ticker and date range.
        Must preserve exact original publication timestamps to ensure
        point-in-time temporal leakage protection during backtests.
        """
        pass
