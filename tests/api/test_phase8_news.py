import pytest
from datetime import datetime, timedelta, timezone
from app.models.domain.news import NewsArticle
from app.services.news_service import deduplicate_news, apply_delay_labels

@pytest.fixture
def base_time():
    return datetime(2026, 10, 7, 12, 0, 0, tzinfo=timezone.utc)

def test_news_deduplication(base_time):
    """Phase 8 Exit Gate: dedup test"""
    articles = [
        NewsArticle(
            id="1", headline="Fed Raises Rates", summary="...", source="ProviderA",
            url="http://a", published_at=base_time, retrieved_at=base_time, category="Macro"
        ),
        NewsArticle(
            id="2", headline=" FED RAISES RATES ", summary="Different summary", source="ProviderB",
            url="http://b", published_at=base_time - timedelta(minutes=30), retrieved_at=base_time, category="Macro"
        ),
        NewsArticle(
            id="3", headline="Apple earnings beat", summary="...", source="ProviderA",
            url="http://c", published_at=base_time, retrieved_at=base_time, category="Company"
        ),
        NewsArticle(
            id="4", headline="Fed Raises Rates", summary="Old news", source="ProviderC",
            url="http://d", published_at=base_time - timedelta(hours=3), retrieved_at=base_time, category="Macro"
        ),
    ]
    
    deduped = deduplicate_news(articles, time_window_hours=2)
    
    # We expect 3 articles:
    # id 1 and id 2 are duplicates within 2 hours, newer (id 1) is kept
    # id 3 is unique
    # id 4 is same headline as id 1, but > 2 hours old, so it's kept as a separate event
    
    assert len(deduped) == 3
    ids = [a.id for a in deduped]
    assert "1" in ids
    assert "2" not in ids # Duplicate of 1 within time window
    assert "3" in ids
    assert "4" in ids # Outside time window, kept

def test_news_delayed_labeling(base_time):
    """Phase 8 Exit Gate: delayed labeling test"""
    articles = [
        NewsArticle(
            id="1", headline="Live News", summary="...", source="A", url="A",
            published_at=base_time - timedelta(minutes=5), retrieved_at=base_time, category="Company"
        ),
        NewsArticle(
            id="2", headline="Delayed News", summary="...", source="B", url="B",
            published_at=base_time - timedelta(minutes=20), retrieved_at=base_time, category="Company"
        )
    ]
    
    labeled = apply_delay_labels(articles)
    
    assert labeled[0].delay_label == "LIVE"
    assert labeled[1].delay_label == "DELAYED"
