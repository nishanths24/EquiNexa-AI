import pandas as pd
from typing import Callable, List, Dict
from backend.app.ai.research.evaluation.splits import walk_forward_split

class BacktestHarness:
    def __init__(self, initial_train_size: int, step_size: int, embargo_bars: int = 1):
        self.initial_train_size = initial_train_size
        self.step_size = step_size
        self.embargo_bars = embargo_bars
        
    def run_walk_forward(self, df: pd.DataFrame, train_func: Callable, predict_func: Callable) -> pd.Series:
        """
        Runs walk forward evaluation strictly respecting embargo to prevent leakage.
        """
        predictions = pd.Series(index=df.index, dtype=float)
        
        splits = walk_forward_split(df, self.initial_train_size, self.step_size, self.embargo_bars)
        
        for train_idx, test_idx in splits:
            # 1. Slice data strictly
            df_train = df.loc[train_idx].copy()
            df_test = df.loc[test_idx].copy()
            
            # 2. Train model
            model = train_func(df_train)
            
            # 3. Predict on test
            preds = predict_func(model, df_test)
            
            # 4. Assign results
            predictions.loc[test_idx] = preds
            
        return predictions
