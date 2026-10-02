import pytest
from fastapi.testclient import TestClient
import sys
import os
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from backend.app.api.main import app

client = TestClient(app)

def test_health():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["version"] == "1.0.0"

def test_research_status():
    response = client.get("/api/v1/research/status")
    assert response.status_code == 200
    data = response.json()
    assert data["model_version"] == "1.0.0"
    assert "evaluated" in data
    # Ensure performance metrics are strictly suppressed
    assert "accuracy" not in data
    assert "brier_score" not in data
    
    # Assert N=0 logic in default mode (no fake inserts)
    if data["evaluated"] == 0:
        assert data["review_status"] == "COLLECTING"

def test_markets_indices():
    response = client.get("/api/v1/markets/indices")
    assert response.status_code == 200
    assert response.json()["status"] == "UNAVAILABLE"

def test_markets_search():
    response = client.get("/api/v1/markets/search?q=AAPL")
    assert response.status_code == 200
    assert response.json()["status"] == "UNAVAILABLE"

def test_markets_search_invalid():
    # Empty query should fail pydantic min_length=1
    response = client.get("/api/v1/markets/search?q=")
    assert response.status_code == 422
    
def test_predictions_latest_not_found():
    response = client.get("/api/v1/predictions/latest?ticker=INVALID")
    assert response.status_code == 404

def test_cors_behavior():
    # Test valid origin
    headers = {"Origin": "http://localhost:5173", "Access-Control-Request-Method": "GET"}
    response = client.options("/api/v1/health", headers=headers)
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://localhost:5173"
    
    # Unconfigured origin should not be in the ACAO header unless explicitly allowed
    headers_invalid = {"Origin": "https://malicious.com", "Access-Control-Request-Method": "GET"}
    response_invalid = client.options("/api/v1/health", headers=headers_invalid)
    assert response_invalid.headers.get("access-control-allow-origin") != "https://malicious.com"
