from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class AlertRule(BaseModel):
    id: str
    user_id: str
    symbol: str
    alert_type: str # "PRICE_CROSSES", "INDICATOR_CROSSES", "AI_BIAS_CHANGE", "NEWS_SENTIMENT_DROP"
    condition: str  # "ABOVE", "BELOW", "CHANGES_TO"
    threshold: float
    is_active: bool = True

class AlertEvent(BaseModel):
    id: str
    rule_id: str
    user_id: str
    symbol: str
    message: str
    triggered_at: datetime = Field(default_factory=datetime.utcnow)
    is_read: bool = False
