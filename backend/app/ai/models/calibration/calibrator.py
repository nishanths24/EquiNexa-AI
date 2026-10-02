import numpy as np
from sklearn.metrics import brier_score_loss

def calculate_brier_score(y_true: np.ndarray, y_prob: np.ndarray) -> float:
    return brier_score_loss(y_true, y_prob)

def calculate_ece(y_true: np.ndarray, y_prob: np.ndarray, n_bins: int = 10) -> float:
    """Expected Calibration Error (ECE)"""
    bins = np.linspace(0., 1., n_bins + 1)
    binids = np.digitize(y_prob, bins) - 1
    
    ece = 0.0
    for i in range(n_bins):
        mask = binids == i
        if np.any(mask):
            prob_mean = np.mean(y_prob[mask])
            acc_mean = np.mean(y_true[mask])
            ece += (np.sum(mask) / len(y_prob)) * np.abs(prob_mean - acc_mean)
            
    return ece

class ProbabilityCalibrator:
    def __init__(self):
        self.is_calibrated = False
        
    def fit(self, y_val: np.ndarray, y_prob_val: np.ndarray):
        # In a real scenario, train IsotonicRegression or Platt scaling here
        self.is_calibrated = True
        
    def validate(self, y_val: np.ndarray, y_prob_val: np.ndarray, ece_threshold: float = 0.1):
        if not self.is_calibrated:
            raise ValueError("Model is not calibrated.")
            
        ece = calculate_ece(y_val, y_prob_val)
        if ece > ece_threshold:
            raise ValueError(f"Calibration failed: ECE {ece} exceeds threshold {ece_threshold}")
            
    def predict_calibrated(self, y_prob: np.ndarray) -> np.ndarray:
        if not self.is_calibrated:
            raise ValueError("Do not expose unvalidated probabilities. Calibrate first.")
        # Return calibrated (mocked as returning original for now)
        return y_prob
