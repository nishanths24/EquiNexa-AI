from pydantic import BaseModel
from typing import Dict

class EnsemblePrediction(BaseModel):
    final_prob: float
    direction: str # UP, DOWN, NEUTRAL
    weights_used: Dict[str, float]

class EnsembleAggregator:
    def __init__(self, use_learned_weights: bool = False):
        self.use_learned_weights = use_learned_weights
        
        # Hard-coded heuristics as per docs unless learned
        self.default_weights = {
            'technical_baseline': 0.3,
            'sentiment_rag': 0.4,
            'pattern_engine': 0.3
        }
        
    def aggregate(self, tech_prob: float, sent_prob: float = None, pattern_prob: float = None) -> EnsemblePrediction:
        w = self.default_weights.copy()
        
        s_prob = sent_prob if sent_prob is not None else 0.5
        p_prob = pattern_prob if pattern_prob is not None else 0.5
        
        # If missing, we can zero out the weight and re-normalize, or assume neutral 0.5.
        # Since standard ensemble might just assume neutral if no info:
        if sent_prob is None:
            w['sentiment_rag'] = 0.0
        if pattern_prob is None:
            w['pattern_engine'] = 0.0
            
        total_weight = sum(w.values())
        if total_weight == 0:
            final_prob = tech_prob
        else:
            final_prob = (
                w['technical_baseline'] * tech_prob +
                w['sentiment_rag'] * s_prob +
                w['pattern_engine'] * p_prob
            ) / total_weight
        
        direction = "UP" if final_prob > 0.55 else ("DOWN" if final_prob < 0.45 else "NEUTRAL")
        
        return EnsemblePrediction(
            final_prob=final_prob,
            direction=direction,
            weights_used=w
        )
