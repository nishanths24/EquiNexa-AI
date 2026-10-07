import json
import logging
from datetime import datetime, timezone

class JSONFormatter(logging.Formatter):
    """H3. Observability: Structured JSON logs"""
    def format(self, record):
        log_obj = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "request_id": getattr(record, "request_id", None),
            "endpoint": getattr(record, "endpoint", None),
            "user_id": getattr(record, "user_id", None),
            "provider": getattr(record, "provider", None),
            "error_code": getattr(record, "error_code", None),
            "latency_ms": getattr(record, "latency_ms", None),
        }
        # Filter out None values to keep logs clean
        log_obj = {k: v for k, v in log_obj.items() if v is not None}
        return json.dumps(log_obj)

def setup_logger():
    logger = logging.getLogger("equinexa_v2")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    if not logger.handlers:
        logger.addHandler(handler)
    return logger

logger = setup_logger()
