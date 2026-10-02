from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from datetime import datetime

class PredictionSnapshot(BaseModel):
    prediction_id: str
    ticker: str
    market: str
    prediction_timestamp: datetime
    as_of_timestamp: datetime
    model_version: str
    model_hash: str
    config_hash: str
    feature_version: str
    target_definition: Dict[str, Any]
    predicted_probability: float
    predicted_class: int
    technical_feature_snapshot: Dict[str, float]
    pattern_snapshot: Dict[str, Any]
    news_article_ids: List[str]
    news_hashes: List[str]
    sentiment_output: Optional[Dict[str, Any]] = None
    retrieval_metadata: Optional[Dict[str, Any]] = None
    provider_metadata: Optional[Dict[str, Any]] = None

class OutcomeSnapshot(BaseModel):
    prediction_id: str
    actual_forward_return: Optional[float] = None
    actual_target: Optional[int] = None
    outcome_timestamp: Optional[datetime] = None
    evaluation_status: str # 'pending', 'evaluated', 'insufficient_data'
