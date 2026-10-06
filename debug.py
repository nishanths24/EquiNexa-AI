import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from fastapi.testclient import TestClient
from backend.app.api.main import app

client = TestClient(app)

response = client.get("/api/v1/markets/history?ticker=^BSEN&period=3M&interval=1d")
print(response.status_code)
print(response.json())
