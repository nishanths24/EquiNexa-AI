import pandas as pd
import numpy as np
from backend.app.ai.technical.registry import feature_registry, FeatureSpec
from backend.app.ai.marketdata.market_data_provider import PriceFrame

def compute_sma_20(df: PriceFrame) -> pd.Series:
    return df['close'].rolling(window=20, min_periods=20).mean()

feature_registry.register(
    FeatureSpec(name="sma_20", version="v1", window=20, inputs=["close"], warmup_bars=19, params_hash="default"),
    compute_sma_20
)

def compute_ema_12(df: PriceFrame) -> pd.Series:
    return df['close'].ewm(span=12, adjust=False).mean()

feature_registry.register(
    FeatureSpec(name="ema_12", version="v1", window=12, inputs=["close"], warmup_bars=11, params_hash="default"),
    compute_ema_12
)

def compute_rsi_14(df: PriceFrame) -> pd.Series:
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    # Handle flat price division by zero
    rsi = rsi.fillna(100.0).where(loss != 0, 100.0).where(gain != 0, 0.0).where((gain != 0) | (loss != 0), 50.0)
    return rsi

feature_registry.register(
    FeatureSpec(name="rsi_14", version="v1", window=14, inputs=["close"], warmup_bars=14, params_hash="default"),
    compute_rsi_14
)

def compute_daily_return(df: PriceFrame) -> pd.Series:
    return df['close'].pct_change(1)

feature_registry.register(
    FeatureSpec(name="daily_return", version="v1", window=2, inputs=["close"], warmup_bars=1, params_hash="default"),
    compute_daily_return
)

def compute_macd(df: PriceFrame) -> pd.Series:
    ema_12 = df['close'].ewm(span=12, adjust=False).mean()
    ema_26 = df['close'].ewm(span=26, adjust=False).mean()
    macd = ema_12 - ema_26
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd - signal

feature_registry.register(
    FeatureSpec(name="macd_hist", version="v1", window=34, inputs=["close"], warmup_bars=34, params_hash="default"),
    compute_macd
)

def compute_bollinger_width(df: PriceFrame) -> pd.Series:
    sma_20 = df['close'].rolling(window=20).mean()
    std_20 = df['close'].rolling(window=20).std()
    upper = sma_20 + (std_20 * 2)
    lower = sma_20 - (std_20 * 2)
    # Return normalized width
    return (upper - lower) / sma_20

feature_registry.register(
    FeatureSpec(name="bb_width", version="v1", window=20, inputs=["close"], warmup_bars=20, params_hash="default"),
    compute_bollinger_width
)

def compute_atr(df: PriceFrame) -> pd.Series:
    high_low = df['high'] - df['low']
    high_close = (df['high'] - df['close'].shift()).abs()
    low_close = (df['low'] - df['close'].shift()).abs()
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    return tr.rolling(window=14).mean() / df['close'] # Normalized ATR

feature_registry.register(
    FeatureSpec(name="atr_14", version="v1", window=14, inputs=["high", "low", "close"], warmup_bars=14, params_hash="default"),
    compute_atr
)

def compute_volume_change(df: PriceFrame) -> pd.Series:
    return df['volume'].pct_change(1)

feature_registry.register(
    FeatureSpec(name="vol_change", version="v1", window=2, inputs=["volume"], warmup_bars=1, params_hash="default"),
    compute_volume_change
)

# --- Phase 6: Parameterised Indicator Framework for Charting & Patterns ---
from typing import Dict, Any, List

def calculate_sma(df: pd.DataFrame, period: int = 20, source: str = 'close') -> pd.Series:
    return df[source].rolling(window=period, min_periods=period).mean()

def calculate_ema(df: pd.DataFrame, period: int = 12, source: str = 'close') -> pd.Series:
    return df[source].ewm(span=period, adjust=False).mean()

