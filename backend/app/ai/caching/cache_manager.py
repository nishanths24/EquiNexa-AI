from typing import Any, Optional, Dict
from datetime import datetime, timedelta, timezone

class CacheManager:
    def __init__(self):
        # In-memory dictionary for testing; use Redis in production
        self._cache: Dict[str, Dict[str, Any]] = {}
        
    def get(self, key: str) -> Optional[Any]:
        entry = self._cache.get(key)
        if not entry:
            return None
            
        if datetime.now(timezone.utc) > entry['expires_at']:
            del self._cache[key]
            return None
            
        return entry['value']
        
    def set(self, key: str, value: Any, ttl_seconds: int = 300):
        expires_at = datetime.now(timezone.utc) + timedelta(seconds=ttl_seconds)
        self._cache[key] = {
            'value': value,
            'expires_at': expires_at
        }
        
def execute_with_fallback(primary_func, fallback_func, cache_mgr: CacheManager, cache_key: str, ttl: int = 300):
    """
    Executes primary function. If it fails, tries fallback. Cache successful results.
    """
    cached = cache_mgr.get(cache_key)
    if cached is not None:
        return cached
        
    try:
        res = primary_func()
        cache_mgr.set(cache_key, res, ttl)
        return res
    except Exception as e:
        # Fallback to degraded mode
        try:
            res = fallback_func()
            return res
        except Exception:
            raise e
