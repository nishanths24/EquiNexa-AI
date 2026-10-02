from pydantic import BaseModel, Field
from datetime import datetime, timezone
import uuid
from backend.app.ai.schemas.canonical import PredictionOutput, CanonicalResponse
from backend.app.ai.schemas.base import ErrorResponse, ErrorEnvelope

class PredictionRequest(BaseModel):
    ticker: str = Field(..., min_length=1, max_length=10)
    horizon_days: int = Field(default=5, ge=1, le=30)
    as_of: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class AIEndpointHandler:
    def __init__(self):
        # In a real app, this would receive the pipeline components
        pass
        
    def predict(self, request: PredictionRequest) -> CanonicalResponse:
        req_id = str(uuid.uuid4())
        try:
            # Here it would call the fusion and ensemble models
            # We mock the canonical response
            pred = PredictionOutput(
                direction="NEUTRAL",
                confidence=0.5,
                horizon=f"{request.horizon_days}d",
                status="ok"
            )
            return CanonicalResponse(
                prediction=pred,
                metadata={"request_id": req_id, "timestamp": datetime.now(timezone.utc).isoformat()}
            )
        except Exception as e:
            # Error handling mapping
            raise ValueError(f"API Error: {str(e)}")
