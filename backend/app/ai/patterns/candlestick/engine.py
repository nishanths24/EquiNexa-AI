import pandas as pd
import numpy as np
from typing import Dict, List, Any
from backend.app.ai.marketdata.market_data_provider import PriceFrame

def detect_doji(df: PriceFrame, tolerance: float = 0.001) -> pd.Series:
    """Mathematical definition of a Doji pattern."""
    body_size = (df['close'] - df['open']).abs()
    candle_range = df['high'] - df['low']
    
    # Avoid div by zero
    candle_range = candle_range.replace(0, np.nan)
    
    is_doji = (body_size / candle_range) <= tolerance
    return is_doji.fillna(False).astype(float)

def detect_hammer(df: PriceFrame) -> pd.Series:
    """Mathematical definition of a Hammer pattern."""
    body_size = (df['close'] - df['open']).abs()
    lower_shadow = np.minimum(df['open'], df['close']) - df['low']
    upper_shadow = df['high'] - np.maximum(df['open'], df['close'])
    candle_range = df['high'] - df['low']
    
    # Hammer conditions:
    # 1. Lower shadow is at least twice the real body
    # 2. Upper shadow is very small (e.g., less than 10% of the entire range)
    cond1 = lower_shadow >= (2 * body_size)
    cond2 = upper_shadow <= (0.1 * candle_range)
    cond3 = candle_range > 0
    
    is_hammer = cond1 & cond2 & cond3
    return is_hammer.astype(float)

def detect_hanging_man(df: PriceFrame) -> pd.Series:
    """Mathematical definition of a Hanging Man pattern (shape is same as hammer, but usually in uptrend)."""
    # For shape, it's identical to hammer. 
    # True Hanging Man requires an uptrend, which we approximate by checking if close > SMA(10).
    is_hammer_shape = detect_hammer(df)
    sma_10 = df['close'].rolling(window=10).mean()
    cond_uptrend = df['close'] > sma_10
    
    is_hanging_man = is_hammer_shape.astype(bool) & cond_uptrend
    return is_hanging_man.astype(float)

def detect_bullish_harami(df: PriceFrame) -> pd.Series:
    """Mathematical definition of Bullish Harami."""
    # Prev candle: large bearish
    prev_open = df['open'].shift(1)
    prev_close = df['close'].shift(1)
    prev_high = df['high'].shift(1)
    prev_low = df['low'].shift(1)
    
    prev_is_bearish = prev_close < prev_open
    prev_body_size = (prev_open - prev_close).abs()
    
    # Current candle: small bullish, completely inside prev body
    curr_open = df['open']
    curr_close = df['close']
    
    curr_is_bullish = curr_close > curr_open
    
    # Harami condition: current body inside prev body
    cond_inside = (curr_open > prev_close) & (curr_close < prev_open)
    
    is_harami = prev_is_bearish & curr_is_bullish & cond_inside
    return is_harami.fillna(False).astype(float)

def detect_bearish_harami(df: PriceFrame) -> pd.Series:
    """Mathematical definition of Bearish Harami."""
    # Prev candle: large bullish
    prev_open = df['open'].shift(1)
    prev_close = df['close'].shift(1)
    
    prev_is_bullish = prev_close > prev_open
    
    # Current candle: small bearish, completely inside prev body
    curr_open = df['open']
    curr_close = df['close']
    
    curr_is_bearish = curr_close < curr_open
    
    # Harami condition: current body inside prev body
    cond_inside = (curr_open < prev_close) & (curr_close > prev_open)
    
    is_harami = prev_is_bullish & curr_is_bearish & cond_inside
    return is_harami.fillna(False).astype(float)

class CandlestickEngine:
    def __init__(self):
        self.detectors = {
            'doji': detect_doji,
            'hammer': detect_hammer,
            'hanging_man': detect_hanging_man,
            'bullish_harami': detect_bullish_harami,
            'bearish_harami': detect_bearish_harami
        }
        
    def detect_all(self, df: PriceFrame) -> pd.DataFrame:
        results = {}
        for name, func in self.detectors.items():
            results[name] = func(df)
            
        return pd.DataFrame(results, index=df.index)
