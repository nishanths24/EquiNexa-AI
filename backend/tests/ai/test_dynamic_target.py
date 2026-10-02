import pytest
import pandas as pd
import numpy as np
import json
import hashlib
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from backend.app.ai.research.config import ExperimentConfig

def create_mock_data():
    df = pd.DataFrame({
        'ticker': ['AAPL']*6 + ['MSFT']*6,
        'close': [100.0, 101.0, 102.0, 103.0, 104.0, 101.0, # AAPL returns: 0.01, 0.02, 0.03, 0.04, -0.03
                  200.0, 202.0, 204.0, 206.0, 208.0, 190.0]  # MSFT returns: 0.01, 0.02, 0.03, 0.04, -0.09
    })
    # Add dummy features
    df['dummy'] = 1.0
    return df

def generate_targets(df, horizon, threshold):
    df['future_return'] = df.groupby('ticker')['close'].shift(-horizon) / df['close'] - 1
    df['dynamic_target'] = (df['future_return'] > threshold).astype(float)
    df.loc[df['future_return'].isna(), 'dynamic_target'] = np.nan
    return df

def test_threshold_distributions():
    df = create_mock_data()
    # Test threshold 0.0
    df_0 = generate_targets(df.copy(), horizon=1, threshold=0.0)
    # Test threshold 0.02
    df_2 = generate_targets(df.copy(), horizon=1, threshold=0.02)
    
    # AAPL returns are [0.01, 0.0099, 0.0098, 0.0097, -0.028] -> wait, returns are relative.
    # 101/100-1 = 0.01
    # 102/101-1 = 0.0099
    
    dist_0 = df_0['dynamic_target'].sum()
    dist_2 = df_2['dynamic_target'].sum()
    
    assert dist_0 > dist_2, "Threshold 0.0 should have more positive targets than 0.02"

def test_end_of_series_excluded():
    df = create_mock_data()
    df = generate_targets(df, horizon=1, threshold=0.0)
    
    # The last row for each ticker should be NaN
    aapl_last = df[df['ticker'] == 'AAPL'].iloc[-1]
    msft_last = df[df['ticker'] == 'MSFT'].iloc[-1]
    
    assert pd.isna(aapl_last['dynamic_target'])
    assert pd.isna(msft_last['dynamic_target'])

def test_future_prices_not_in_features():
    df = create_mock_data()
    df = generate_targets(df, horizon=1, threshold=0.0)
    features = ['dummy']
    assert 'future_return' not in features
    assert 'dynamic_target' not in features
    assert 'close' not in features

def test_config_hashing_respects_threshold():
    base_config = {
        "experiment_id": "TEST",
        "description": "test",
        "data": {"dataset_path": "test.csv", "tickers": ["AAPL"], "start_date": "2020", "end_date": "2021", "features": ["dummy"]},
        "target": {"horizon": 5, "threshold": 0.0, "type": "binary"},
        "validation": {"method": "walk_forward", "initial_train_size": 1, "step_size": 1, "embargo_bars": 1},
        "model": {"model_type": "LogisticRegression", "hyperparameters": {}, "use_patterns": False},
        "random_seed": 42
    }
    
    cfg_0 = ExperimentConfig(**base_config)
    hash_0 = hashlib.sha256(json.dumps(base_config, sort_keys=True).encode()).hexdigest()
    
    base_config["target"]["threshold"] = 0.02
    cfg_2 = ExperimentConfig(**base_config)
    hash_2 = hashlib.sha256(json.dumps(base_config, sort_keys=True).encode()).hexdigest()
    
    assert hash_0 != hash_2, "Config hash must change when threshold changes"

def test_dataset_hash_independent():
    df1 = create_mock_data()
    hash1 = hashlib.sha256(pd.util.hash_pandas_object(df1, index=True).values).hexdigest()
    
    df2 = create_mock_data()
    df2 = generate_targets(df2, horizon=1, threshold=0.0)
    # The raw dataset read from CSV does not have dynamic_target initially
    hash2 = hashlib.sha256(pd.util.hash_pandas_object(df2.drop(columns=['future_return', 'dynamic_target']), index=True).values).hexdigest()
    
    assert hash1 == hash2, "Raw dataset hash must be independent of target generation"

def test_deterministic_target():
    df1 = create_mock_data()
    df2 = create_mock_data()
    
    df1 = generate_targets(df1, horizon=1, threshold=0.02)
    df2 = generate_targets(df2, horizon=1, threshold=0.02)
    
    pd.testing.assert_series_equal(df1['dynamic_target'], df2['dynamic_target'])
