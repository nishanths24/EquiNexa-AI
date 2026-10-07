import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from datetime import datetime
from app.models.domain.market import Quote, DataMetadata
from app.providers.interfaces.market_provider import MarketDataProvider
from app.providers.core.circuit_breaker import CircuitBreaker, CircuitState, CircuitBreakerOpenException
from app.providers.core.provider_manager import ProviderManager

# Import the new adapters
from app.providers.adapters.yfinance_adapter import YFinanceAdapter
from app.providers.adapters.twelvedata_adapter import TwelveDataAdapter
from app.providers.adapters.alphavantage_adapter import AlphaVantageAdapter

class MockProvider(MarketDataProvider):
    @property
    def provider_name(self) -> str:
        return "mock_provider"
        
    async def capabilities(self) -> dict:
        return {"supports_realtime": True}
        
    async def quote(self, symbol: str) -> Quote:
        return Quote(
            price=100.0,
            change=1.0,
            change_percent=1.0,
            high=105.0,
            low=95.0,
            volume=10000.0,
            meta=DataMetadata(
                symbol=symbol,
                provider=self.provider_name,
                market="TEST",
                currency="USD",
                timestamp=datetime.now(),
                retrieved_at=datetime.now(),
                data_status="REALTIME",
                source="mock",
                is_market_open=True
            )
        )
        
    async def ohlcv(self, symbol, timeframe, start, end): pass
    async def intraday(self, symbol): pass
    async def historical(self, symbol): pass
    async def search_symbols(self, query): pass
    async def company_profile(self, symbol): pass
    async def fundamentals(self, symbol): pass
    async def corporate_events(self, symbol): pass
    async def forex(self, pair): pass
    async def indices(self, index_symbol): pass
    async def market_status(self, market): pass

class FailingProvider(MockProvider):
    @property
    def provider_name(self) -> str:
        return "failing_provider"
        
    async def quote(self, symbol: str) -> Quote:
        raise ValueError("Simulated provider failure")

@pytest.mark.asyncio
async def test_circuit_breaker():
    cb = CircuitBreaker(failure_threshold=2, recovery_timeout=0.1)
    async def fail(): raise ValueError("Fail")
    
    with pytest.raises(ValueError):
        await cb.execute(fail)
    assert cb.state == CircuitState.CLOSED
    
    with pytest.raises(ValueError):
        await cb.execute(fail)
    assert cb.state == CircuitState.OPEN
    
    with pytest.raises(CircuitBreakerOpenException):
        await cb.execute(fail)
        
@pytest.mark.asyncio
async def test_provider_manager_fallback():
    pm = ProviderManager()
    pm.register_provider(FailingProvider())
    pm.register_provider(MockProvider())
    
    quote = await pm.get_quote("AAPL")
    assert quote.meta.provider == "mock_provider"

@pytest.fixture
def mock_httpx_client():
    with patch("httpx.AsyncClient") as mock_client:
        mock_instance = AsyncMock()
        mock_client.return_value.__aenter__.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def mock_yfinance():
    with patch("yfinance.Ticker") as mock_ticker:
        mock_instance = MagicMock()
        mock_instance.fast_info.last_price = 150.0
        mock_instance.fast_info.previous_close = 145.0
        mock_instance.fast_info.day_high = 155.0
        mock_instance.fast_info.day_low = 140.0
        mock_instance.fast_info.last_volume = 1000000
        mock_ticker.return_value = mock_instance
        yield mock_ticker

@pytest.mark.asyncio
async def test_yfinance_adapter_contract(mock_yfinance):
    adapter = YFinanceAdapter()
    quote = await adapter.quote("AAPL")
    assert quote.price == 150.0
    assert quote.change == 5.0
    assert quote.meta.provider == "yfinance"

@pytest.mark.asyncio
async def test_twelvedata_adapter_contract(mock_httpx_client):
    adapter = TwelveDataAdapter(api_key="test")
    
    # Mock HTTP response
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "symbol": "AAPL",
        "close": "150.0",
        "change": "5.0",
        "percent_change": "3.33",
        "high": "155.0",
        "low": "140.0",
        "volume": "1000000"
    }
    mock_httpx_client.get.return_value = mock_response
    
    quote = await adapter.quote("AAPL")
    assert quote.price == 150.0
    assert quote.change == 5.0
    assert quote.meta.provider == "twelvedata"

@pytest.mark.asyncio
async def test_alphavantage_adapter_contract(mock_httpx_client):
    adapter = AlphaVantageAdapter(api_key="test")
    
    # Mock HTTP response
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "Global Quote": {
            "01. symbol": "AAPL",
            "05. price": "150.0",
            "09. change": "5.0",
            "10. change percent": "3.33%",
            "03. high": "155.0",
            "04. low": "140.0",
            "06. volume": "1000000"
        }
    }
    mock_httpx_client.get.return_value = mock_response
    
    quote = await adapter.quote("AAPL")
    assert quote.price == 150.0
    assert quote.change == 5.0
    assert quote.meta.provider == "alphavantage"

