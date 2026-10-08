import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from backend.app.ai.research.backtest.harness import BacktestHarness
from backend.app.ai.models.targets.labels import compute_labels

def test_embargo_leakage():
    # Create 50 days of dummy data
    dates = pd.date_range("2022-01-01", periods=50, freq='D')
    df = pd.DataFrame({"close": np.arange(50)}, index=dates)
    
    harness = BacktestHarness(initial_train_size=20, step_size=5, embargo_bars=2)
    
    from backend.app.ai.research.evaluation.splits import walk_forward_split
    splits = list(walk_forward_split(df, harness.initial_train_size, harness.step_size, harness.embargo_bars))
    assert len(splits) > 0
    
    train_idx, test_idx = splits[0]
    
    train_dates = df.loc[train_idx].index
    test_dates = df.loc[test_idx].index
    
    max_train = train_dates.max()
    min_test = test_dates.min()
    
    # Embargo of 2 bars means min_test should be max_train + 2 days (in this daily freq)
    # Actually, df.iloc returns integer locations.
    assert min_test > max_train + timedelta(days=harness.embargo_bars - 1)

def test_future_target_leakage():
    dates = pd.date_range("2022-01-01", periods=20, freq='D')
    df = pd.DataFrame({"close": np.linspace(100, 120, 20)}, index=dates)
    
    horizon = 5
    target = compute_labels(df, horizon=horizon, threshold=0.01)
    
    # The last 5 labels must be NaN because future data doesn't exist
    assert target.iloc[-horizon:].isna().all()
    # The first 15 should not be NaN
    assert target.iloc[:-horizon].notna().all()
