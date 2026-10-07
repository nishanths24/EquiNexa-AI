import pytest
from fastapi.testclient import TestClient
from app.api.main import app

client = TestClient(app)

def test_v2_markets_overview():
    # Calling the overview endpoint
    response = client.get("/api/v2/markets/overview")
    assert response.status_code == 200
    data = response.json()
    
    # Assert regions exist
    assert "India" in data
    assert "USA" in data
    assert "Europe" in data
    
    # Assert the format follows our Pydantic Quote model (e.g. meta object included)
    for region, quotes in data.items():
        for quote in quotes:
            assert "price" in quote
            assert "meta" in quote
            assert quote["meta"]["data_status"] in ["REALTIME", "DELAYED", "EOD", "STALE", "UNAVAILABLE"]

def test_v2_forex_overview():
    response = client.get("/api/v2/markets/forex")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    
def test_v2_macro_overview():
    response = client.get("/api/v2/markets/macro")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
