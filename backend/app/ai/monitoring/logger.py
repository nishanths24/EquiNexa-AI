import logging
import json
from typing import Any, Dict
from datetime import datetime, timezone

class SafeJSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_obj = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name
        }
        
        if hasattr(record, "safe_context"):
            log_obj["context"] = getattr(record, "safe_context")
            
        return json.dumps(log_obj)

def get_ai_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(SafeJSONFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

def log_safe_prediction(logger: logging.Logger, ticker: str, direction: str, prob: float, req_id: str):
    """Logs prediction without exposing sensitive or uncalibrated details."""
    context = {
        "ticker": ticker,
        "direction": direction,
        "probability_bin": round(prob, 1), # binned for safety/noise
        "request_id": req_id
    }
    logger.info("Prediction generated", extra={"safe_context": context})
