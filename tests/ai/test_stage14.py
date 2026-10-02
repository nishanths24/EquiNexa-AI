import pytest
from backend.app.ai.models.fusion.feature_vector import build_fusion_vector

def test_feature_fusion():
    technical = {'close': 150.0, 'sma_20': 140.0, 'rsi_14': 75.0} # Bullish technical
    sentiment = {'score': -0.8, 'impact': 'high'} # Bearish sentiment
    patterns = {'hammer': 1.0, 'breakout': 0.0}
    vision = {'trend': 'up', 'has_evidence': True}
    
    fv = build_fusion_vector(
        technical=technical,
        baseline_prob=0.6,
        sentiment=sentiment,
        patterns=patterns,
        vision=vision
    )
    
    assert fv.technical_signal == 1
    assert fv.sentiment_signal == -1
    assert fv.disagreement_flag == True
    assert fv.candlestick_hammer == 1.0
