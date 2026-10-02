import pytest
from datetime import datetime, timezone, timedelta
from backend.app.ai.rag.ingestion.normalize import normalize_text, canonicalize_url
from backend.app.ai.rag.ingestion.dedupe import deduplicate_exact, get_content_hash
from backend.app.ai.rag.ingestion.timestamp_validation import validate_timestamp
from backend.app.ai.rag.sources.news_source import RawArticle

def test_normalize():
    assert normalize_text("  hello   world  ") == "hello world"
    assert normalize_text("<p>Hello</p> World") == "Hello World"
    
def test_canonicalize_url():
    url = "https://example.com/news/123?utm_source=twitter"
    assert canonicalize_url(url) == "https://example.com/news/123"

def test_dedupe():
    now = datetime.now(timezone.utc)
    a1 = RawArticle(title="A", source="Src", url="url1", published_at=now, content="same content")
    a2 = RawArticle(title="B", source="Src", url="url2", published_at=now + timedelta(hours=1), content="same content")
    
    unique = deduplicate_exact([a2, a1])
    assert len(unique) == 1
    assert unique[0].title == "A" # Earliest is kept

def test_timestamp_validation():
    ingested_at = datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)
    
    # Valid
    assert validate_timestamp(datetime(2026, 1, 1, 10, 0, tzinfo=timezone.utc), ingested_at)
    
    # Invalid future
    assert not validate_timestamp(datetime(2026, 1, 1, 13, 0, tzinfo=timezone.utc), ingested_at)
    
    # Naive timestamp
    assert not validate_timestamp(datetime(2026, 1, 1, 10, 0), ingested_at)
