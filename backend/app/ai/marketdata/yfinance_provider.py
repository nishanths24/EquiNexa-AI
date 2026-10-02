import yfinance as yf
from datetime import datetime
import pandas as pd
from .market_data_provider import MarketDataProvider, PriceFrame
from typing import Optional

class YFinanceProvider(MarketDataProvider):
    def fetch_ohlcv(self, symbol: str, start: datetime, end: datetime, interval: str = '1d') -> PriceFrame:
        ticker = yf.Ticker(symbol)
        df = ticker.history(start=start, end=end, interval=interval, auto_adjust=False)
        
        if df.empty:
            return PriceFrame()
            
        # Rename columns to lowercase to match the spec
        df.reset_index(inplace=True)
        df.rename(columns={
            'Date': 'ts_local',
            'Datetime': 'ts_local',
            'Open': 'open',
            'High': 'high',
            'Low': 'low',
            'Close': 'close',
            'Volume': 'volume',
            'Adj Close': 'adj_close'
        }, inplace=True)
        
        # Ensure ts_utc exists
        if df['ts_local'].dt.tz is None:
            # yfinance usually returns timezone-aware datetimes, but just in case
            df['ts_utc'] = df['ts_local'].dt.tz_localize('UTC')
        else:
            df['ts_utc'] = df['ts_local'].dt.tz_convert('UTC')
            
        return PriceFrame(df)

    def get_metadata(self, symbol: str) -> dict:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        return {
            'symbol': symbol,
            'exchange': info.get('exchange', ''),
            'currency': info.get('currency', ''),
            'timezone': info.get('exchangeTimezoneName', ''),
            'instrument_type': info.get('quoteType', ''),
            'data_source': 'yfinance',
            'fetched_at': datetime.utcnow().isoformat()
        }
