import pytest
import os
from backend.app.ai.safety.security import SecurityContext, get_cors_config

def test_security_hardening():
    # Valid ticker
    assert SecurityContext.validate_ticker_input("AAPL")
    assert SecurityContext.validate_ticker_input("BRK.B")
    
    # Invalid ticker (injection attempt)
    with pytest.raises(ValueError):
        SecurityContext.validate_ticker_input("AAPL'; DROP TABLE users;")
        
    # Test CORS
    cors = get_cors_config()
    assert "https://equinexa.com" in cors["allow_origins"]
    assert "*" not in cors["allow_origins"] # Ensure no wildcard
