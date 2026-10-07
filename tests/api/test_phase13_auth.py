import pytest
from fastapi import FastAPI, Depends, HTTPException
from fastapi.testclient import TestClient
import jwt
from app.core.auth import get_current_user, get_current_admin, SUPABASE_JWT_SECRET

# Create a dummy app for testing the dependencies
app = FastAPI()

@app.get("/api/v2/user/profile")
def read_profile(user=Depends(get_current_user)):
    return {"status": "success", "user": user["sub"]}

@app.get("/api/v2/admin/metrics")
def read_metrics(admin=Depends(get_current_admin)):
    return {"status": "success", "metrics": "secure data"}

client = TestClient(app)

def create_mock_jwt(sub: str, role: str, audience: str = "authenticated") -> str:
    payload = {
        "sub": sub,
        "aud": audience,
        "user_metadata": {"role": role}
    }
    return jwt.encode(payload, SUPABASE_JWT_SECRET, algorithm="HS256")

def test_unauthorized_missing_token():
    """Phase 13 Exit Gate: unauthorized tests (Missing Token)"""
    response = client.get("/api/v2/user/profile")
    assert response.status_code == 401 # FastAPI HTTPBearer returns 401 when Not authenticated

def test_unauthorized_invalid_token():
    """Phase 13 Exit Gate: unauthorized tests (Invalid Token)"""
    headers = {"Authorization": "Bearer not.a.real.jwt"}
    response = client.get("/api/v2/user/profile", headers=headers)
    assert response.status_code == 401
    assert "Invalid token" in response.json()["detail"]

def test_authorized_user():
    """Valid standard user"""
    token = create_mock_jwt(sub="user123", role="user")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/v2/user/profile", headers=headers)
    assert response.status_code == 200
    assert response.json()["user"] == "user123"

def test_non_admin_hits_admin_route():
    """Phase 13 Exit Gate: non-admin hits admin route -> 403 Forbidden"""
    token = create_mock_jwt(sub="user123", role="user")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/v2/admin/metrics", headers=headers)
    assert response.status_code == 403
    assert response.json()["detail"] == "Admin privileges required"

def test_admin_hits_admin_route():
    """Valid admin user"""
    token = create_mock_jwt(sub="admin999", role="admin")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/v2/admin/metrics", headers=headers)
    assert response.status_code == 200
    assert response.json()["metrics"] == "secure data"
