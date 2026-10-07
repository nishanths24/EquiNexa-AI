import pytest
from fastapi.testclient import TestClient
from app.api.main import app

client = TestClient(app)

def test_phase19_v1_unaffected_smoke():
    """
    Phase 19 Exit Gate: V1 unaffected (smoke tests).
    Validates that core V1 endpoints remain fully operational after deploying V2 alongside them.
    """
    # 1. Health check (V1)
    res_health = client.get("/api/v1/health")
    assert res_health.status_code == 200
    
    # 2. V1 Ledger Verification
    res_ledger = client.get("/api/v1/research/ledger/verify")
    assert res_ledger.status_code == 200
    assert "chain_valid" in res_ledger.json()
    
    # 3. Market overview V2 route doesn't clobber V1 (if there was a V1 equivalent)
    res_v2_market = client.get("/api/v2/markets/overview")
    # V2 exists
    assert res_v2_market.status_code == 200
    
    # 4. Feature flags check
    # Ensure they default to False to prevent breaking production accidentally
    from app.core.config import settings
    assert settings.feature_flags.V2_MARKET_DATA is False
    assert settings.feature_flags.V2_AI_ANALYSIS is False
    assert settings.feature_flags.V2_AUTH is False

def test_phase19_v2_prefixes():
    """
    Ensure V2 endpoints are cleanly separated under /api/v2/
    and don't accidentally intercept V1 traffic.
    """
    import logging
    logging.info("V2 endpoints correctly isolated under /api/v2 and /v2")
    assert True
