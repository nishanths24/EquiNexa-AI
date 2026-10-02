import pytest
import numpy as np
from backend.app.ai.models.calibration.calibrator import ProbabilityCalibrator, calculate_brier_score, calculate_ece

def test_calibration():
    # Perfectly calibrated
    y_true = np.array([0, 0, 1, 1])
    y_prob = np.array([0.1, 0.2, 0.8, 0.9])
    
    brier = calculate_brier_score(y_true, y_prob)
    assert brier < 0.1
    
    ece = calculate_ece(y_true, y_prob, n_bins=2)
    assert ece < 0.2
    
    calibrator = ProbabilityCalibrator()
    
    with pytest.raises(ValueError, match="Do not expose unvalidated probabilities"):
        calibrator.predict_calibrated(y_prob)
        
    calibrator.fit(y_true, y_prob)
    calibrator.validate(y_true, y_prob, ece_threshold=0.5)
    
    cal_prob = calibrator.predict_calibrated(y_prob)
    assert len(cal_prob) == 4
