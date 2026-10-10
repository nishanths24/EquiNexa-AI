# Conftest to set pytest root and reset test fixtures
import pytest
from backend.app.core.security import _rate_limits

@pytest.fixture(autouse=True)
def reset_rate_limits():
    _rate_limits.clear()
    yield
    _rate_limits.clear()
