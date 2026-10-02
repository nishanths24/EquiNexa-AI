from pydantic import BaseModel
from typing import Dict, Any, Optional

class FeatureVector(BaseModel):
    # Technical
    price_close: float
    sma_20: float
    rsi_14: float
    
    # ML Baseline
    baseline_ml_prob: float
    
    # Sentiment & News
    sentiment_score: float
    event_impact: str
    
    # Patterns
    candlestick_hammer: float
    chart_breakout: float
    
    # Vision
    vision_trend: str
    vision_has_evidence: bool
    
    # Preserve disagreements explicitly
    # E.g., if Technical is Bullish (RSI>70, SMA positive) but Sentiment is Bearish
    technical_signal: int # 1, 0, -1
    sentiment_signal: int # 1, 0, -1
    disagreement_flag: bool

def build_fusion_vector(
    technical: Dict[str, Any],
    baseline_prob: float,
    sentiment: Dict[str, Any],
    patterns: Dict[str, Any],
    vision: Dict[str, Any]
) -> FeatureVector:
    
    tech_signal = 1 if technical.get('rsi_14', 50) > 60 else (-1 if technical.get('rsi_14', 50) < 40 else 0)
    sent_signal = 1 if sentiment.get('score', 0) > 0.5 else (-1 if sentiment.get('score', 0) < -0.5 else 0)
    
    disagreement = tech_signal != 0 and sent_signal != 0 and tech_signal != sent_signal
    
    return FeatureVector(
        price_close=technical.get('close', 0.0),
        sma_20=technical.get('sma_20', 0.0),
        rsi_14=technical.get('rsi_14', 50.0),
        baseline_ml_prob=baseline_prob,
        sentiment_score=sentiment.get('score', 0.0),
        event_impact=sentiment.get('impact', 'none'),
        candlestick_hammer=patterns.get('hammer', 0.0),
        chart_breakout=patterns.get('breakout', 0.0),
        vision_trend=vision.get('trend', 'unknown'),
        vision_has_evidence=vision.get('has_evidence', False),
        technical_signal=tech_signal,
        sentiment_signal=sent_signal,
        disagreement_flag=disagreement
    )
