import pandas as pd
import numpy as np

def detect_doji(df: pd.DataFrame, threshold: float = 0.1) -> pd.Series:
    """
    Detects Doji candlestick pattern.
    A Doji occurs when the open and close are almost equal.
    Threshold is the maximum percentage of the total range that the real body can occupy.
    """
    body_size = (df['close'] - df['open']).abs()
    total_range = (df['high'] - df['low']).abs()
    
    # Avoid division by zero
    total_range = total_range.replace(0, np.nan)
    
    doji = (body_size / total_range) <= threshold
    return doji.fillna(False)

def detect_engulfing(df: pd.DataFrame) -> pd.Series:
    """
    Detects Bullish and Bearish Engulfing patterns.
    Returns: 1 for Bullish, -1 for Bearish, 0 for none.
    """
    engulfing = pd.Series(0, index=df.index)
    
    prev_open = df['open'].shift(1)
    prev_close = df['close'].shift(1)
    curr_open = df['open']
    curr_close = df['close']
    
    # Bullish Engulfing: Previous red, current green, current body engulfs previous
    bullish = (prev_close < prev_open) & (curr_close > curr_open) & \
              (curr_open <= prev_close) & (curr_close >= prev_open)
              
    # Bearish Engulfing: Previous green, current red, current body engulfs previous
    bearish = (prev_close > prev_open) & (curr_close < curr_open) & \
              (curr_open >= prev_close) & (curr_close <= prev_open)
              
    engulfing[bullish] = 1
    engulfing[bearish] = -1
    
    return engulfing
