import os
import sys
from datetime import datetime, timezone

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from backend.app.ai.marketdata.yfinance_provider import YFinanceProvider
from backend.app.ai.marketdata.validation import validate_price_frame
from backend.app.ai.technical.registry import feature_registry
# Ensure indicators are registered
import backend.app.ai.technical.indicators
from backend.app.ai.models.targets.labels import compute_labels

def build_dataset():
    universe = ["AAPL", "MSFT", "GOOGL"]
    start_date = datetime(2022, 1, 1, tzinfo=timezone.utc)
    end_date = datetime(2023, 1, 1, tzinfo=timezone.utc)
    
    provider = YFinanceProvider()
    registry = feature_registry
    
    all_data = []
    
    for ticker in universe:
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
        df_features = registry.compute_all(df)
        
        print(f"Computing target labels for {ticker}...")
        df_features['target_label_5d'] = compute_labels(df_features, horizon=5, threshold=0.02)
        
        df_features['ticker'] = ticker
        all_data.append(df_features)
        
    import pandas as pd
    if all_data:
        final_df = pd.concat(all_data)
        os.makedirs("data", exist_ok=True)
        out_path = "data/historical_dataset.csv"
        final_df.to_csv(out_path)
        print(f"Dataset successfully built and saved to {out_path}")
        print(f"Total rows: {len(final_df)}")
    else:
        print("Failed to build dataset.")

if __name__ == "__main__":
    build_dataset()
