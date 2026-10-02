from pydantic import BaseModel, Field
from typing import Literal, List, Optional
from datetime import datetime

class PredictionOutput(BaseModel):
    direction: Literal["UP", "DOWN", "NEUTRAL", "UNKNOWN"]
    confidence: float = Field(ge=0.0, le=1.0)
    probability_up: Optional[float] = None
    calibration_validated: bool = False
    horizon: str
    status: Literal["ok", "degraded", "unavailable"]

class CanonicalResponse(BaseModel):
    prediction: PredictionOutput
    technical: dict = {}
    news: dict = {}
    patterns: dict = {}
    drivers: list = []
    risks: list = []
    uncertainties: list = []
    evidence: list = []
    metadata: dict = {}
