import pytest
from backend.app.models.domain.ai_analysis import AIAnalysisResponse, SetupConfig
from backend.app.ai.risk.risk_engine import RiskEngine
from pydantic import ValidationError

def test_phase10_pydantic_guardrails():
    """Phase 10: AI Analysis Guardrails - malformed/hallucinated-output tests"""
    # Test rejection of negative prices
    with pytest.raises(ValidationError):
        SetupConfig(entry_zone_low=-10, entry_zone_high=100, stop_loss=90, target_1=110)
        
    # Test rejection of invalid geometry (stop loss above entry for LONG)
    with pytest.raises(ValidationError):
        # Long setup, but stop loss (105) is higher than entry zone (95-100)
        SetupConfig(entry_zone_low=95, entry_zone_high=100, stop_loss=105, target_1=110)

def test_phase12_risk_engine():
    """Phase 12: Risk Engine - entry/stop/targets/RR/sizing - invalid-geometry rejection"""
    engine = RiskEngine(account_size=10000, max_portfolio_risk_pct=0.02, max_position_pct=1.0)
    
    # 2% of 10000 is $200 risk allowed.
    # Entry at 100, stop at 90. Risk per share is $10.
    # Target at 130.
    result = engine.compute_risk(entry_price=100, stop_loss=90, target=130)
    assert result["position_size"] == 20
    assert result["risk_reward"] == 3.0 # $30 reward / $10 risk

    # Zero risk scenario (invalid geometry rejection handled natively)
    with pytest.raises(ValueError):
        engine.compute_risk(entry_price=100, stop_loss=100, target=110)
