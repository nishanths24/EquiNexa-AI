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

@patch.dict(os.environ, {"GROQ_API_KEY": ""})
def test_vision_analyze_no_key():
    files = {'file': ('test.png', b'dummy', 'image/png')}
    response = client.post("/api/v1/vision/analyze", files=files)
    assert response.status_code == 501
    assert "LLM provider is not configured" in response.json()["detail"]

@patch.dict(os.environ, {"GROQ_API_KEY": "valid_key"})
def test_vision_analyze_invalid_image():
    files = {'file': ('test.png', b'not an image', 'image/png')}
    response = client.post("/api/v1/vision/analyze", files=files)
    assert response.status_code == 400
    assert "Invalid or corrupt" in response.json()["detail"]

@patch.dict(os.environ, {"GROQ_API_KEY": "valid_key"})
@patch("backend.app.api.main.get_groq_client")
def test_vision_analyze_success(mock_get_client):
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_response.choices = [mock_choice]
    mock_choice.message.content = json.dumps({
        "has_sufficient_evidence": True,
        "market_direction": {"bias": "bullish"},
        "trade_setup": {"entry_zone": "100"},
        "risk_assessment": {"volatility": "low"},
        "patterns": ["doji"]
    })
    mock_client.chat.completions.create.return_value = mock_response
    mock_get_client.return_value = mock_client
    
    # Create a real dummy image
    img = Image.new('RGB', (10, 10))
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    
    files = {'file': ('test.png', img_byte_arr.getvalue(), 'image/png')}
    response = client.post("/api/v1/vision/analyze", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert data["market_direction"]["bias"] == "bullish"
    assert "doji" in data["patterns"]

@patch("time.sleep", return_value=None)
@patch("yfinance.Ticker")
@patch.dict(os.environ, {"GROQ_API_KEY": "valid_key"})
@patch("backend.app.api.main.get_groq_client")
def test_research_query_quota_retry(mock_get_client, mock_ticker, mock_sleep):
    mock_ticker.return_value.info = {"exchange": "NMS", "currency": "USD"}
    mock_client = MagicMock()
    # Always fail with 429
    mock_client.chat.completions.create.side_effect = Exception("429 Too Many Requests: Quota exceeded")
    mock_get_client.return_value = mock_client
    
    body = {"ticker": "AAPL", "query": "Latest news?"}
    response = client.post("/api/v1/research/query", json=body)
    assert response.status_code == 429
    assert "quota or rate limit" in response.json()["detail"].lower()
    # It should have retried max_retries + 1 times for both primary and fallback models (8 times)
    assert mock_client.chat.completions.create.call_count == 8

@patch("time.sleep", return_value=None)
@patch("yfinance.Ticker")
@patch.dict(os.environ, {"GROQ_API_KEY": "valid_key", "GROQ_FALLBACK_MODEL": "fallback-model"})
@patch("backend.app.api.main.get_groq_client")
def test_research_query_fallback(mock_get_client, mock_ticker, mock_sleep):
    mock_ticker.return_value.info = {"exchange": "NMS", "currency": "USD"}
    mock_client = MagicMock()
    # Fail first model with 503, succeed second
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_response.choices = [mock_choice]
    mock_choice.message.content = json.dumps({
        "market_direction": {"bias": "bullish"},
        "trade_setup": {},
        "risk_assessment": {},
        "news_summary": "Fallback report.",
        "citations": [],
        "disclaimer": "Disclaimer"
    })
    
    call_count = 0
    def side_effect(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if kwargs.get('model') != "fallback-model":
            raise Exception("503 Unavailable")
        return mock_response
        
    mock_client.chat.completions.create.side_effect = side_effect
    mock_get_client.return_value = mock_client
    
    body = {"ticker": "AAPL", "query": "Latest news?"}
    response = client.post("/api/v1/research/query", json=body)
    assert response.status_code == 200
    assert response.json()["news_summary"] == "Fallback report."

@patch("time.sleep", return_value=None)
@patch("yfinance.Ticker")
@patch.dict(os.environ, {"GROQ_API_KEY": "valid_key", "GROQ_FALLBACK_MODEL": "fallback-model"})
@patch("backend.app.api.main.get_groq_client")
def test_research_query_fallback_fail(mock_get_client, mock_ticker, mock_sleep):
    mock_ticker.return_value.info = {"exchange": "NMS", "currency": "USD"}
    mock_client = MagicMock()
    # Fail both models with 404
    mock_client.chat.completions.create.side_effect = Exception("404 Not Found")
    mock_get_client.return_value = mock_client
    
    body = {"ticker": "AAPL", "query": "Latest news?"}
    response = client.post("/api/v1/research/query", json=body)
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
    
@patch("time.sleep", return_value=None)
@patch("yfinance.Ticker")
@patch.dict(os.environ, {"GROQ_API_KEY": "valid_key"})
@patch("backend.app.api.main.get_groq_client")
def test_research_query_fail_fast(mock_get_client, mock_ticker, mock_sleep):
    mock_ticker.return_value.info = {"exchange": "NMS", "currency": "USD"}
    mock_client = MagicMock()
    # Fail with 400 Bad Request
    mock_client.chat.completions.create.side_effect = Exception("400 Bad Request")
    mock_get_client.return_value = mock_client
    
    body = {"ticker": "AAPL", "query": "Latest news?"}
    response = client.post("/api/v1/research/query", json=body)
    assert response.status_code == 500
    assert "provider api request failed" in response.json()["detail"].lower()
    # Should not retry
    assert mock_client.chat.completions.create.call_count == 1
    
@patch("yfinance.Ticker")
@patch.dict(os.environ, {"GROQ_API_KEY": "valid_key"})
@patch("backend.app.api.main.get_groq_client")
def test_research_query_success(mock_get_client, mock_ticker):
    mock_ticker.return_value.info = {"exchange": "NMS", "currency": "USD"}
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_response.choices = [mock_choice]
    mock_choice.message.content = json.dumps({
        "market_direction": {"bias": "bullish"},
        "trade_setup": {},
        "risk_assessment": {},
        "news_summary": "AAPL is doing well.",
        "citations": ["News"],
        "disclaimer": "Not advice."
    })
    mock_client.chat.completions.create.return_value = mock_response
    mock_get_client.return_value = mock_client
    
    body = {"ticker": "AAPL", "query": "Latest news?"}
    response = client.post("/api/v1/research/query", json=body)
    assert response.status_code == 200
    data = response.json()
    assert data["news_summary"] == "AAPL is doing well."
    
@patch("time.sleep", return_value=None)
@patch("yfinance.Ticker")
@patch.dict(os.environ, {"GROQ_API_KEY": "valid_key"})
@patch("backend.app.api.main.get_groq_client")
def test_research_query_fenced_json(mock_get_client, mock_ticker, mock_sleep):
    mock_ticker.return_value.info = {"exchange": "NMS", "currency": "USD"}
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_response.choices = [mock_choice]
    mock_choice.message.content = '```json\n{"market_direction": {"bias": "bullish"}, "trade_setup": {}, "risk_assessment": {}, "news_summary": "Test", "citations": [], "disclaimer": "Test"}\n```'
    mock_client.chat.completions.create.return_value = mock_response
    mock_get_client.return_value = mock_client
    
    body = {"ticker": "AAPL", "query": "Test"}
    response = client.post("/api/v1/research/query", json=body)
    assert response.status_code == 200
    assert response.json()["news_summary"] == "Test"

@patch("time.sleep", return_value=None)
@patch("yfinance.Ticker")
@patch.dict(os.environ, {"GROQ_API_KEY": "valid_key"})
@patch("backend.app.api.main.get_groq_client")
def test_research_query_missing_fields(mock_get_client, mock_ticker, mock_sleep):
    mock_ticker.return_value.info = {"exchange": "NMS", "currency": "USD"}
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_response.choices = [mock_choice]
    mock_choice.message.content = '{"news_summary": "Test"}' # Missing citations and disclaimer
    mock_client.chat.completions.create.return_value = mock_response
    mock_get_client.return_value = mock_client
    
    body = {"ticker": "AAPL", "query": "Test"}
    response = client.post("/api/v1/research/query", json=body)
    assert response.status_code == 500
    assert "missing required field" in response.json()["detail"].lower()

@patch("time.sleep", return_value=None)
@patch("yfinance.Ticker")
@patch.dict(os.environ, {"GROQ_API_KEY": "valid_key"})
@patch("backend.app.api.main.get_groq_client")
def test_research_query_malformed_json(mock_get_client, mock_ticker, mock_sleep):
    mock_ticker.return_value.info = {"exchange": "NMS", "currency": "USD"}
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_response.choices = [mock_choice]
    mock_choice.message.content = '{broken json'
    mock_client.chat.completions.create.return_value = mock_response
    mock_get_client.return_value = mock_client
    
    body = {"ticker": "AAPL", "query": "Test"}
    response = client.post("/api/v1/research/query", json=body)
    assert response.status_code == 500
    assert "malformed json" in response.json()["detail"].lower()

@patch("time.sleep", return_value=None)
@patch("yfinance.Ticker")
@patch.dict(os.environ, {"GROQ_API_KEY": "valid_key"})
@patch("backend.app.api.main.get_groq_client")
def test_research_query_empty_response(mock_get_client, mock_ticker, mock_sleep):
    mock_ticker.return_value.info = {"exchange": "NMS", "currency": "USD"}
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_response.choices = [mock_choice]
    mock_choice.message.content = '   '
    mock_client.chat.completions.create.return_value = mock_response
    mock_get_client.return_value = mock_client
    
    body = {"ticker": "AAPL", "query": "Test"}
    response = client.post("/api/v1/research/query", json=body)
    assert response.status_code == 500
    assert "empty response" in response.json()["detail"].lower()

@patch("yfinance.Search")
@patch("yfinance.Ticker")
@patch.dict(os.environ, {"GROQ_API_KEY": "valid_key"})
def test_research_query_ambiguous_ticker(mock_ticker, mock_search):
    mock_ticker.return_value.info = {}
    mock_search.return_value.quotes = [{"symbol": "TATASTEEL.NS"}, {"symbol": "TATAMOTORS.NS"}]
    
    body = {"ticker": "TATA", "query": "Test"}
    response = client.post("/api/v1/research/query", json=body)
    assert response.status_code == 409
    assert "ambiguous" in response.json()["detail"].lower()
    
@patch("yfinance.Search")
@patch("yfinance.Ticker")
@patch.dict(os.environ, {"GROQ_API_KEY": "valid_key"})
def test_research_query_404_ticker(mock_ticker, mock_search):
    mock_ticker.return_value.info = {}
    mock_search.return_value.quotes = []
    
    body = {"ticker": "INVALID", "query": "Test"}
    response = client.post("/api/v1/research/query", json=body)
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
    
@patch("yfinance.Ticker")
@patch.dict(os.environ, {"GROQ_API_KEY": "valid_key"})
@patch("backend.app.api.main.get_groq_client")
def test_research_query_missing_market_data(mock_get_client, mock_ticker):
    # Mock yfinance to raise an exception indicating missing data
    mock_ticker.side_effect = Exception("Some connection error")
    
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_response.choices = [mock_choice]
    mock_choice.message.content = json.dumps({
        "market_direction": {"bias": "neutral"},
        "trade_setup": {},
        "risk_assessment": {},
        "news_summary": "I could not verify current prices.",
        "citations": ["Unverified"],
        "disclaimer": "Not advice."
    })
    mock_client.chat.completions.create.return_value = mock_response
    mock_get_client.return_value = mock_client
    
    body = {"ticker": "AAPL", "query": "Latest news?"}
    response = client.post("/api/v1/research/query", json=body)
    assert response.status_code == 200
    assert "I could not verify" in response.json()["news_summary"]

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
@patch.dict(os.environ, {"GROQ_API_KEY": "valid_key", "GROQ_VISION_MODEL": "qwen/qwen3.8-27b", "GROQ_VISION_FALLBACK_MODEL": "qwen/qwen3.8-27b"})
@patch("backend.app.api.main.get_groq_client")
def test_vision_analyze_retry_timeout(mock_get_client, mock_sleep):
    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = Exception("504 Gateway Timeout")
    mock_get_client.return_value = mock_client
    
    img = Image.new('RGB', (10, 10))
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    
    files = {'file': ('test.png', img_byte_arr.getvalue(), 'image/png')}
    response = client.post("/api/v1/vision/analyze", files=files)
    
    assert response.status_code == 504
    assert "timed out" in response.json()["detail"].lower()
    # verify retries happened (model + fallback deduplicated = 4 times)
    assert mock_client.chat.completions.create.call_count == 4

@patch("asyncio.sleep", return_value=None)
@patch.dict(os.environ, {"GROQ_API_KEY": "valid_key", "GROQ_VISION_MODEL": "qwen/qwen3.8-27b", "GROQ_VISION_FALLBACK_MODEL": "qwen/qwen3.8-27b"})
@patch("backend.app.api.main.get_groq_client")
def test_vision_analyze_quota_failure_and_uncertain_prices(mock_get_client, mock_sleep):
    mock_client = MagicMock()
    # Mock to throw 429
    mock_client.chat.completions.create.side_effect = Exception("429 Too Many Requests")
    mock_get_client.return_value = mock_client
    
    img = Image.new('RGB', (10, 10))
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    files = {'file': ('test.png', img_byte_arr.getvalue(), 'image/png')}
    
    response = client.post("/api/v1/vision/analyze", files=files)
    assert response.status_code == 429
    assert "quota or rate limit" in response.json()["detail"].lower()
    
    # Now test uncertain price levels
    mock_client.chat.completions.create.side_effect = None
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_response.choices = [mock_choice]
    mock_choice.message.content = json.dumps({
        "has_sufficient_evidence": True,
        "market_direction": {"bias": "neutral"},
        "trade_setup": {"entry_zone": "Unavailable"},
        "risk_assessment": {"volatility": "Unclear"},
        "patterns": []
    })
    mock_client.chat.completions.create.return_value = mock_response
    
    response2 = client.post("/api/v1/vision/analyze", files=files)
    assert response2.status_code == 200
    assert response2.json()["trade_setup"]["entry_zone"] == "Unavailable"

# ─── Image-mode regression tests ──────────────────────────────────────────────

def _make_upload(mode: str, size=(32, 32), fmt='PNG'):
    """Helper: create a minimal in-memory image and return multipart file tuple."""
    if mode == 'P':
        img = Image.new('RGB', size, (100, 150, 200)).quantize()
    else:
        img = Image.new(mode, size, 0 if mode == '1' else (100, 150, 200, 128) if 'A' in mode else (100, 150, 200))
    buf = BytesIO()
    img.save(buf, format=fmt)
    return ('file', (f'test.{fmt.lower()}', buf.getvalue(), f'image/{fmt.lower()}'))


@patch("asyncio.sleep", return_value=None)
@patch.dict(os.environ, {"GROQ_API_KEY": "valid_key", "GROQ_VISION_MODEL": "qwen/qwen3.8-27b", "GROQ_VISION_FALLBACK_MODEL": "qwen/qwen3.8-27b"})
@patch("backend.app.api.main.get_groq_client")
def test_vision_rgba_image_converts_without_error(mock_get_client, mock_sleep):
    """RGBA PNG (common for browser screenshots) must not raise 'cannot write mode RGBA as JPEG'."""
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_response.choices = [mock_choice]
    mock_choice.message.content = json.dumps({
        "has_sufficient_evidence": True,
        "market_direction": {"bias": "bullish", "evidence": "test", "alternative": "n/a", "confidence": "low"},
        "trade_setup": {"entry_zone": "Unavailable", "stop_loss": "Unavailable", "targets": [], "risk_reward": "Unavailable", "invalidation": "n/a", "timeframe": "n/a"},
        "risk_assessment": {"volatility": "low", "key_levels": "n/a", "avoid_reasons": "n/a", "is_uncertain": True},
        "patterns": []
    })
    mock_client.chat.completions.create.return_value = mock_response
    mock_get_client.return_value = mock_client

    files = [_make_upload('RGBA')]
    response = client.post("/api/v1/vision/analyze", files=files)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"


@patch("asyncio.sleep", return_value=None)
@patch.dict(os.environ, {"GROQ_API_KEY": "valid_key", "GROQ_VISION_MODEL": "qwen/qwen3.8-27b", "GROQ_VISION_FALLBACK_MODEL": "qwen/qwen3.8-27b"})
@patch("backend.app.api.main.get_groq_client")
def test_vision_grayscale_image_converts_without_error(mock_get_client, mock_sleep):
    """Grayscale 'L' mode images must be converted to RGB for JPEG encoding."""
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_response.choices = [mock_choice]
    mock_choice.message.content = json.dumps({
        "has_sufficient_evidence": False,
        "market_direction": {"bias": "neutral", "evidence": "grey image", "alternative": "n/a", "confidence": "n/a"},
        "trade_setup": {"entry_zone": "Unavailable", "stop_loss": "Unavailable", "targets": [], "risk_reward": "Unavailable", "invalidation": "n/a", "timeframe": "n/a"},
        "risk_assessment": {"volatility": "n/a", "key_levels": "n/a", "avoid_reasons": "n/a", "is_uncertain": True},
        "patterns": []
    })
    mock_client.chat.completions.create.return_value = mock_response
    mock_get_client.return_value = mock_client

    img = Image.new('L', (32, 32), 128)  # Grayscale
    buf = BytesIO()
    img.save(buf, format='PNG')
    files = [('file', ('grey.png', buf.getvalue(), 'image/png'))]
    response = client.post("/api/v1/vision/analyze", files=files)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"


@patch("asyncio.sleep", return_value=None)
@patch.dict(os.environ, {"GROQ_API_KEY": "valid_key", "GROQ_VISION_MODEL": "qwen/qwen3.8-27b", "GROQ_VISION_FALLBACK_MODEL": "qwen/qwen3.8-27b"})
@patch("backend.app.api.main.get_groq_client")
def test_vision_palette_image_converts_without_error(mock_get_client, mock_sleep):
    """Palette-mode 'P' PNG images must be converted to RGB for JPEG encoding."""
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_response.choices = [mock_choice]
    mock_choice.message.content = json.dumps({
        "has_sufficient_evidence": False,
        "market_direction": {"bias": "neutral", "evidence": "palette image", "alternative": "n/a", "confidence": "n/a"},
        "trade_setup": {"entry_zone": "Unavailable", "stop_loss": "Unavailable", "targets": [], "risk_reward": "Unavailable", "invalidation": "n/a", "timeframe": "n/a"},
        "risk_assessment": {"volatility": "n/a", "key_levels": "n/a", "avoid_reasons": "n/a", "is_uncertain": True},
        "patterns": []
    })
    mock_client.chat.completions.create.return_value = mock_response
    mock_get_client.return_value = mock_client

    files = [_make_upload('P')]
    response = client.post("/api/v1/vision/analyze", files=files)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"


@patch.dict(os.environ, {"GROQ_API_KEY": "valid_key"})
def test_vision_invalid_file_type_rejected():
    """Non-image files must return 400."""
    files = [('file', ('test.pdf', b'%PDF-1.4 fake content', 'application/pdf'))]
    response = client.post("/api/v1/vision/analyze", files=files)
    assert response.status_code == 400
    assert "unsupported file format" in response.json()["detail"].lower()


@patch("asyncio.sleep", return_value=None)
@patch.dict(os.environ, {"GROQ_API_KEY": "valid_key", "GROQ_VISION_MODEL": "qwen/qwen3.8-27b", "GROQ_VISION_FALLBACK_MODEL": "qwen/qwen3.8-27b"})
@patch("backend.app.api.main.get_groq_client")
def test_vision_unsupported_model_returns_404(mock_get_client, mock_sleep):
    """When all configured models respond with 404, backend must return 404."""
    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = Exception("404 model not found")
    mock_get_client.return_value = mock_client

    img = Image.new('RGB', (32, 32))
    buf = BytesIO()
    img.save(buf, format='PNG')
    files = [('file', ('test.png', buf.getvalue(), 'image/png'))]
    response = client.post("/api/v1/vision/analyze", files=files)
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


@patch("asyncio.sleep", return_value=None)
@patch.dict(os.environ, {"GROQ_API_KEY": "valid_key", "GROQ_VISION_MODEL": "qwen/qwen3.8-27b", "GROQ_VISION_FALLBACK_MODEL": "qwen/qwen3.8-27b"})
@patch("backend.app.api.main.get_groq_client")
def test_vision_malformed_model_output_returns_500(mock_get_client, mock_sleep):
    """Malformed JSON from the model must return 500, not the original error string."""
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_response.choices = [mock_choice]
    mock_choice.message.content = "This is not JSON at all!"
    mock_client.chat.completions.create.return_value = mock_response
    mock_get_client.return_value = mock_client

    img = Image.new('RGB', (32, 32))
    buf = BytesIO()
    img.save(buf, format='PNG')
    files = [('file', ('test.png', buf.getvalue(), 'image/png'))]
    response = client.post("/api/v1/vision/analyze", files=files)
    assert response.status_code == 500

