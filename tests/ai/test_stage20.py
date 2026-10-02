import pytest
import logging
import io
import json
from backend.app.ai.monitoring.logger import get_ai_logger, log_safe_prediction

def test_safe_logging():
    logger = get_ai_logger("test_logger")
    
    # Capture output
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    from backend.app.ai.monitoring.logger import SafeJSONFormatter
    handler.setFormatter(SafeJSONFormatter())
    logger.handlers = [handler]
    
    log_safe_prediction(logger, "AAPL", "UP", 0.87, "req123")
    
    output = stream.getvalue()
    log_dict = json.loads(output)
    
    assert log_dict["level"] == "INFO"
    assert log_dict["context"]["ticker"] == "AAPL"
    assert log_dict["context"]["probability_bin"] == 0.9 # 0.87 rounded to 0.9
    assert "req123" in log_dict["context"]["request_id"]
