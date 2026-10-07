import os
from pydantic_settings import BaseSettings

class FeatureFlags(BaseSettings):
    """H6: Feature Flags. Server-evaluated, default OFF until acceptance."""
    V2_MARKET_DATA: bool = False
    V2_AI_ANALYSIS: bool = False
    V2_NEWS: bool = False
    V2_FOREX: bool = False
    V2_FUNDAMENTALS: bool = False
    V2_ALERTS: bool = False
    V2_BACKTESTING: bool = False
    V2_AUTH: bool = False

    class Config:
        env_prefix = "FF_"

class Settings(BaseSettings):
    """H2: Security. CORS allowlist, no wildcard credentials."""
    FRONTEND_ORIGIN: str = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
    feature_flags: FeatureFlags = FeatureFlags()

settings = Settings()
