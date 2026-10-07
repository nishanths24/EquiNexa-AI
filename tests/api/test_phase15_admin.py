import pytest
import os
from fastapi.testclient import TestClient
from app.api.main import app
import jwt

client = TestClient(app)

# Dummy secret must match the fallback in auth.py
DUMMY_SECRET = os.getenv("SUPABASE_JWT_SECRET", "super-secret-jwt-token-with-at-least-32-characters-long")

def create_token(role: str) -> str:
    payload = {
        "sub": "test_user_123",
        "aud": "authenticated",
        "user_metadata": {"role": role}
    }
    return jwt.encode(payload, DUMMY_SECRET, algorithm="HS256")

def test_admin_routes_rbac_verified():
    """
    Phase 15 Exit Gate: RBAC verified for Admin dashboard routes.
    """
    # 1. Unauthorized (No token)
    response = client.get("/api/v2/admin/health/providers")
    assert response.status_code == 401
    
    # 2. Regular User (Forbidden)
    user_token = create_token("user")
    headers = {"Authorization": f"Bearer {user_token}"}
    response = client.get("/api/v2/admin/health/providers", headers=headers)
    assert response.status_code == 403
    assert "Admin privileges required" in response.text
    
    # 3. Admin User (Allowed)
    admin_token = create_token("admin")
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    response_health = client.get("/api/v2/admin/health/providers", headers=headers)
    assert response_health.status_code == 200
    assert "twelvedata" in response_health.json()["data"]
    
    response_metrics = client.get("/api/v2/admin/metrics/usage", headers=headers)
    assert response_metrics.status_code == 200
    assert "cache_hit_ratio" in response_metrics.json()["data"]
