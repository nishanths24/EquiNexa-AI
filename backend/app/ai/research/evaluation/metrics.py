import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from typing import Dict
from backend.app.ai.models.calibration.calibrator import calculate_brier_score, calculate_ece

def evaluate_classification(y_true: np.ndarray, y_prob: np.ndarray, threshold: float = 0.5) -> Dict[str, float]:
    """Calculate core classification metrics."""
    # Filter out NaNs
    mask = ~np.isnan(y_true) & ~np.isnan(y_prob)
    yt = y_true[mask]
    yp = y_prob[mask]
    
    if len(yt) == 0:
        return {}
        
    y_pred = (yp > threshold).astype(int)
    
    from sklearn.metrics import balanced_accuracy_score, roc_auc_score, average_precision_score
    try: roc = roc_auc_score(yt, yp)
    except: roc = float('nan')
    
    try: pr = average_precision_score(yt, yp)
    except: pr = float('nan')
    
    return {
        "accuracy": accuracy_score(yt, y_pred),
        "balanced_accuracy": balanced_accuracy_score(yt, y_pred),
        "precision": precision_score(yt, y_pred, zero_division=0),
        "recall": recall_score(yt, y_pred, zero_division=0),
        "f1": f1_score(yt, y_pred, zero_division=0),
        "roc_auc": roc,
        "pr_auc": pr,
        "brier": calculate_brier_score(yt, yp),
        "ece": calculate_ece(yt, yp)
    }

def compare_models(baseline_metrics: Dict[str, float], enhanced_metrics: Dict[str, float]) -> Dict[str, float]:
    """Return the absolute improvement of enhanced over baseline."""
    improvements = {}
    for k in baseline_metrics:
        if k in enhanced_metrics:
            improvements[f"{k}_improvement"] = enhanced_metrics[k] - baseline_metrics[k]
    return improvements
