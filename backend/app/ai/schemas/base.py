from pydantic import BaseModel, ConfigDict
from typing import Literal, List, Dict, Any, Optional

class ErrorResponse(BaseModel):
    code: str
    message: str
    request_id: Optional[str] = None

class ErrorEnvelope(BaseModel):
    error: ErrorResponse

class ProviderHealth(BaseModel):
    status: Literal["ok", "degraded", "unavailable"]
    latency_ms: Optional[float] = None
    message: Optional[str] = None
