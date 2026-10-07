import os
from fastapi import Request, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from typing import Dict, Any

security = HTTPBearer()

# For local testing, we fallback to a dummy secret. In prod, this must match Supabase's JWT secret.
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET", "super-secret-jwt-token-with-at-least-32-characters-long")

def verify_supabase_jwt(token: str) -> Dict[str, Any]:
    """Verify Supabase JWT locally without network calls."""
    try:
        decoded = jwt.decode(
            token, 
            SUPABASE_JWT_SECRET, 
            algorithms=["HS256"], 
            audience="authenticated"
        )
        return decoded
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)) -> Dict[str, Any]:
    """Dependency for authenticated endpoints."""
    return verify_supabase_jwt(credentials.credentials)

def get_current_admin(user: Dict[str, Any] = Security(get_current_user)) -> Dict[str, Any]:
    """Dependency for RBAC admin endpoints."""
    # Checks a custom claim in user_metadata or app_metadata
    role = user.get("user_metadata", {}).get("role", "user")
    if role != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return user
