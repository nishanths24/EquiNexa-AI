import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from backend.app.api.main import app

client = TestClient(app)

def test_markets_history_success():
    response = client.get("/api/v1/markets/history?ticker=^NSEI&period=1M&interval=1d")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "OK"
    assert "data" in data
    assert isinstance(data["data"], list)

def test_markets_history_invalid_preset():
    response = client.get("/api/v1/markets/history?ticker=^NSEI&period=UNKNOWN_RANGE&interval=1d")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ERROR"
    assert "Unknown range preset" in data["reason"]

def test_markets_history_ytd():
    response = client.get("/api/v1/markets/history?ticker=^NSEI&period=ytd&interval=1d")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "OK"
    assert "data" in data

def test_markets_history_3mo():
    response = client.get("/api/v1/markets/history?ticker=^NSEI&period=3mo&interval=1d")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "OK"
    assert "data" in data

def test_markets_history_unsupported_symbol():
    response = client.get("/api/v1/markets/history?ticker=INVALID_TICKER_X123&period=1M&interval=1d")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data


def test_markets_search_compatible_shape():
    response = client.get('/api/v1/market/instruments/search?q=Infosys')
    assert response.status_code == 200
    data = response.json()
    assert data['status'] in {'OK', 'UNAVAILABLE'}
    if data['status'] == 'OK' and data['results']:
        assert {'symbol', 'name', 'exchange', 'instrument_type'} <= set(data['results'][0])


def test_markets_history_intraday_unavailable_nse():
    response = client.get("/api/v1/markets/history?ticker=RELIANCE.NS&period=1D&interval=5m")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ("ERROR", "OK")
    if data["status"] == "ERROR":
        assert data.get("code") == "INTRADAY_DATA_UNAVAILABLE"
        assert "Intraday data is currently unavailable" in data.get("reason", "")


def test_markets_history_valid_nse_daily():
    response = client.get("/api/v1/markets/history?ticker=RELIANCE.NS&period=1M&interval=1d")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "OK"
    assert len(data.get("data", [])) > 0


def test_markets_history_valid_us_intraday():
    response = client.get("/api/v1/markets/history?ticker=AAPL&period=5D&interval=5m")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "OK"
    assert len(data.get("data", [])) > 0

