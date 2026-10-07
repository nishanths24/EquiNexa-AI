from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class NewsArticle(BaseModel):
    """Phase 8 News Model"""
    id: str
    headline: str
    summary: str
    source: str
    url: str
    published_at: datetime
    retrieved_at: datetime
    category: str  # e.g., "Company", "Macro", "Crypto"
    sentiment: Optional[str] = None # "Bullish", "Bearish", "Neutral"
    delay_label: Optional[str] = None # "LIVE", "DELAYED"

class NewsFeed(BaseModel):
    articles: List[NewsArticle]
