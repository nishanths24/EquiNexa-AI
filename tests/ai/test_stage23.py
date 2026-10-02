import pytest
import numpy as np
from backend.app.ai.research.evaluation.metrics import evaluate_classification, compare_models

def test_evaluation_metrics():
    y_true = np.array([1.0, 0.0, 1.0, 0.0, np.nan])
    y_prob_base = np.array([0.6, 0.6, 0.4, 0.4, np.nan]) # acc: 0.5
    y_prob_enh = np.array([0.9, 0.1, 0.8, 0.2, 0.5]) # acc: 1.0
    
    metrics_base = evaluate_classification(y_true, y_prob_base)
    metrics_enh = evaluate_classification(y_true, y_prob_enh)
    
    assert metrics_base["accuracy"] == 0.5
    assert metrics_enh["accuracy"] == 1.0
    
    comp = compare_models(metrics_base, metrics_enh)
    assert comp["accuracy_improvement"] == 0.5
    
    # Check ECE and Brier exist
    assert "brier" in metrics_enh
    assert "ece" in metrics_enh
