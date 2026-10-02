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
