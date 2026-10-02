import pytest
from backend.app.ai.caching.cache_manager import CacheManager, execute_with_fallback

def test_cache_manager():
    mgr = CacheManager()
    mgr.set("test_key", "test_val", ttl_seconds=10)
    assert mgr.get("test_key") == "test_val"
    
    # Test expiration by setting TTL to -1
    mgr.set("expired_key", "expired_val", ttl_seconds=-1)
    assert mgr.get("expired_key") is None

def test_fallback_execution():
    mgr = CacheManager()
    
    def fail_func():
        raise ValueError("API Offline")
        
    def backup_func():
        return "fallback_result"
        
    # Should use backup
    res = execute_with_fallback(fail_func, backup_func, mgr, "api_call")
    assert res == "fallback_result"
    
    def success_func():
        return "success_result"
        
    # Should use success and cache
    res2 = execute_with_fallback(success_func, backup_func, mgr, "api_call_2")
    assert res2 == "success_result"
    assert mgr.get("api_call_2") == "success_result"
