import pytest
from backend.app.ai.models.ensemble.aggregator import EnsembleAggregator

def test_ensemble_aggregator():
    agg = EnsembleAggregator()
    
    # 0.8 * 0.3 + 0.9 * 0.4 + 0.1 * 0.3 = 0.24 + 0.36 + 0.03 = 0.63
    pred = agg.aggregate(tech_prob=0.8, sent_prob=0.9, pattern_prob=0.1)
    
    assert abs(pred.final_prob - 0.63) < 0.001
    assert pred.direction == "UP"
    
    # 0.2 * 0.3 + 0.1 * 0.4 + 0.3 * 0.3 = 0.06 + 0.04 + 0.09 = 0.19
    pred2 = agg.aggregate(tech_prob=0.2, sent_prob=0.1, pattern_prob=0.3)
    assert abs(pred2.final_prob - 0.19) < 0.001
    assert pred2.direction == "DOWN"
