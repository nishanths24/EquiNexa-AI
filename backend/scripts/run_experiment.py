import os
import sys
import json
import argparse
import pandas as pd
import numpy as np
import hashlib
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from backend.app.ai.research.config import ExperimentConfig, ExperimentResult
from backend.app.ai.models.baseline.model_factory import create_model
from backend.app.ai.research.backtest.harness import BacktestHarness
from backend.app.ai.research.evaluation.metrics import evaluate_classification
from backend.app.ai.models.ensemble.aggregator import EnsembleAggregator
from backend.app.ai.patterns.candlestick.engine import CandlestickEngine
from backend.app.ai.patterns.chart.engine import ChartPatternEngine

def run_experiment(config_path: str):
    with open(config_path, 'r') as f:
        config_data = json.load(f)
    
    config = ExperimentConfig(**config_data)
    
    data_path = config.data.dataset_path
    df = pd.read_csv(data_path, index_col=0, parse_dates=True)
    
    dataset_hash = hashlib.sha256(pd.util.hash_pandas_object(df, index=True).values).hexdigest()
    config_hash = hashlib.sha256(json.dumps(config_data, sort_keys=True).encode()).hexdigest()
    
    # Filter tickers
    df = df[df['ticker'].isin(config.data.tickers)]
    df = df.reset_index(drop=True)
    features = config.data.features
    
    horizon = config.target.horizon
    thresh = config.target.threshold
    df['future_return'] = df.groupby('ticker')['close'].shift(-horizon) / df['close'] - 1
    df['dynamic_target'] = (df['future_return'] > thresh).astype(float)
    df.loc[df['future_return'].isna(), 'dynamic_target'] = np.nan
    
    harness = BacktestHarness(config.validation.initial_train_size, config.validation.step_size, config.validation.embargo_bars)
    
    def train_func(df_train):
        X = df_train[features].values
        y = df_train['dynamic_target'].values
        valid_idx = ~np.isnan(y) & ~np.isnan(X).any(axis=1)
        X, y = X[valid_idx], y[valid_idx]
        
        model = create_model(config.model.model_type, config.model.hyperparameters, config.random_seed)
        if len(y) > 0 and len(np.unique(y)) > 1:
            model.fit(X, y)
        return model
        
    def predict_func(model, df_test):
        X = df_test[features].values
        if not hasattr(model.named_steps['classifier'], 'classes_'):
            return pd.Series(np.nan, index=df_test.index)
        try:
            preds = model.predict_proba(X)[:, 1]
            return pd.Series(preds, index=df_test.index)
        except Exception:
            return pd.Series(np.nan, index=df_test.index)
            
    # Baseline
    preds = harness.run_walk_forward(df, train_func, predict_func)
    
    # Patterns
    if config.model.use_patterns:
        ce = CandlestickEngine()
        cpe = ChartPatternEngine()
        cs_res = ce.detect_all(df)
        
        agg = EnsembleAggregator()
        ensemble_preds = []
        for i, p in enumerate(preds.values):
            if pd.isna(p):
                ensemble_preds.append(np.nan)
                continue
            row = df.iloc[i:i+1]
            bo = cpe.detect_breakout(row).iloc[0]
            sb = cpe.detect_support_bounce(row).iloc[0]
            db = cpe.detect_double_bottom(row).iloc[0]
            dt = cpe.detect_double_top(row).iloc[0]
            hs = cpe.detect_head_and_shoulders(row).iloc[0]
            
            bullish = bool(bo or sb or db)
            bearish = bool(dt or hs)
            pat_prob = 0.5
            if bullish and not bearish: pat_prob = 0.8
            elif bearish and not bullish: pat_prob = 0.2
            
            agg_pred = agg.aggregate(tech_prob=p, sent_prob=None, pattern_prob=pat_prob)
            ensemble_preds.append(agg_pred.final_prob)
            
        preds = pd.Series(ensemble_preds, index=preds.index)
    
    y_true = df.loc[preds.index, 'dynamic_target']
    metrics = evaluate_classification(y_true.values, preds.values)
    
    # Subset metrics
    def subset_metrics(group_col):
        res = {}
        if group_col in df.columns:
            groups = df.loc[preds.index].groupby(group_col)
            for name, group in groups:
                idx = group.index
                yt = y_true.loc[idx]
                yp = preds.loc[idx]
                if len(yt) > 10:
                    res[str(name)] = evaluate_classification(yt.values, yp.values)
        return res
        
    metrics['per_year'] = subset_metrics('year')
    metrics['per_ticker'] = subset_metrics('ticker')
    metrics['per_regime'] = subset_metrics('market_regime')
    metrics['per_market'] = subset_metrics('market')
    
    result = ExperimentResult(
        experiment_id=config.experiment_id,
        timestamp=datetime.now().isoformat(),
        config_hash=config_hash,
        dataset_hash=dataset_hash,
        metrics=metrics,
        artifacts=[]
    )
    
    registry_path = "backend/app/ai/research/registry/registry.jsonl"
    with open(registry_path, 'a') as f:
        f.write(result.model_dump_json() + '\n')
        
    print(f"{config.experiment_id} | Acc: {metrics['accuracy']:.4f} | Brier: {metrics['brier']:.4f} | ECE: {metrics['ece']:.4f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    run_experiment(args.config)
