from pydantic import BaseModel, Field, root_validator
from typing import List, Dict, Optional, Literal
from datetime import datetime

class SetupConfig(BaseModel):
    setup_type: Literal["BREAKOUT", "BREAKDOWN", "PULLBACK", "TREND_CONTINUATION", "REVERSAL", "RANGE_TRADE", "MOMENTUM", "MEAN_REVERSION", "NO_SETUP"]
    timeframe: str
    entry_zone: List[float] = Field(..., min_items=2, max_items=2)
    stop_loss: float
    targets: List[float]
    risk_reward: float
    status: Literal["WAIT_FOR_CONFIRMATION", "ACTIVE", "INVALIDATED", "NO_SETUP"]
    confirmation_required: List[str]
    invalidation: List[str]

class AIAnalysisResponse(BaseModel):
    symbol: str
    as_of: str
    bias: Literal["STRONGLY_BULLISH", "BULLISH", "NEUTRAL", "BEARISH", "STRONGLY_BEARISH"]
    confidence: float
    confidence_kind: Literal["heuristic", "calibrated"]
    current_price: float
    scenarios: Dict[str, Dict]
    setup: SetupConfig
    reasons: List[str]
    risks: List[str]
    evidence: Dict[str, Dict]
    data_status: Dict[str, str]
    warning: str

    @root_validator(pre=True)
    def validate_guardrails(cls, values):
        price = values.get("current_price")
        if price is None or price <= 0:
            raise ValueError("Guardrail Violation: Negative or zero current price.")
            
        setup = values.get("setup")
        bias = values.get("bias")
        if setup and setup.get("setup_type") != "NO_SETUP":
            sl = setup.get("stop_loss", 0)
            entry_low, entry_high = setup.get("entry_zone", [0, 0])
            targets = setup.get("targets", [])
            
            if bias in ["BULLISH", "STRONGLY_BULLISH"]:
                if sl >= entry_low:
                    raise ValueError("Guardrail Violation: Stop loss must be below entry zone for long setups.")
                if targets and min(targets) <= entry_high:
                    raise ValueError("Guardrail Violation: Target must be above entry zone for long setups.")
            elif bias in ["BEARISH", "STRONGLY_BEARISH"]:
                if sl <= entry_high:
                    raise ValueError("Guardrail Violation: Stop loss must be above entry zone for short setups.")
                if targets and max(targets) >= entry_low:
                    raise ValueError("Guardrail Violation: Target must be below entry zone for short setups.")
                    
            if setup.get("risk_reward", 0) <= 0:
                raise ValueError("Guardrail Violation: Impossible or zero risk-reward ratio.")
                
        return values
