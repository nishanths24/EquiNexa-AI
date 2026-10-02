import os
import sys
import json
import subprocess

feature_sets = {
    "basic": ["daily_return"],
    "trend": ["daily_return", "sma_20", "ema_12"],
    "momentum": ["daily_return", "sma_20", "ema_12", "rsi_14", "macd_hist"],
    "volatility": ["daily_return", "sma_20", "ema_12", "rsi_14", "macd_hist", "atr_14", "bb_width"],
    "volume": ["daily_return", "sma_20", "ema_12", "rsi_14", "macd_hist", "atr_14", "bb_width", "vol_change"]
}

models = ["LogisticRegression", "RandomForest", "HistGradientBoosting"]

def create_config(exp_id, features, model_type, use_pat):
    cfg = {
        "experiment_id": exp_id,
        "description": f"Model: {model_type}, Features: {len(features)}, Patterns: {use_pat}",
        "data": {
            "tickers": ["AAPL", "MSFT", "GOOGL"],
            "start_date": "2022-01-01",
            "end_date": "2023-01-01",
            "features": features
        },
        "target": {
            "horizon": 5,
            "threshold": 0.02,
            "type": "binary"
        },
        "validation": {
            "method": "walk_forward",
            "initial_train_size": 100,
            "step_size": 20,
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

def run_ablation():
    print("=== PHASE 5: ABLATION MATRIX ===")
    
    # Run LogReg Ablation
    for f_name, f_list in feature_sets.items():
        # Without patterns
        path = create_config(f"EXP-5-LOGREG-{f_name.upper()}", f_list, "LogisticRegression", False)
        subprocess.run([sys.executable, "backend/scripts/run_experiment.py", "--config", path])
    
    # Run Pattern Ablation on Full Feature Set
    path = create_config(f"EXP-5-LOGREG-VOLUME-PATTERNS", feature_sets["volume"], "LogisticRegression", True)
    subprocess.run([sys.executable, "backend/scripts/run_experiment.py", "--config", path])
    
    # Run Model Comparison on Full Feature Set + Patterns
    path = create_config(f"EXP-5-RF-VOLUME-PATTERNS", feature_sets["volume"], "RandomForest", True)
    subprocess.run([sys.executable, "backend/scripts/run_experiment.py", "--config", path])
    
    path = create_config(f"EXP-5-HGB-VOLUME-PATTERNS", feature_sets["volume"], "HistGradientBoosting", True)
    subprocess.run([sys.executable, "backend/scripts/run_experiment.py", "--config", path])
    
if __name__ == "__main__":
    run_ablation()
