import pytest
import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from app.ai.patterns.candlestick.engine import CandlestickEngine
from app.ai.patterns.chart.engine import ChartPatternEngine

def test_doji_detection():
    ce = CandlestickEngine()
    
    # Doji: open and close are almost identical
    dates = pd.date_range("2022-01-01", periods=1)
    df = pd.DataFrame({
        "open": [100.0],
        "high": [105.0],
        "low": [95.0],
        "close": [100.005]
    }, index=dates)
    
    res = ce.detect_all(df)
    assert res['doji'].iloc[0] == 1.0
    
    # Not a doji
    df2 = pd.DataFrame({
        "open": [100.0],
        "high": [105.0],
        "low": [95.0],
        "close": [104.0]
    }, index=dates)
    
    res2 = ce.detect_all(df2)
    assert res2['doji'].iloc[0] == 0.0

def test_hammer_detection():
    ce = CandlestickEngine()
    dates = pd.date_range("2022-01-01", periods=1)
    
    # Hammer: long lower shadow, small body, little upper shadow
    df = pd.DataFrame({
        "open": [100.0],
        "high": [100.5],
        "low": [90.0],
        "close": [99.0]
    }, index=dates)
    
    res = ce.detect_all(df)
    assert res['hammer'].iloc[0] == 1.0
