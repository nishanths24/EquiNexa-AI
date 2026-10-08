import pytest
import os
from fastapi.testclient import TestClient
from backend.app.api.main import app

client = TestClient(app)

def test_security_headers_present():
    """Phase 17 Exit Gate: Validate security headers."""
    response = client.get("/api/v1/health")
    assert response.headers.get("Strict-Transport-Security") == "max-age=31536000; includeSubDomains"
    assert response.headers.get("X-Content-Type-Options") == "nosniff"
    assert response.headers.get("X-Frame-Options") == "DENY"
    assert response.headers.get("Content-Security-Policy") == "default-src 'self'"
    assert response.headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"

def test_rate_limiting_429_returned():
    """Phase 17 Exit Gate: Anonymous rate limit is enforced."""
    # The anonymous limit is 30 requests per minute
    # Reset internal state if this is run multiple times
    from backend.app.core.security import _rate_limits
    _rate_limits.clear()
    
    # Hit the limit
    for _ in range(30):
        res = client.get("/api/v1/health")
        assert res.status_code == 200
        
    # The 31st request should be rejected with 429
    res_429 = client.get("/api/v1/health")
    assert res_429.status_code == 429
    assert "Retry-After" in res_429.headers
    assert res_429.json()["detail"] == "Too Many Requests"

def test_env_example_no_secrets():
    """Phase 17 Exit Gate: Verify .env.example contains no real secrets."""
    env_example_path = os.path.join(os.path.dirname(__file__), "..", "..", "backend", ".env.example")
    assert os.path.exists(env_example_path), ".env.example is missing"
    
    with open(env_example_path, "r") as f:
        content = f.read()
    
    # Simple heuristic: keys should have empty values or localhost URLs
    lines = content.splitlines()
    for line in lines:
        if "=" in line:
            key, val = line.split("=", 1)
            val = val.strip()
            if "API_KEY" in key or "SECRET" in key or "TOKEN" in key:
                assert val == "", f"Secret {key} must be empty in .env.example!"
