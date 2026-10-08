import pytest
import numpy as np
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from backend.app.ai.research.evaluation.metrics import evaluate_classification

def test_metrics_calculation():
    # Simple deterministic test
    y_true = np.array([1, 1, 0, 0, 1])
    y_pred = np.array([0.9, 0.8, 0.1, 0.6, 0.4]) # 3 correct (idx 0, 1, 2), 2 incorrect (idx 3, 4)
    
    metrics = evaluate_classification(y_true, y_pred)
    
    # Threshold is 0.5
    # y_pred_binary = [1, 1, 0, 1, 0]
    # correct = [1, 1, 1, 0, 0] => accuracy = 3/5 = 0.6
    assert np.isclose(metrics['accuracy'], 0.6)
    
    # Brier score = mean((y_pred - y_true)^2)
    # (0.9-1)^2 + (0.8-1)^2 + (0.1-0)^2 + (0.6-0)^2 + (0.4-1)^2
    # 0.01 + 0.04 + 0.01 + 0.36 + 0.36 = 0.78 / 5 = 0.156
    assert np.isclose(metrics['brier'], 0.156)
