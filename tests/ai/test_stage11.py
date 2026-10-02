import pytest
import pandas as pd
from backend.app.ai.patterns.candlestick.engine import CandlestickEngine
from backend.app.ai.marketdata.market_data_provider import PriceFrame

def test_candlestick_engine():
    df = pd.DataFrame({
        'open': [100.0, 100.0],
        'high': [101.0, 105.0],
        'low': [99.0, 90.0],
        'close': [100.0, 102.0]
    })
    pf = PriceFrame(df)
    
    engine = CandlestickEngine()
    results = engine.detect_all(pf)
    
    # First row is a perfect Doji (open == close)
    assert results['doji'].iloc[0] == 1.0
    
    # Second row is a Hammer (long lower shadow, small body, small upper shadow)
    # open:100, close:102 (body=2)
    # low:90, high:105 (lower shadow = 10, upper shadow = 3) -> Wait, upper shadow is 3, which is 3/15 = 20% of range. Not a hammer by strict <10% rule.
    # Let's adjust df to make a strict hammer
    df.loc[1, 'high'] = 102.5 # upper shadow 0.5. Range 12.5. 0.5 / 12.5 = 4% < 10%
    
    pf2 = PriceFrame(df)
    results2 = engine.detect_all(pf2)
    assert results2['hammer'].iloc[1] == 1.0
