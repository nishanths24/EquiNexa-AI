import numpy as np
import pandas as pd
from typing import Dict, Any

class OODScorer:
    """
    Out-Of-Distribution (OOD) Scorer.
    Determines if a feature vector deviates significantly from the training distribution.
    For this version, we use simple Z-score bounding or IQR heuristics based on training stats.
    """
    def __init__(self, training_stats: Dict[str, Dict[str, float]] = None):
        # training_stats format: {"feature_name": {"mean": 0.0, "std": 1.0}}
        self.training_stats = training_stats or {}
        
    def score(self, features: pd.Series) -> Dict[str, Any]:
        """
        Returns a score from 0.0 (in-distribution) to 1.0 (highly out-of-distribution).
        """
        if not self.training_stats:
            # If no stats available, assume safe
            return {"ood_score": 0.0, "warning": False, "deviations": []}
            
        deviations = []
        total_z = 0.0
        valid_features = 0
        
        for feature, val in features.items():
            if feature in self.training_stats and not pd.isna(val):
                mean = self.training_stats[feature].get("mean", 0.0)
                std = self.training_stats[feature].get("std", 1.0)
                if std > 0:
                    z = abs((val - mean) / std)
                    total_z += z
                    valid_features += 1
                    if z > 3.0:
                        deviations.append({feature: {"val": val, "z_score": z}})
                        
        avg_z = (total_z / valid_features) if valid_features > 0 else 0.0
        
        # Sigmoid-like squashing for OOD score: 0 to 1
        ood_score = 1.0 - (1.0 / (1.0 + (avg_z / 3.0)))
        
        return {
            "ood_score": round(ood_score, 4),
            "warning": ood_score > 0.5 or len(deviations) > 0,
            "deviations": deviations
        }
