import os
import sys
import pandas as pd
from datetime import datetime, timezone
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from backend.app.ai.models.baseline.technical_model import TechnicalBaselineModel
from backend.app.ai.research.backtest.harness import BacktestHarness
from backend.app.ai.research.evaluation.metrics import evaluate_classification

def train_baseline():
    data_path = "data/historical_dataset.csv"
    if not os.path.exists(data_path):
        print("Historical dataset not found. Run build_historical_dataset.py first.")
        return
        
    df = pd.read_csv(data_path, index_col=0, parse_dates=True)
    
    # We will run walk-forward for AAPL as an example
    df_aapl = df[df['ticker'] == 'AAPL'].sort_index()
    
    # Needs to be at least large enough for walk-forward
    if len(df_aapl) < 100:
        print("Not enough data for AAPL")
        return
        
    print(f"Running walk-forward evaluation on AAPL (Rows: {len(df_aapl)})...")
    
    harness = BacktestHarness(initial_train_size=100, step_size=20, embargo_bars=1)
    
    def train_func(df_train):
        model = TechnicalBaselineModel()
        model.train(df_train)
        return model
        
    def predict_func(model, df_test):
        return model.predict_proba(df_test)
        
    preds = harness.run_walk_forward(df_aapl, train_func, predict_func)
    
    # Align targets with predictions
    y_true = df_aapl['target_label_5d']
    y_prob = preds
    
    # Evaluate
    metrics = evaluate_classification(y_true.values, y_prob.values)
    
    print("Baseline Metrics (Technical Only):")
    print(json.dumps(metrics, indent=2))
    
    with open("data/baseline_metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

if __name__ == "__main__":
    train_baseline()
