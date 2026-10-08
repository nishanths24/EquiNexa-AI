from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import time
from typing import Dict, Tuple

# Simple in-memory rate limiter (for Phase 17 demonstration)
# ip -> (request_count, window_start_time)
_rate_limits: Dict[str, Tuple[int, float]] = {}

WINDOW_SIZE_SECONDS = 60
ANONYMOUS_LIMIT = 30
AUTH_LIMIT = 100

def check_rate_limit(request: Request):
    """Phase 17: Simple in-memory rate limiter dependency."""
    client_ip = request.client.host if request.client else "unknown"
    is_authenticated = "Authorization" in request.headers
    
    limit = AUTH_LIMIT if is_authenticated else ANONYMOUS_LIMIT
    
    current_time = time.time()
    count, window_start = _rate_limits.get(client_ip, (0, current_time))
    
    if current_time - window_start > WINDOW_SIZE_SECONDS:
        # Reset window
        count = 1
        window_start = current_time
    else:
        count += 1
        
    if count > limit:
        raise HTTPException(
            status_code=429,
            detail="Too Many Requests",
            headers={"Retry-After": str(int(WINDOW_SIZE_SECONDS - (current_time - window_start)))}
        )
        
    _rate_limits[client_ip] = (count, window_start)

async def add_security_headers_middleware(request: Request, call_next):
    """Phase 17: Security headers middleware."""
    response = await call_next(request)
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response
