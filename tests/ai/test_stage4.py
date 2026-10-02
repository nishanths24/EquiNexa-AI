import pytest
import pandas as pd
import numpy as np
from backend.app.ai.models.targets.labels import compute_labels
from backend.app.ai.research.evaluation.splits import walk_forward_split
from backend.app.ai.models.baseline.technical_model import create_technical_baseline_model, get_majority_class_prediction

def test_labels():
    df = pd.DataFrame({
        'close': [100, 105, 95, 100, 110]
    })
    
    # 1 bar horizon
    # Returns: NaN, 0.05, -0.095, 0.052, 0.1
    # Shifted -1: 0.05, -0.095, 0.052, 0.1, NaN
    labels = compute_labels(df, horizon=1, threshold=0.0)
    
    assert labels.iloc[0] == 1.0 # 105 > 100
    assert labels.iloc[1] == 0.0 # 95 < 105
    assert labels.iloc[2] == 1.0 # 100 > 95
    assert labels.iloc[3] == 1.0 # 110 > 100
    assert pd.isna(labels.iloc[4]) # last row

def test_walk_forward():
    df = pd.DataFrame({'val': range(10)})
    splits = list(walk_forward_split(df, initial_train_size=4, step_size=2, embargo_bars=1))
    
    # Split 1: train up to 4-1 = 3, test 5 to 6
    train1, test1 = splits[0]
    assert len(train1) == 4 # index 0,1,2,3
    assert len(test1) == 2 # index 5,6
    assert set(test1) == {5, 6}

def test_baseline_model():
    X_train = np.random.rand(100, 5)
    y_train = np.random.randint(0, 2, 100)
    
    model = create_technical_baseline_model()
    model.fit(X_train, y_train)
    
    X_test = np.random.rand(10, 5)
    preds = model.predict(X_test)
    assert len(preds) == 10
    
    majority_preds = get_majority_class_prediction(y_train, 10)
    assert len(majority_preds) == 10
