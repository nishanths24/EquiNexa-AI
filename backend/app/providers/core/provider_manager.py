import logging
from typing import List, Optional
from backend.app.providers.interfaces.market_provider import MarketDataProvider
from backend.app.providers.core.circuit_breaker import CircuitBreaker, CircuitBreakerOpenException
from backend.app.cache.cache_service import CacheService

logger = logging.getLogger(__name__)

class ProviderManager:
    def __init__(self, cache_service: CacheService = None):
        self._providers: List[MarketDataProvider] = []
        self._circuit_breakers = {}
        self._cache = cache_service or CacheService()

    def register_provider(self, provider: MarketDataProvider):
        self._providers.append(provider)
        self._circuit_breakers[provider.provider_name] = CircuitBreaker()

    async def _fetch_quote_from_providers(self, symbol: str):
        for provider in self._providers:
            cb = self._circuit_breakers[provider.provider_name]
            try:
                # Deterministic priority iteration
                return await cb.execute(provider.quote, symbol)
            except CircuitBreakerOpenException:
                logger.warning(f"Provider {provider.provider_name} circuit is OPEN. Falling back...")
                continue
            except Exception as e:
                logger.error(f"Provider {provider.provider_name} failed: {e}")
                continue
        raise Exception("All providers exhausted or unavailable.")

    async def get_quote(self, symbol: str):
        # 60 second cache to protect API limits
        return await self._cache.get_or_set(
            key=f"quote:{symbol}",
            fetch_func=lambda: self._fetch_quote_from_providers(symbol),
            ttl=60
        )
