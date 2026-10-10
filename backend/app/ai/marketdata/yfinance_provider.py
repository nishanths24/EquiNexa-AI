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
        info = ticker.info or {}
        fi = getattr(ticker, 'fast_info', None)
        ex = info.get('exchange') if isinstance(info.get('exchange'), str) else None
        if not ex and fi:
            fi_ex = getattr(fi, 'exchange', None)
            if isinstance(fi_ex, str):
                ex = fi_ex
        curr = info.get('currency') if isinstance(info.get('currency'), str) else None
        if not curr and fi:
            fi_curr = getattr(fi, 'currency', None)
            if isinstance(fi_curr, str):
                curr = fi_curr
        return {
            'symbol': symbol,
            'exchange': ex or '',
            'currency': curr or '',
            'timezone': info.get('exchangeTimezoneName') or (getattr(fi, 'timezone', '') if isinstance(getattr(fi, 'timezone', None), str) else ''),
            'instrument_type': info.get('quoteType') or (getattr(fi, 'quote_type', '') if isinstance(getattr(fi, 'quote_type', None), str) else ''),
            'data_source': 'yfinance',
            'fetched_at': datetime.utcnow().isoformat()
        }
