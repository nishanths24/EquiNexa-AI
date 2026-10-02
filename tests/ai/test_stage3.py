import pytest
import pandas as pd
from backend.app.ai.technical.registry import feature_registry
from backend.app.ai.marketdata.market_data_provider import PriceFrame
import backend.app.ai.technical.indicators

def test_feature_registry():
    spec = feature_registry.get_spec("sma_20")
    assert spec.name == "sma_20"
    
def test_technical_indicators():
    df = pd.DataFrame({
        'close': [100.0] * 30
    })
    
    pf = PriceFrame(df)
    
    sma = feature_registry.compute("sma_20", pf)
    assert len(sma) == 30
    assert pd.isna(sma.iloc[0])
    assert sma.iloc[-1] == 100.0
    
    rsi = feature_registry.compute("rsi_14", pf)
    assert rsi.iloc[-1] == 50.0 # flat line handled as 50.0
    
    returns = feature_registry.compute("daily_return", pf)
    assert returns.iloc[-1] == 0.0
