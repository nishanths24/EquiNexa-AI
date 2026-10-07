import yfinance as yf
from datetime import datetime, timedelta
from typing import List
from app.models.domain.market import Quote, OHLCV, DataMetadata, MarketStatus
from app.providers.interfaces.market_provider import MarketDataProvider

class YFinanceAdapter(MarketDataProvider):
    @property
    def provider_name(self) -> str:
        return "yfinance"

    async def capabilities(self) -> dict:
        return {
            "supports_realtime": False,
            "supports_delayed": True,
            "supports_historical": True,
            "supports_public_display": False,
            "supports_commercial_use": False
        }

    async def quote(self, symbol: str) -> Quote:
        ticker = yf.Ticker(symbol)
        data = ticker.fast_info
        
        # fallback for missing info
        price = data.last_price if data.last_price is not None else 0.0
        prev_close = data.previous_close if data.previous_close is not None else price
        change = price - prev_close
        change_percent = (change / prev_close) if prev_close else 0.0
        
        meta = DataMetadata(
            symbol=symbol,
            provider=self.provider_name,
            market="US",
            currency="USD",
            timestamp=datetime.now(),
            retrieved_at=datetime.now(),
            data_status="DELAYED",
            source="yfinance",
            is_market_open=False
        )
        
        return Quote(
            price=price,
            change=change,
            change_percent=change_percent,
            high=data.day_high if data.day_high else price,
            low=data.day_low if data.day_low else price,
            volume=data.last_volume if data.last_volume else 0,
            meta=meta
        )

    async def ohlcv(self, symbol: str, timeframe: str, start: datetime, end: datetime) -> List[OHLCV]:
        ticker = yf.Ticker(symbol)
        # yfinance timeframe mapping: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
        # We need to map our standard timeframes to yf
        interval_map = {
            "1m": "1m", "5m": "5m", "15m": "15m", "30m": "30m",
            "1h": "1h", "1D": "1d", "1W": "1wk", "1M": "1mo"
        }
        yf_interval = interval_map.get(timeframe, "1d")
        
        df = ticker.history(start=start, end=end, interval=yf_interval)
        results = []
        for index, row in df.iterrows():
            meta = DataMetadata(
                symbol=symbol,
                provider=self.provider_name,
                market="US",
                currency="USD",
                timestamp=index.to_pydatetime() if hasattr(index, 'to_pydatetime') else datetime.now(),
                retrieved_at=datetime.now(),
                data_status="DELAYED",
                source="yfinance",
                is_market_open=False
            )
            results.append(OHLCV(
                timestamp=index.to_pydatetime() if hasattr(index, 'to_pydatetime') else datetime.now(),
                open=float(row['Open']),
                high=float(row['High']),
                low=float(row['Low']),
                close=float(row['Close']),
                volume=float(row['Volume']),
                meta=meta
            ))
        return results

    async def intraday(self, symbol: str) -> List[OHLCV]:
        return await self.ohlcv(symbol, "15m", datetime.now() - timedelta(days=1), datetime.now())

    async def historical(self, symbol: str) -> List[OHLCV]:
        return await self.ohlcv(symbol, "1D", datetime.now() - timedelta(days=365), datetime.now())

    async def search_symbols(self, query: str) -> List[dict]:
        return []

    async def company_profile(self, symbol: str) -> dict:
        return {}

    async def fundamentals(self, symbol: str) -> dict:
        return {}

    async def corporate_events(self, symbol: str) -> List[dict]:
        return []

    async def forex(self, pair: str) -> Quote:
        return await self.quote(pair)

    async def indices(self, index_symbol: str) -> Quote:
        return await self.quote(index_symbol)

    async def market_status(self, market: str) -> MarketStatus:
        meta = DataMetadata(
            symbol=market,
            provider=self.provider_name,
            market=market,
            currency="USD",
            timestamp=datetime.now(),
            retrieved_at=datetime.now(),
            data_status="DELAYED",
            source="yfinance",
            is_market_open=False
        )
        return MarketStatus(
            market=market,
            is_open=False,
            next_open=None,
            next_close=None,
            meta=meta
        )
