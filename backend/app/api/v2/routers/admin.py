from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any

from backend.app.core.auth import get_current_admin

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_current_admin)]
)

@router.get("/health/providers")
async def get_provider_health() -> Dict[str, Any]:
    """
    Phase 15: Admin Dashboard - Provider health
    Returns status, latency, last success/failure, quota, and circuit state.
    """
    # Mocked data for V2 architecture
    return {
        "status": "success",
        "data": {
            "twelvedata": {
                "status": "healthy",
                "latency_ms": 145,
                "circuit_state": "CLOSED",
                "quota_remaining": 750,
                "last_success": "2026-10-07T10:32:15Z",
                "last_failure": None
            },
            "finnhub": {
                "status": "degraded",
                "latency_ms": 850,
                "circuit_state": "HALF_OPEN",
                "quota_remaining": 42,
                "last_success": "2026-10-07T10:30:00Z",
                "last_failure": "2026-10-07T10:31:00Z"
            }
        }
    }

@router.get("/metrics/usage")
async def get_usage_metrics() -> Dict[str, Any]:
    """
    Phase 15: Admin Dashboard - API usage & metrics
    Returns API usage, cache hit ratio, DB health, error rate, active users.
    """
    return {
        "status": "success",
        "data": {
            "active_users_24h": 1240,
            "api_requests_24h": 45000,
            "error_rate_percent": 0.05,
            "cache_hit_ratio": 0.82,
            "db_health": "healthy",
            "ai_requests_24h": 1500
        }
    }
