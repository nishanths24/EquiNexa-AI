import pytest
import pandas as pd
from backend.app.ai.patterns.chart.engine import ChartPatternEngine
from backend.app.ai.marketdata.market_data_provider import PriceFrame

def test_chart_pattern_engine():
    # Setup data where 1-20 is low, 21 breaks out
    closes = [100.0] * 20 + [105.0]
    highs = [101.0] * 20 + [106.0]
    lows = [99.0] * 21
    opens = [100.0] * 21
    
    df = pd.DataFrame({
        'open': opens,
        'high': highs,
        'low': lows,
        'close': closes
    })
    pf = PriceFrame(df)
    
    engine = ChartPatternEngine()
    results = engine.detect_all(pf)
    
    assert results['breakout'].iloc[20] == 1.0 # breakout happened
    assert results['breakout'].iloc[19] == 0.0 # no breakout before
