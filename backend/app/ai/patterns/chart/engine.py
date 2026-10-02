import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
from backend.app.ai.marketdata.market_data_provider import PriceFrame

class ChartPatternEngine:
    def detect_breakout(self, df: PriceFrame, lookback: int = 20, threshold: float = 0.0) -> pd.Series:
        """
        Detects a basic breakout where close > highest high of the previous `lookback` periods.
        """
        if len(df) < lookback + 1:
            return pd.Series(0.0, index=df.index)
            
        rolling_high = df['high'].rolling(window=lookback).max().shift(1)
        breakout = df['close'] > (rolling_high * (1 + threshold))
        
        return breakout.astype(float)
        
    def detect_support_bounce(self, df: PriceFrame, lookback: int = 20, tolerance: float = 0.01) -> pd.Series:
        """
        Detects a bounce off a support level (lowest low of the previous `lookback` periods).
        """
        if len(df) < lookback + 1:
            return pd.Series(0.0, index=df.index)
            
        rolling_low = df['low'].rolling(window=lookback).min().shift(1)
        
        near_support = (df['low'] - rolling_low).abs() / rolling_low <= tolerance
        bounced = df['close'] > df['open'] # bullish candle
        
        support_bounce = near_support & bounced
        return support_bounce.astype(float)
        
    def detect_double_top(self, df: PriceFrame, lookback: int = 20, tolerance: float = 0.02) -> pd.Series:
        """Detects basic double top formation using rolling windows."""
        if len(df) < lookback + 1:
            return pd.Series(0.0, index=df.index)
            
        rolling_high = df['high'].rolling(window=lookback).max().shift(1)
        # To be a double top, current high must be very close to the rolling high, and we need a bearish reaction
        near_resistance = (rolling_high - df['high']).abs() / rolling_high <= tolerance
        bearish_reaction = df['close'] < df['open']
        
        double_top = near_resistance & bearish_reaction
        return double_top.astype(float)
        
    def detect_double_bottom(self, df: PriceFrame, lookback: int = 20, tolerance: float = 0.02) -> pd.Series:
        """Detects basic double bottom formation."""
        if len(df) < lookback + 1:
            return pd.Series(0.0, index=df.index)
            
        rolling_low = df['low'].rolling(window=lookback).min().shift(1)
        near_support = (df['low'] - rolling_low).abs() / rolling_low <= tolerance
        bullish_reaction = df['close'] > df['open']
        
        double_bottom = near_support & bullish_reaction
        return double_bottom.astype(float)
        
    def detect_head_and_shoulders(self, df: PriceFrame, lookback: int = 20, tolerance: float = 0.03) -> pd.Series:
        """Detects basic head and shoulders using peak heuristics."""
        if len(df) < lookback * 3:
            return pd.Series(0.0, index=df.index)
            
        # Simplified: left shoulder, head, right shoulder within lookback*3
        # In a real engine, we'd use local extrema (e.g., scipy.signal.find_peaks).
        # We'll use a simple proxy: rolling max over 3 different windows to represent the 3 peaks.
        # This is a basic mathematical heuristic.
        p3 = df['high'] # right shoulder (current)
        p2 = df['high'].shift(lookback) # head
        p1 = df['high'].shift(lookback * 2) # left shoulder
        
        # Head must be higher than both shoulders
        head_highest = (p2 > p1) & (p2 > p3)
        # Shoulders should be roughly equal
        shoulders_equal = (p1 - p3).abs() / p1 <= tolerance
        bearish_reaction = df['close'] < df['open']
        
        hns = head_highest & shoulders_equal & bearish_reaction
        return hns.fillna(False).astype(float)

    def detect_all(self, df: PriceFrame) -> pd.DataFrame:
        results = {
            'breakout': self.detect_breakout(df),
            'support_bounce': self.detect_support_bounce(df),
            'double_top': self.detect_double_top(df),
            'double_bottom': self.detect_double_bottom(df),
            'head_and_shoulders': self.detect_head_and_shoulders(df)
        }
        return pd.DataFrame(results, index=df.index)
