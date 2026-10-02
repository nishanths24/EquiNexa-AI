import os
import sys
import json
import subprocess

us_tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA"]
in_tickers = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS"]
all_tickers = us_tickers + in_tickers

vol_features = ["daily_return", "sma_20", "ema_12", "rsi_14", "macd_hist", "atr_14", "bb_width", "vol_change"]

def create_config(exp_id, thresh, model_type, use_pat):
    cfg = {
        "experiment_id": exp_id,
        "description": f"Phase 6: {model_type}, Thresh: {thresh}, Pat: {use_pat}",
        "data": {
            "dataset_path": "data/phase6_dataset.csv",
            "tickers": all_tickers,
            "start_date": "2018-01-01",
            "end_date": "2024-01-01",
            "features": vol_features
        },
        "target": {
            "horizon": 5,
            "threshold": thresh,
            "type": "binary"
        },
        "validation": {
            "method": "walk_forward",
            "initial_train_size": 252, # 1 year initial train
            "step_size": 63, # 1 quarter step
            "embargo_bars": 1
        },
        "model": {
            "model_type": model_type,
            "hyperparameters": {},
            "use_patterns": use_pat
        },
        "random_seed": 42
    }
    path = f"backend/app/ai/research/configs/{exp_id}.json"
    with open(path, 'w') as f:
        json.dump(cfg, f, indent=4)
    return path

def run_phase6():
    print("=== PHASE 6: GENERALIZATION STUDY ===")
    
    # 1. Target Sensitivity with HGB + Patterns
    for thresh in [0.0, 0.01, 0.02, 0.03]:
        path = create_config(f"EXP-6-HGB-TH-{int(thresh*100)}", thresh, "HistGradientBoosting", True)
        subprocess.run([sys.executable, "backend/scripts/run_experiment.py", "--config", path])
        
    # 2. Pattern Ablation on standard 0.02 threshold
    # HGB without patterns
    path = create_config("EXP-6-HGB-NOPAT", 0.02, "HistGradientBoosting", False)
    subprocess.run([sys.executable, "backend/scripts/run_experiment.py", "--config", path])
    
    # RF without patterns
    path = create_config("EXP-6-RF-NOPAT", 0.02, "RandomForest", False)
    subprocess.run([sys.executable, "backend/scripts/run_experiment.py", "--config", path])
    
    # RF with patterns
    path = create_config("EXP-6-RF-PAT", 0.02, "RandomForest", True)
    subprocess.run([sys.executable, "backend/scripts/run_experiment.py", "--config", path])

if __name__ == "__main__":
    run_phase6()
