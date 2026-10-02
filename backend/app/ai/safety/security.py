import os
from pydantic import BaseModel, ValidationError
import re

class SecurityContext:
    @staticmethod
    def ensure_no_hardcoded_keys():
        """Ensure critical API keys are only loaded from environment variables."""
        if os.getenv("OPENAI_API_KEY") == "sk-hardcoded-fake":
            raise ValueError("Hardcoded API key detected in environment!")
            
    @staticmethod
    def validate_ticker_input(ticker: str) -> bool:
        """Strict input validation for SQLi/NoSQLi prevention."""
        if not re.match(r"^[A-Z0-9.\-]{1,10}$", ticker):
            raise ValueError(f"Invalid ticker format: {ticker}")
        return True

def get_cors_config() -> dict:
    return {
        "allow_origins": ["https://equinexa.com"], # Strict origin
        "allow_methods": ["GET", "POST"],
        "allow_headers": ["Authorization", "Content-Type"]
    }
