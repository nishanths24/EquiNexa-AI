import logging
from typing import List, Optional
from app.providers.interfaces.market_provider import MarketDataProvider
from app.providers.core.circuit_breaker import CircuitBreaker, CircuitBreakerOpenException

logger = logging.getLogger(__name__)

class ProviderManager:
    def __init__(self):
        self._providers: List[MarketDataProvider] = []
        self._circuit_breakers = {}

    def register_provider(self, provider: MarketDataProvider):
        self._providers.append(provider)
        self._circuit_breakers[provider.provider_name] = CircuitBreaker()

    async def get_quote(self, symbol: str):
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
