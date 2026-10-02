import pytest
from datetime import datetime, timezone
from backend.api.ai.endpoints import PredictionRequest, AIEndpointHandler
from backend.app.ai.schemas.canonical import CanonicalResponse
from pydantic import ValidationError

def test_api_schemas_and_handler():
    # Test valid request
    req = PredictionRequest(ticker="AAPL", horizon_days=5)
    assert req.ticker == "AAPL"
    
    # Test invalid ticker length
    with pytest.raises(ValidationError):
        PredictionRequest(ticker="", horizon_days=5)
        
    # Test invalid horizon
    with pytest.raises(ValidationError):
        PredictionRequest(ticker="AAPL", horizon_days=100)
        
    handler = AIEndpointHandler()
    resp = handler.predict(req)
    
    assert isinstance(resp, CanonicalResponse)
    assert resp.prediction.direction == "NEUTRAL"
    assert "request_id" in resp.metadata
