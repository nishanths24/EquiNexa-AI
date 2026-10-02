import pytest
import pandas as pd
from backend.app.ai.research.backtest.harness import BacktestHarness

def test_backtest_harness():
    df = pd.DataFrame({'feature': range(10)})
    
    harness = BacktestHarness(initial_train_size=4, step_size=2, embargo_bars=1)
    
    def mock_train(df_train):
        # Model just learns the max value of train set
        return df_train['feature'].max()
        
    def mock_predict(model, df_test):
        # Predicts 1 if feature > model else 0
        return (df_test['feature'] > model).astype(float)
        
    preds = harness.run_walk_forward(df, mock_train, mock_predict)
    
    # Split 1: train 0-3 (max 3), test 5-6 (feature 5,6) -> preds 1,1
    assert preds.loc[5] == 1.0
    assert preds.loc[6] == 1.0
    
    # Split 2: train 0-5 (max 5), test 7-8 (feature 7,8) -> preds 1,1
    assert preds.loc[7] == 1.0
    
    # Assert embargo rows were never predicted on
    assert pd.isna(preds.loc[4])
