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

class CandlestickEngine:
    def __init__(self):
        self.detectors = {
            'doji': detect_doji,
            'hammer': detect_hammer
        }
        
    def detect_all(self, df: PriceFrame) -> pd.DataFrame:
        results = {}
        for name, func in self.detectors.items():
            results[name] = func(df)
            
        return pd.DataFrame(results, index=df.index)
