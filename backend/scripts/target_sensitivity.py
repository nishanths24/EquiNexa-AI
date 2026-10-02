import os
import sys
import pandas as pd
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from backend.app.ai.models.targets.labels import compute_labels
from backend.app.ai.research.backtest.harness import BacktestHarness
from backend.app.ai.research.evaluation.metrics import evaluate_classification

def target_sensitivity():
    df = pd.read_csv("data/historical_dataset.csv", index_col=0, parse_dates=True)
    df_aapl = df[df['ticker'] == 'AAPL'].sort_index().copy()
    
    thresholds = [0.0, 0.01, 0.02, 0.03]
    harness = BacktestHarness(initial_train_size=100, step_size=20, embargo_bars=1)
    
    class MajorityModel:
        def train(self, df_train):
            y = df_train['target'].dropna().values
            if len(y) > 0:
                values, counts = np.unique(y, return_counts=True)
                self.majority_class = values[np.argmax(counts)]
            else:
                self.majority_class = np.nan
                
    def predict_majority(model, df_test):
        if not hasattr(model, 'majority_class'):
            return pd.Series(np.nan, index=df_test.index)
        return pd.Series(model.majority_class, index=df_test.index)
        
    print("=== MAJORITY-BASELINE RECONCILIATION & TARGET SENSITIVITY (AAPL) ===")
    for thresh in thresholds:
        print(f"\nThreshold: > {thresh*100}% in 5 days")
        target = compute_labels(df_aapl, horizon=5, threshold=thresh)
        df_aapl['target'] = target
        
        # Whole dataset distribution
        pos = (target == 1.0).sum()
        neg = (target == 0.0).sum()
        total = pos + neg
        
        print(f"  Whole Dataset Distribution:")
        print(f"    Positive (UP): {pos} ({(pos/total)*100:.1f}%)")
        print(f"    Negative (DOWN): {neg} ({(neg/total)*100:.1f}%)")
        
        # Walk-forward Majority Baseline
        maj_preds = harness.run_walk_forward(df_aapl, lambda d: [m:=MajorityModel(), m.train(d)][0], predict_majority)
        
        # Align targets for evaluation
        test_indices = maj_preds.index
        y_true = df_aapl.loc[test_indices, 'target']
        
        # Drop NaNs before evaluation (due to horizon at the end)
        valid_idx = y_true.notna() & maj_preds.notna()
        y_true_valid = y_true[valid_idx]
        maj_preds_valid = maj_preds[valid_idx]
        
        acc = (y_true_valid == maj_preds_valid).mean()
        print(f"  Walk-Forward Test Majority Accuracy: {acc*100:.1f}%")

if __name__ == "__main__":
    target_sensitivity()
