import pytest
import pandas as pd
from datetime import datetime, timezone
from backend.app.ai.marketdata.validation import validate_price_frame, DataQualityReport
from backend.app.ai.marketdata.instrument_master import InstrumentMaster, Instrument

def test_validation():
    # Valid dataframe
    df = pd.DataFrame({
        'ts_local': pd.date_range('2026-01-01', periods=2),
        'ts_utc': pd.date_range('2026-01-01', periods=2, tz='UTC'),
        'open': [100, 101],
        'high': [105, 106],
        'low': [95, 96],
        'close': [102, 103],
        'volume': [1000, 1500]
    })
    
    report = validate_price_frame(df)
    assert report.is_valid
    assert report.score == 1.0
    
    # Inconsistent OHLC (low > open)
    df_inconsistent = df.copy()
    df_inconsistent.loc[0, 'low'] = 110
    
    report_inc = validate_price_frame(df_inconsistent)
    assert not report_inc.is_valid or report_inc.score < 1.0
    assert any(i.issue_type == "ohlc_inconsistency" for i in report_inc.issues)
    
def test_instrument_master():
    master = InstrumentMaster()
    inst = Instrument(
        instrument_id="TCS_IN",
        symbol="TCS.NS",
        provider_symbols={"yfinance": "TCS.NS"},
        name="Tata Consultancy Services",
        aliases=["TCS"],
        market="IN",
        exchange="NSE",
        currency="INR",
        timezone="Asia/Kolkata",
        instrument_type="equity",
        sector="IT"
    )
    master.add_instrument(inst)
    
    assert master.get_by_symbol("TCS.NS") == inst
    assert master.resolve_alias("TCS") == inst
    assert master.resolve_alias("Tata Consultancy Services") == inst
