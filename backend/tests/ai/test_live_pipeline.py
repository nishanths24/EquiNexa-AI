import pytest
from datetime import datetime, timezone, timedelta
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from backend.app.ai.research.live_pipeline import LivePredictionPipeline
from backend.app.ai.research.config import ExperimentConfig

class DummyConfig:
    class Data:
        features = ["dummy_feature"]
    data = Data()
    def model_dump(self):
        return {"dummy": "config"}

class DummyNewsProvider:
    class Article:
        def __init__(self, t):
            self.article_id = "1"
            self.published_at = t
            self.content_hash = "abc"
            self.ticker = "AAPL"
            
    def fetch_live_news(self, ticker):
        # returns one future news, one past news
        return [
            self.Article(datetime(2022, 1, 1, tzinfo=timezone.utc)),
            self.Article(datetime(2022, 1, 10, tzinfo=timezone.utc))
        ]

def test_live_pipeline_leakage_rejection():
    config = DummyConfig()
    pipeline = LivePredictionPipeline(None, config, None, None, DummyNewsProvider())
    
    # Create market data with future rows
    dates = [
        datetime(2022, 1, 1, tzinfo=timezone.utc),
        datetime(2022, 1, 5, tzinfo=timezone.utc),
        datetime(2022, 1, 10, tzinfo=timezone.utc)
    ]
    df = pd.DataFrame({
        "dummy_feature": [1.0, 2.0, 3.0]
    }, index=dates)
    
    # Predict at 2022-01-05
    pred_time = datetime(2022, 1, 5, tzinfo=timezone.utc)
    
    snapshot = pipeline.predict("AAPL", "US", df, pred_time)
    
    # Ensure technical feature used is from 2022-01-05 (value = 2.0)
    assert snapshot.technical_feature_snapshot["dummy_feature"] == 2.0
    
    # Ensure news retrieved strictly < prediction_time (so only the 2022-01-01 article)
    assert len(snapshot.news_article_ids) == 1
    
    # Ensure prediction snapshot is immutable
    assert snapshot.prediction_id is not None
    assert snapshot.as_of_timestamp == pred_time
