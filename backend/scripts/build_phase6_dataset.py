import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime, timezone

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from backend.app.ai.marketdata.yfinance_provider import YFinanceProvider
from backend.app.ai.marketdata.validation import validate_price_frame
from backend.app.ai.technical.registry import feature_registry
import backend.app.ai.technical.indicators
from backend.app.ai.models.targets.labels import compute_labels

def build_phase6_dataset():
    us_universe = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA"]
    in_universe = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS"]
    
    start_date = datetime(2018, 1, 1, tzinfo=timezone.utc)
    # Using the end of 2023 to have a solid multi-year historical block
    end_date = datetime(2024, 1, 1, tzinfo=timezone.utc) 
    
    provider = YFinanceProvider()
    
    print("Fetching regime data...")
    spy = provider.fetch_ohlcv("SPY", start_date, end_date)
    if not spy.empty: spy.set_index('ts_utc', inplace=True)
    nsei = provider.fetch_ohlcv("^NSEI", start_date, end_date)
    if not nsei.empty: nsei.set_index('ts_utc', inplace=True)
    
    spy_sma200 = spy['close'].rolling(200).mean() if not spy.empty else pd.Series()
    nsei_sma200 = nsei['close'].rolling(200).mean() if not nsei.empty else pd.Series()
    
    def get_regime(ticker, date, close_price):
        if ticker.endswith(".NS"):
            if nsei_sma200.empty or date not in nsei_sma200.index: return "UNKNOWN"
            sma = nsei_sma200.loc[date]
            if pd.isna(sma): return "UNKNOWN"
            # We compare the NIFTY 50 close price to its SMA, not the individual stock
            # Actually simpler: compare NIFTY50 close to NIFTY50 SMA200
            idx_close = nsei.loc[date, 'close']
            return "BULL" if idx_close > sma else "BEAR"
        else:
            if spy_sma200.empty or date not in spy_sma200.index: return "UNKNOWN"
            sma = spy_sma200.loc[date]
            if pd.isna(sma): return "UNKNOWN"
            idx_close = spy.loc[date, 'close']
            return "BULL" if idx_close > sma else "BEAR"

    all_data = []
    
    for ticker in us_universe + in_universe:
        print(f"Fetching data for {ticker}...")
        df = provider.fetch_ohlcv(ticker, start_date, end_date)
        
        if df.empty:
            print(f"No data for {ticker}")
            continue
            
        report = validate_price_frame(df)
        if not report.is_valid:
            print(f"Validation failed for {ticker}")
            continue
            
        print(f"Computing technicals for {ticker}...")
        df_features = feature_registry.compute_all(df)
        
        print(f"Computing target labels for {ticker}...")
        df_features['target_label_5d'] = compute_labels(df_features, horizon=5, threshold=0.02)
        
        df_features['ticker'] = ticker
        df_features['market'] = "IN" if ticker.endswith(".NS") else "US"
        
        # Add Regime
        regimes = []
        for d, row in df_features.iterrows():
            regimes.append(get_regime(ticker, d, row['close']))
        df_features['market_regime'] = regimes
        
        # Add year
        df_features['year'] = df_features.index.year if isinstance(df_features.index, pd.DatetimeIndex) else pd.to_datetime(df_features['ts_utc']).dt.year
        
        all_data.append(df_features)
        
    if all_data:
        final_df = pd.concat(all_data)
        os.makedirs("data", exist_ok=True)
        out_path = "data/phase6_dataset.csv"
        final_df.to_csv(out_path)
        print(f"Dataset successfully built and saved to {out_path}")
        print(f"Total rows: {len(final_df)}")
    else:
        print("Failed to build dataset.")

if __name__ == "__main__":
    build_phase6_dataset()
