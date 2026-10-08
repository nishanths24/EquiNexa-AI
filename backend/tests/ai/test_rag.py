import pytest
from datetime import datetime, timezone, timedelta
from typing import List
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from backend.app.ai.rag.sources.historical_news_provider import HistoricalArticle

def filter_news(articles: List[HistoricalArticle], as_of_date: datetime) -> List[HistoricalArticle]:
    return [a for a in articles if a.published_at <= as_of_date]

def test_historical_rag_strict_filter():
    as_of = datetime(2022, 6, 1, tzinfo=timezone.utc)
    
    valid_article = HistoricalArticle(
        article_id="1", url="", source="", title="", content="", ticker="AAPL",
        published_at=datetime(2022, 5, 20, tzinfo=timezone.utc),
        ingested_at=datetime.now(timezone.utc), content_hash=""
    )
    
    future_article = HistoricalArticle(
        article_id="2", url="", source="", title="", content="", ticker="AAPL",
        published_at=datetime(2022, 6, 2, tzinfo=timezone.utc),
        ingested_at=datetime.now(timezone.utc), content_hash=""
    )
    
    live_article = HistoricalArticle(
        article_id="3", url="", source="", title="", content="", ticker="AAPL",
        published_at=datetime(2026, 9, 29, tzinfo=timezone.utc),
        ingested_at=datetime.now(timezone.utc), content_hash=""
    )
    
    corpus = [valid_article, future_article, live_article]
    filtered = filter_news(corpus, as_of)
    
    assert len(filtered) == 1
    assert filtered[0].article_id == "1"
