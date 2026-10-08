import pytest
import pandas as pd
import numpy as np
from backend.app.ai.technical.indicators import calculate_sma, calculate_rsi
from backend.app.ai.technical.patterns import detect_doji, detect_engulfing

@pytest.fixture
def sample_ohlcv():
    # Construct a deterministic dataframe for known-dataset testing
    data = {
        'open': [100, 102, 105, 105, 104, 101, 100, 102, 105, 110],
        'high': [102, 106, 107, 108, 106, 102, 105, 108, 110, 115],
        'low':  [99, 101, 104, 104, 100, 99, 98, 100, 104, 108],
        'close': [101, 105, 105, 104, 101, 100, 102, 105, 110, 114],
        'volume': [1000, 1200, 1100, 900, 1500, 1300, 1600, 2000, 2500, 3000]
    }
    return pd.DataFrame(data)

def test_sma_no_lookahead(sample_ohlcv):
    """Bar-by-bar replay no look-ahead test"""
    # Calculate SMA period 3
    sma = calculate_sma(sample_ohlcv, period=3, source='close')
    
    # Manual calculation for index 2: (101 + 105 + 105) / 3 = 103.666...
    assert np.isclose(sma.iloc[2], 103.666666)
    
    # Simulate a bar-by-bar replay: if we only had up to index 2, the SMA should be exactly the same
    sma_subset = calculate_sma(sample_ohlcv.iloc[:3], period=3, source='close')
    assert np.isclose(sma_subset.iloc[2], sma.iloc[2])

def test_doji_detection():
    data = {
        'open': [100, 100, 100],
        'high': [105, 105, 105],
        'low':  [95, 95, 95],
        'close': [100, 100.5, 104] # Exact Doji, Near Doji, Not Doji
    }
    df = pd.DataFrame(data)
    doji = detect_doji(df, threshold=0.1)
    
    assert doji.iloc[0] == True # 0% body
    assert doji.iloc[1] == True # 5% body (0.5 / 10)
    assert doji.iloc[2] == False # 40% body (4 / 10)

def test_engulfing_detection():
    data = {
        'open': [100, 105, 100, 95],
        'high': [106, 106, 106, 106],
        'low':  [99, 99, 99, 99],
        'close':[105, 95, 95, 105] 
    }
    # row 0: green (100 -> 105)
    # row 1: red (105 -> 95) => Bearish engulfing of row 0
    # row 2: red (100 -> 95)
    # row 3: green (95 -> 105) => Bullish engulfing of row 2
    df = pd.DataFrame(data)
    
    engulf = detect_engulfing(df)
    assert engulf.iloc[1] == -1 # Bearish
    assert engulf.iloc[3] == 1  # Bullish
