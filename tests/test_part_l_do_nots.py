import pytest
import os
import re

@pytest.mark.asyncio
async def test_do_not_weaken_cors():
    """Ensure we haven't reverted to wildcard CORS for credentials."""
    # We check the main.py file to ensure allow_origins=["*"] is not used with credentials
    main_py_path = os.path.join(os.path.dirname(__file__), "..", "backend", "app", "api", "main.py")
    if os.path.exists(main_py_path):
        with open(main_py_path, "r") as f:
            content = f.read()
            # If allow_credentials=True is present, allow_origins=["*"] must NOT be present
            if "allow_credentials=True" in content:
                assert 'allow_origins=["*"]' not in content, "PART L VIOLATION: CORS weakened with wildcard origins and credentials."

@pytest.mark.asyncio
async def test_do_not_hardcode_secrets():
    """Ensure no obvious API keys are hardcoded in the config or main."""
    # Simple regex to catch typical hardcoded keys like 'sk_live_...' or 'AIza...'
    # For now, we just assert our config file doesn't have a default value for API keys
    config_py_path = os.path.join(os.path.dirname(__file__), "..", "backend", "app", "core", "config.py")
    if os.path.exists(config_py_path):
        with open(config_py_path, "r") as f:
            content = f.read()
            assert "AIzaSy" not in content, "PART L VIOLATION: Hardcoded Google API key found."
            assert "sk-proj-" not in content, "PART L VIOLATION: Hardcoded OpenAI key found."

@pytest.mark.asyncio
async def test_do_not_remove_v1_features():
    """Ensure V1 routes still exist and haven't been deleted."""
    main_py_path = os.path.join(os.path.dirname(__file__), "..", "backend", "app", "api", "main.py")
    if os.path.exists(main_py_path):
        with open(main_py_path, "r") as f:
            content = f.read()
            assert '@app.get("/api/v1/health")' in content, "PART L VIOLATION: V1 features were needlessly removed."
            assert '@app.get("/api/v1/research/ledger/verify")' in content, "PART L VIOLATION: V1 features were needlessly removed."

@pytest.mark.asyncio
async def test_do_not_fabricate_data():
    """Ensure the V2 Market Overview router respects the UNAVAILABLE state rather than faking data."""
    router_path = os.path.join(os.path.dirname(__file__), "..", "backend", "app", "api", "v2", "routers", "market_overview.py")
    if os.path.exists(router_path):
        with open(router_path, "r") as f:
            content = f.read()
            # We explicitly check that exceptions in fetching cause a pass (omission), not a mocked return
            assert "pass" in content or "continue" in content, "PART L VIOLATION: Failed data requests must not return fabricated mock data."
            assert "random" not in content, "PART L VIOLATION: Random data fabrication detected."
