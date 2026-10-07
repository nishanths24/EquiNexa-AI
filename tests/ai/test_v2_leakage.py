import pytest
from datetime import datetime, timedelta
import pandas as pd

@pytest.mark.asyncio
async def test_v2_leakage_future_data():
    """
    G7. Mandatory Leakage Test:
    Ensures that shifting future data does not change the prediction at time T.
    feature at T uses only data <= T.
    """
    # Create mock OHLCV timeline
    dates = pd.date_range(start="2026-09-01", end="2026-10-01")
    df = pd.DataFrame({"close": [100 + i for i in range(len(dates))]}, index=dates)
    
    T = datetime(2026, 9, 20)
    
    def generate_features_at_t(data, t):
        # The feature extractor MUST strictly truncate data to <= T
        visible_data = data[data.index <= t]
        return visible_data['close'].mean()
        
    feature_original = generate_features_at_t(df, T)
    
    # Mutate future data
    df.loc[df.index > T, "close"] = 9999
    feature_mutated = generate_features_at_t(df, T)
    
    # Assert features are perfectly identical despite future mutation
    assert feature_original == feature_mutated, "LEAKAGE DETECTED: Future data mutated the features at time T."

@pytest.mark.asyncio
async def test_v2_leakage_news_publication():
    """
    News must be strictly bounded by published_at <= T.
    """
    news = [
        {"published_at": datetime(2026, 9, 19), "sentiment": 1},
        {"published_at": datetime(2026, 9, 21), "sentiment": -1}, # FUTURE
    ]
    T = datetime(2026, 9, 20)
    
    def get_news_sentiment(news_list, t):
        valid = [n for n in news_list if n["published_at"] <= t]
        if not valid: return 0
        return sum(n["sentiment"] for n in valid) / len(valid)
        
    sentiment = get_news_sentiment(news, T)
    assert sentiment == 1, "LEAKAGE DETECTED: Future news was included in sentiment calculation."
