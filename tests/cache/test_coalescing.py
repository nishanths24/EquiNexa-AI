import pytest
import asyncio
from backend.app.cache.cache_service import CacheService
from backend.app.providers.core.quota_manager import QuotaManager

@pytest.mark.asyncio
async def test_cache_coalescing():
    cache = CacheService()
    fetch_count = 0
    
    async def slow_fetch():
        nonlocal fetch_count
        fetch_count += 1
        await asyncio.sleep(0.1)  # Simulate network call latency
        return "data"
        
    # Launch 100 concurrent requests for the exact same key
    tasks = [cache.get_or_set("shared_key", slow_fetch) for _ in range(100)]
    results = await asyncio.gather(*tasks)
    
    # Assert all 100 users got the correct data
    assert all(r == "data" for r in results)
    
    # Phase 3 EXIT GATE ASSERTION: "100 users -> 1 provider call"
    assert fetch_count == 1
    
def test_quota_manager():
    qm = QuotaManager()
    qm.set_limit("twelvedata", limit_per_minute=2, limit_per_day=100)
    
    assert qm.check_and_consume("twelvedata") == True
    assert qm.check_and_consume("twelvedata") == True
    # 3rd request in the same minute should be rejected
    assert qm.check_and_consume("twelvedata") == False
    
    assert qm.check_and_consume("unlimited_provider") == True
