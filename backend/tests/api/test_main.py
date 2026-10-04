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
    # Provider might fail, so status is OK or UNAVAILABLE
    assert response.json()["status"] in ["OK", "UNAVAILABLE"]

def test_markets_search_invalid():
    # Empty query should fail pydantic min_length=1
    response = client.get("/api/v1/market/instruments/search?q=")
    assert response.status_code == 422

from unittest.mock import patch, MagicMock
from io import BytesIO
from PIL import Image

def test_vision_analyze_no_file():
    response = client.post("/api/v1/vision/analyze")
    assert response.status_code == 422

@patch.dict(os.environ, {"GEMINI_API_KEY": ""})
def test_vision_analyze_no_key():
    files = {'file': ('test.png', b'dummy', 'image/png')}
    response = client.post("/api/v1/vision/analyze", files=files)
    assert response.status_code == 501
    assert "LLM provider is not configured" in response.json()["detail"]

@patch.dict(os.environ, {"GEMINI_API_KEY": "valid_key"})
def test_vision_analyze_invalid_image():
    files = {'file': ('test.png', b'not an image', 'image/png')}
    response = client.post("/api/v1/vision/analyze", files=files)
    assert response.status_code == 400
    assert "Invalid or corrupt" in response.json()["detail"]

@patch.dict(os.environ, {"GEMINI_API_KEY": "valid_key"})
@patch("backend.app.api.main.get_gemini_client")
def test_vision_analyze_success(mock_get_client):
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.text = json.dumps({
        "has_sufficient_evidence": True,
        "support_levels": ["100"],
        "resistance_levels": ["110"],
        "detected_trend": "bullish",
        "patterns": ["doji"],
        "reasoning": "Looks good"
    })
    mock_client.models.generate_content.return_value = mock_response
    mock_get_client.return_value = mock_client
    
    # Create a real dummy image
    img = Image.new('RGB', (10, 10))
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    
    files = {'file': ('test.png', img_byte_arr.getvalue(), 'image/png')}
    response = client.post("/api/v1/vision/analyze", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert data["detected_trend"] == "bullish"
    assert "doji" in data["patterns"]

@patch("time.sleep", return_value=None)
@patch("yfinance.Ticker")
@patch.dict(os.environ, {"GEMINI_API_KEY": "valid_key"})
@patch("backend.app.api.main.get_gemini_client")
def test_research_query_quota_retry(mock_get_client, mock_ticker, mock_sleep):
    mock_ticker.return_value.info = {"exchange": "NMS", "currency": "USD"}
    mock_client = MagicMock()
    # Always fail with 429
    mock_client.models.generate_content.side_effect = Exception("429 Too Many Requests: Quota exceeded")
    mock_get_client.return_value = mock_client
    
    body = {"ticker": "AAPL", "query": "Latest news?"}
    response = client.post("/api/v1/research/query", json=body)
    assert response.status_code == 429
    assert "quota exceeded" in response.json()["detail"].lower()
    # It should have retried max_retries + 1 times (4 times)
    assert mock_client.models.generate_content.call_count == 4

@patch("time.sleep", return_value=None)
@patch("yfinance.Ticker")
@patch.dict(os.environ, {"GEMINI_API_KEY": "valid_key", "GEMINI_FALLBACK_MODEL": "fallback-model"})
@patch("backend.app.api.main.get_gemini_client")
def test_research_query_fallback(mock_get_client, mock_ticker, mock_sleep):
    mock_ticker.return_value.info = {"exchange": "NMS", "currency": "USD"}
    mock_client = MagicMock()
    # Fail first model with 503, succeed second
    mock_response = MagicMock()
    mock_response.text = json.dumps({"report": "Fallback report.", "citations": [], "disclaimer": "Disclaimer"})
    
    call_count = 0
    def side_effect(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if kwargs.get('model') != "fallback-model":
            raise Exception("503 Unavailable")
        return mock_response
        
    mock_client.models.generate_content.side_effect = side_effect
    mock_get_client.return_value = mock_client
    
    body = {"ticker": "AAPL", "query": "Latest news?"}
    response = client.post("/api/v1/research/query", json=body)
    assert response.status_code == 200
    assert response.json()["report"] == "Fallback report."

@patch("time.sleep", return_value=None)
@patch("yfinance.Ticker")
@patch.dict(os.environ, {"GEMINI_API_KEY": "valid_key", "GEMINI_FALLBACK_MODEL": "fallback-model"})
@patch("backend.app.api.main.get_gemini_client")
def test_research_query_fallback_fail(mock_get_client, mock_ticker, mock_sleep):
    mock_ticker.return_value.info = {"exchange": "NMS", "currency": "USD"}
    mock_client = MagicMock()
    # Fail both models with 404
    mock_client.models.generate_content.side_effect = Exception("404 Not Found")
    mock_get_client.return_value = mock_client
    
    body = {"ticker": "AAPL", "query": "Latest news?"}
    response = client.post("/api/v1/research/query", json=body)
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
    
@patch("time.sleep", return_value=None)
@patch("yfinance.Ticker")
@patch.dict(os.environ, {"GEMINI_API_KEY": "valid_key"})
@patch("backend.app.api.main.get_gemini_client")
def test_research_query_fail_fast(mock_get_client, mock_ticker, mock_sleep):
    mock_ticker.return_value.info = {"exchange": "NMS", "currency": "USD"}
    mock_client = MagicMock()
    # Fail with 400 Bad Request
    mock_client.models.generate_content.side_effect = Exception("400 Bad Request")
    mock_get_client.return_value = mock_client
    
    body = {"ticker": "AAPL", "query": "Latest news?"}
    response = client.post("/api/v1/research/query", json=body)
    assert response.status_code == 500
    assert "provider api request failed" in response.json()["detail"].lower()
    # Should not retry
    assert mock_client.models.generate_content.call_count == 1
    
@patch("yfinance.Ticker")
@patch.dict(os.environ, {"GEMINI_API_KEY": "valid_key"})
@patch("backend.app.api.main.get_gemini_client")
def test_research_query_success(mock_get_client, mock_ticker):
    mock_ticker.return_value.info = {"exchange": "NMS", "currency": "USD"}
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.text = json.dumps({
        "report": "AAPL is doing well.",
        "citations": ["News"],
        "disclaimer": "Not advice."
    })
    mock_client.models.generate_content.return_value = mock_response
    mock_get_client.return_value = mock_client
    
    body = {"ticker": "AAPL", "query": "Latest news?"}
    response = client.post("/api/v1/research/query", json=body)
    assert response.status_code == 200
    data = response.json()
    assert data["report"] == "AAPL is doing well."
    
@patch("time.sleep", return_value=None)
@patch("yfinance.Ticker")
@patch.dict(os.environ, {"GEMINI_API_KEY": "valid_key"})
@patch("backend.app.api.main.get_gemini_client")
def test_research_query_fenced_json(mock_get_client, mock_ticker, mock_sleep):
    mock_ticker.return_value.info = {"exchange": "NMS", "currency": "USD"}
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.text = '```json\n{"report": "Test", "citations": [], "disclaimer": "Test"}\n```'
    mock_client.models.generate_content.return_value = mock_response
    mock_get_client.return_value = mock_client
    
    body = {"ticker": "AAPL", "query": "Test"}
    response = client.post("/api/v1/research/query", json=body)
    assert response.status_code == 200
    assert response.json()["report"] == "Test"

@patch("time.sleep", return_value=None)
@patch("yfinance.Ticker")
@patch.dict(os.environ, {"GEMINI_API_KEY": "valid_key"})
@patch("backend.app.api.main.get_gemini_client")
def test_research_query_missing_fields(mock_get_client, mock_ticker, mock_sleep):
    mock_ticker.return_value.info = {"exchange": "NMS", "currency": "USD"}
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.text = '{"report": "Test"}' # Missing citations and disclaimer
    mock_client.models.generate_content.return_value = mock_response
    mock_get_client.return_value = mock_client
    
    body = {"ticker": "AAPL", "query": "Test"}
    response = client.post("/api/v1/research/query", json=body)
    assert response.status_code == 500
    assert "missing required field" in response.json()["detail"].lower()

@patch("time.sleep", return_value=None)
@patch("yfinance.Ticker")
@patch.dict(os.environ, {"GEMINI_API_KEY": "valid_key"})
@patch("backend.app.api.main.get_gemini_client")
def test_research_query_malformed_json(mock_get_client, mock_ticker, mock_sleep):
    mock_ticker.return_value.info = {"exchange": "NMS", "currency": "USD"}
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.text = '{broken json'
    mock_client.models.generate_content.return_value = mock_response
    mock_get_client.return_value = mock_client
    
    body = {"ticker": "AAPL", "query": "Test"}
    response = client.post("/api/v1/research/query", json=body)
    assert response.status_code == 500
    assert "malformed json" in response.json()["detail"].lower()

@patch("time.sleep", return_value=None)
@patch("yfinance.Ticker")
@patch.dict(os.environ, {"GEMINI_API_KEY": "valid_key"})
@patch("backend.app.api.main.get_gemini_client")
def test_research_query_empty_response(mock_get_client, mock_ticker, mock_sleep):
    mock_ticker.return_value.info = {"exchange": "NMS", "currency": "USD"}
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.text = '   '
    mock_client.models.generate_content.return_value = mock_response
    mock_get_client.return_value = mock_client
    
    body = {"ticker": "AAPL", "query": "Test"}
    response = client.post("/api/v1/research/query", json=body)
    assert response.status_code == 500
    assert "empty response" in response.json()["detail"].lower()

@patch("yfinance.Search")
@patch("yfinance.Ticker")
def test_research_query_ambiguous_ticker(mock_ticker, mock_search):
    mock_ticker.return_value.info = {}
    mock_search.return_value.quotes = [{"symbol": "TATASTEEL.NS"}, {"symbol": "TATAMOTORS.NS"}]
    
    body = {"ticker": "TATA", "query": "Test"}
    response = client.post("/api/v1/research/query", json=body)
    assert response.status_code == 409
    assert "ambiguous" in response.json()["detail"].lower()
    
@patch("yfinance.Search")
@patch("yfinance.Ticker")
def test_research_query_404_ticker(mock_ticker, mock_search):
    mock_ticker.return_value.info = {}
    mock_search.return_value.quotes = []
    
    body = {"ticker": "INVALID", "query": "Test"}
    response = client.post("/api/v1/research/query", json=body)
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
    
@patch("yfinance.Ticker")
@patch.dict(os.environ, {"GEMINI_API_KEY": "valid_key"})
@patch("backend.app.api.main.get_gemini_client")
def test_research_query_missing_market_data(mock_get_client, mock_ticker):
    # Mock yfinance to raise an exception indicating missing data
    mock_ticker.side_effect = Exception("Some connection error")
    
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.text = json.dumps({
        "report": "I could not verify current prices.",
        "citations": ["Unverified"],
        "disclaimer": "Not advice."
    })
    mock_client.models.generate_content.return_value = mock_response
    mock_get_client.return_value = mock_client
    
    body = {"ticker": "AAPL", "query": "Latest news?"}
    response = client.post("/api/v1/research/query", json=body)
    assert response.status_code == 200
    assert "I could not verify" in response.json()["report"]

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

@patch("asyncio.sleep", return_value=None)
@patch.dict(os.environ, {"GEMINI_API_KEY": "valid_key"})
@patch("backend.app.api.main.get_gemini_client")
def test_vision_analyze_retry_timeout(mock_get_client, mock_sleep):
    mock_client = MagicMock()
    mock_client.models.generate_content.side_effect = Exception("504 Gateway Timeout")
    mock_get_client.return_value = mock_client
    
    img = Image.new('RGB', (10, 10))
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    
    files = {'file': ('test.png', img_byte_arr.getvalue(), 'image/png')}
    response = client.post("/api/v1/vision/analyze", files=files)
    
    assert response.status_code == 504
    assert "timed out" in response.json()["detail"].lower()
    # verify retries happened
    assert mock_client.models.generate_content.call_count == 4

@patch("asyncio.sleep", return_value=None)
@patch.dict(os.environ, {"GEMINI_API_KEY": "valid_key"})
@patch("backend.app.api.main.get_gemini_client")
def test_vision_analyze_quota_failure_and_uncertain_prices(mock_get_client, mock_sleep):
    mock_client = MagicMock()
    # Mock to throw 429
    mock_client.models.generate_content.side_effect = Exception("429 Too Many Requests")
    mock_get_client.return_value = mock_client
    
    img = Image.new('RGB', (10, 10))
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    files = {'file': ('test.png', img_byte_arr.getvalue(), 'image/png')}
    
    response = client.post("/api/v1/vision/analyze", files=files)
    assert response.status_code == 429
    assert "quota exceeded" in response.json()["detail"].lower()
    
    # Now test uncertain price levels
    mock_client.models.generate_content.side_effect = None
    mock_response = MagicMock()
    mock_response.text = json.dumps({
        "has_sufficient_evidence": True,
        "support_levels": ["Unavailable"],
        "resistance_levels": ["Unclear"],
        "detected_trend": "neutral",
        "patterns": [],
        "reasoning": "Hard to say"
    })
    mock_client.models.generate_content.return_value = mock_response
    
    response2 = client.post("/api/v1/vision/analyze", files=files)
    assert response2.status_code == 200
    assert response2.json()["support_levels"] == ["Unavailable"]