def calculate_rsi(df: pd.DataFrame, period: int = 14, source: str = 'close') -> pd.Series:
    delta = df[source].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(100.0).where(loss != 0, 100.0).where(gain != 0, 0.0).where((gain != 0) | (loss != 0), 50.0)

def calculate_macd(df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9, source: str = 'close') -> Dict[str, pd.Series]:
    ema_fast = df[source].ewm(span=fast, adjust=False).mean()
    ema_slow = df[source].ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    hist = macd_line - signal_line
    return {"macd": macd_line, "signal": signal_line, "histogram": hist}

def calculate_bollinger_bands(df: pd.DataFrame, period: int = 20, std_dev: float = 2.0, source: str = 'close') -> Dict[str, pd.Series]:
    sma = df[source].rolling(window=period).mean()
    std = df[source].rolling(window=period).std()
    return {"upper": sma + (std * std_dev), "middle": sma, "lower": sma - (std * std_dev)}

def calculate_atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    high_low = df['high'] - df['low']
    high_close = (df['high'] - df['close'].shift()).abs()
    low_close = (df['low'] - df['close'].shift()).abs()
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    return tr.rolling(window=period).mean()

def calculate_supertrend(df: pd.DataFrame, period: int = 10, multiplier: float = 3.0) -> Dict[str, pd.Series]:
    atr = calculate_atr(df, period)
    hl2 = (df['high'] + df['low']) / 2
    final_upperband = hl2 + (multiplier * atr)
    final_lowerband = hl2 - (multiplier * atr)
    
    supertrend = pd.Series(0.0, index=df.index)
    direction = pd.Series(1, index=df.index)
    
    for i in range(1, len(df.index)):
        if df['close'].iloc[i] > final_upperband.iloc[i-1]:
            direction.iloc[i] = 1
        elif df['close'].iloc[i] < final_lowerband.iloc[i-1]:
            direction.iloc[i] = -1
        else:
            direction.iloc[i] = direction.iloc[i-1]
            if direction.iloc[i] == 1 and final_lowerband.iloc[i] < final_lowerband.iloc[i-1]:
                final_lowerband.iloc[i] = final_lowerband.iloc[i-1]
            if direction.iloc[i] == -1 and final_upperband.iloc[i] > final_upperband.iloc[i-1]:
                final_upperband.iloc[i] = final_upperband.iloc[i-1]
                
        supertrend.iloc[i] = final_lowerband.iloc[i] if direction.iloc[i] == 1 else final_upperband.iloc[i]
        
    return {"supertrend": supertrend, "direction": direction}

def calculate_vwap(df: pd.DataFrame) -> pd.Series:
    """Session-based VWAP."""
    q = df['volume']
    p = (df['high'] + df['low'] + df['close']) / 3
    # Approximated VWAP across the entire dataframe for now.
    # Proper session reset requires datetime handling in df.
    vwap = (p * q).cumsum() / q.cumsum()
    return vwap

# Framework Catalogue
INDICATOR_CATALOGUE = {
    "SMA": {"name": "Simple Moving Average", "params": {"period": 20, "source": "close"}, "func": calculate_sma},
    "EMA": {"name": "Exponential Moving Average", "params": {"period": 12, "source": "close"}, "func": calculate_ema},
    "RSI": {"name": "Relative Strength Index", "params": {"period": 14, "source": "close"}, "func": calculate_rsi},
    "MACD": {"name": "MACD", "params": {"fast": 12, "slow": 26, "signal": 9, "source": "close"}, "func": calculate_macd},
    "BB": {"name": "Bollinger Bands", "params": {"period": 20, "std_dev": 2.0, "source": "close"}, "func": calculate_bollinger_bands},
    "ATR": {"name": "Average True Range", "params": {"period": 14}, "func": calculate_atr},
    "SUPERTREND": {"name": "Supertrend", "params": {"period": 10, "multiplier": 3.0}, "func": calculate_supertrend},
    "VWAP": {"name": "Volume Weighted Average Price", "params": {}, "func": calculate_vwap}
}
