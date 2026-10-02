import os
import sys
import pandas as pd
import numpy as np
import json
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from backend.app.ai.models.targets.labels import compute_labels
from backend.app.ai.research.evaluation.metrics import evaluate_classification
from backend.app.ai.patterns.chart.engine import ChartPatternEngine
from backend.app.ai.patterns.candlestick.engine import CandlestickEngine
import yfinance as yf

def audit_dataset():
    data_path = "data/historical_dataset.csv"
    df = pd.read_csv(data_path, index_col=0, parse_dates=True)
    
    print("=== DATASET AUDIT ===")
    for ticker in df['ticker'].unique():
        df_t = df[df['ticker'] == ticker]
        if 'ts_utc' in df_t.columns:
            min_d, max_d = df_t['ts_utc'].min(), df_t['ts_utc'].max()
        else:
            min_d, max_d = df_t.index.min(), df_t.index.max()
        print(f"Ticker: {ticker}")
        print(f"  Rows: {len(df_t)}")
        print(f"  Min Date: {min_d}")
        print(f"  Max Date: {max_d}")
        
    print("\n=== TARGET AUDIT ===")
    target = df['target_label_5d']
    pos = (target == 1.0).sum()
    neg = (target == 0.0).sum()
    nans = target.isna().sum()
    total = len(target)
    
    print(f"  Total Rows: {total}")
    print(f"  Positives: {pos} ({(pos/(pos+neg))*100:.1f}%)")
    print(f"  Negatives: {neg} ({(neg/(pos+neg))*100:.1f}%)")
    print(f"  Removed by Horizon/NaNs: {nans}")
    
    print("\n=== PATTERN AUDIT (AAPL) ===")
    df_aapl = df[df['ticker'] == 'AAPL'].copy()
    ce = CandlestickEngine()
    cpe = ChartPatternEngine()
    
    cs_res = ce.detect_all(df_aapl)
    doji = cs_res.get('doji', pd.Series([0])).sum()
    hammer = cs_res.get('hammer', pd.Series([0])).sum()
    bo = cpe.detect_breakout(df_aapl).sum()
    sb = cpe.detect_support_bounce(df_aapl).sum()
    dt = cpe.detect_double_top(df_aapl).sum()
    db = cpe.detect_double_bottom(df_aapl).sum()
    hs = cpe.detect_head_and_shoulders(df_aapl).sum()
    
    print(f"  Doji: {doji}")
    print(f"  Hammer: {hammer}")
    print(f"  Breakout: {bo}")
    print(f"  Support Bounce: {sb}")
    print(f"  Double Top: {dt}")
    print(f"  Double Bottom: {db}")
    print(f"  Head & Shoulders: {hs}")

if __name__ == "__main__":
    audit_dataset()
