import asyncio
import time
from typing import Any, Callable, Dict

class CacheService:
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._futures: Dict[str, asyncio.Future] = {}
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> Any:
        entry = self._cache.get(key)
        if entry:
            if time.time() > entry["expires_at"]:
                del self._cache[key]
                return None
            return entry["value"]
        return None

    async def set(self, key: str, value: Any, ttl: int = 60) -> None:
        self._cache[key] = {
            "value": value,
            "expires_at": time.time() + ttl
        }

    async def get_or_set(self, key: str, fetch_func: Callable, ttl: int = 60) -> Any:
        # 1. Check cache first
        cached_value = await self.get(key)
        if cached_value is not None:
            return cached_value

        # 2. Check if a fetch is already in progress (Coalescing)
        async with self._lock:
            # Check cache again inside lock just in case it was set
            cached_value = self._cache.get(key)
            if cached_value and time.time() <= cached_value["expires_at"]:
                return cached_value["value"]

            if key in self._futures:
                future = self._futures[key]
                is_fetcher = False
            else:
                future = asyncio.Future()
                self._futures[key] = future
                is_fetcher = True

        # 3. Await the existing future or fetch the data
        if not is_fetcher:
            return await future

        try:
            result = await fetch_func()
            await self.set(key, result, ttl)
            future.set_result(result)
            return result
        except Exception as e:
            future.set_exception(e)
            raise e
        finally:
            async with self._lock:
                self._futures.pop(key, None)
