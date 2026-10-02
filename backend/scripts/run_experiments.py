import os
import sys
import pandas as pd
import numpy as np
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from backend.app.ai.research.backtest.harness import BacktestHarness
from backend.app.ai.models.baseline.technical_model import create_technical_baseline_model
from backend.app.ai.research.evaluation.metrics import evaluate_classification, compare_models
from backend.app.ai.models.ensemble.aggregator import EnsembleAggregator

def run_experiments():
    data_path = "data/historical_dataset.csv"
    if not os.path.exists(data_path):
        print("Historical dataset not found.")
        return
        
    df = pd.read_csv(data_path, index_col=0, parse_dates=True)
    df_aapl = df[df['ticker'] == 'AAPL'].sort_index()
    
    if len(df_aapl) < 100:
        print("Insufficient data.")
        return
        
    y_true = df_aapl['target_label_5d']
    
    # 1. Baseline Technical Model
    harness = BacktestHarness(initial_train_size=100, step_size=20, embargo_bars=1)
    
    def train_baseline(df_train):
        features = ['sma_20', 'ema_12', 'rsi_14', 'daily_return']
        X = df_train[features].values
        y = df_train['target_label_5d'].values
        
        # Remove NaNs for training
        valid_idx = ~np.isnan(y) & ~np.isnan(X).any(axis=1)
        X, y = X[valid_idx], y[valid_idx]
        
        model = create_technical_baseline_model()
        if len(y) > 0 and len(np.unique(y)) > 1:
            model.fit(X, y)
        return model
        
    def predict_baseline(model, df_test):
        features = ['sma_20', 'ema_12', 'rsi_14', 'daily_return']
        X = df_test[features].values
        
        # If model is not fitted properly, predict NaN
        if not hasattr(model.named_steps['classifier'], 'classes_'):
            return pd.Series(np.nan, index=df_test.index)
            
        try:
            preds = model.predict_proba(X)[:, 1]
            return pd.Series(preds, index=df_test.index)
        except Exception:
            return pd.Series(np.nan, index=df_test.index)
        
    # Experiment A: Majority Baseline
    def predict_majority(model, df_test):
        if not hasattr(model, 'majority_class'):
            return pd.Series(np.nan, index=df_test.index)
        return pd.Series(model.majority_class, index=df_test.index)

    class MajorityModel:
        def train(self, df_train):
            y = df_train['target_label_5d'].dropna().values
            if len(y) > 0:
                values, counts = np.unique(y, return_counts=True)
                self.majority_class = values[np.argmax(counts)]
            else:
                self.majority_class = np.nan

    maj_preds = harness.run_walk_forward(df_aapl, lambda df: [m:=MajorityModel(), m.train(df)][0], predict_majority)
    metrics_A = evaluate_classification(y_true.values, maj_preds.values)

    # Experiment B: Technical ML Baseline
    baseline_preds = harness.run_walk_forward(df_aapl, train_baseline, predict_baseline)
    metrics_B = evaluate_classification(y_true.values, baseline_preds.values)
    
    # Experiment C/D: RAG + Sentiment
    # Since we have no historical news (0 RAG participation), this will perfectly mirror the technical baseline 
    # for any prediction because sentiment/RAG data is explicitly unavailable.
    # We will NOT inject random noise. 
    
    # Experiment E: Technical + Patterns (Actual Data Exists)
    from backend.app.ai.patterns.candlestick.engine import CandlestickEngine
    from backend.app.ai.patterns.chart.engine import ChartPatternEngine
    
    ce = CandlestickEngine()
    cpe = ChartPatternEngine()
    cs_res = ce.detect_all(df_aapl)
    
    # Simple deterministic fusion: if technical predicts UP and we have a bullish pattern, boost prob.
    # If technical predicts DOWN and bearish pattern, decrease prob.
    agg = EnsembleAggregator()
    ensemble_preds = []
    
    for i, p in enumerate(baseline_preds.values):
        if pd.isna(p):
            ensemble_preds.append(np.nan)
            continue
            
        # Get pattern signals for this row
        row = df_aapl.iloc[i:i+1]
        bo = cpe.detect_breakout(row).iloc[0]
        sb = cpe.detect_support_bounce(row).iloc[0]
        db = cpe.detect_double_bottom(row).iloc[0]
        
        dt = cpe.detect_double_top(row).iloc[0]
        hs = cpe.detect_head_and_shoulders(row).iloc[0]
        
        # Bullish probability shift if bullish pattern present
        bullish_signal = bool(bo or sb or db)
        bearish_signal = bool(dt or hs)
        
        # Use actual Aggregator (fallback for missing sentiment)
        # Aggregator expects probability inputs. We map deterministic patterns to extreme probabilities
        pat_prob = 0.5
        if bullish_signal and not bearish_signal:
            pat_prob = 0.8
        elif bearish_signal and not bullish_signal:
            pat_prob = 0.2
            
        agg_pred = agg.aggregate(tech_prob=p, sent_prob=None, pattern_prob=pat_prob)
        ensemble_preds.append(agg_pred.final_prob)
        
    ensemble_series = pd.Series(ensemble_preds, index=baseline_preds.index)
    metrics_E = evaluate_classification(y_true.values, ensemble_series.values)
    
    report = {
        "dataset": "AAPL 2022-01-03 to 2022-12-30",
        "validation_methodology": "Walk-Forward (Embargo 1, Train 100, Step 20)",
        "rag_participation": "0.0% (No zero-budget historical news available for 2022. Live news correctly blocked by temporal filter.)",
        "experiment_A_majority": metrics_A,
        "experiment_B_technical": metrics_B,
        "experiment_C_sentiment": "Identical to B due to 0% historical news availability.",
        "experiment_D_rag": "Identical to B due to 0% historical news availability.",
        "experiment_E_fusion_patterns": metrics_E,
        "benchmark_reproduction": "Benchmark not reproduced with the available dataset/experimental configuration."
    }
    
    print(json.dumps(report, indent=2))
    
    with open("data/phase2_audit.json", "w") as f:
        json.dump(report, f, indent=2)

if __name__ == "__main__":
    run_experiments()
