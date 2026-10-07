import datetime
from zoneinfo import ZoneInfo
from typing import Tuple, List, Optional

class TradingCalendar:
    def __init__(self, exchange: str, timezone_str: str):
        self.exchange = exchange
        self.tz = ZoneInfo(timezone_str)
        # Simplified default session hours
        if exchange == "NSE":
            self.open_time = datetime.time(9, 15)
            self.close_time = datetime.time(15, 30)
        else: # Default US NYSE/NASDAQ
            self.open_time = datetime.time(9, 30)
            self.close_time = datetime.time(16, 0)

    def is_holiday_or_weekend(self, dt: datetime.date) -> bool:
        # Simplistic implementation: weekends only for now
        return dt.weekday() >= 5
        
    def get_last_completed_session(self, ref_dt: datetime.datetime) -> datetime.date:
        """Returns the last completed trading session relative to ref_dt."""
        local_ref = ref_dt.astimezone(self.tz)
        current_date = local_ref.date()
        
        # If today is a trading day and we're past close, it's today
        if not self.is_holiday_or_weekend(current_date) and local_ref.time() >= self.close_time:
            return current_date
            
        # Otherwise, go back until a valid trading day
        d = current_date - datetime.timedelta(days=1)
        while self.is_holiday_or_weekend(d):
            d -= datetime.timedelta(days=1)
        return d
        
    def get_session_window(self, d: datetime.date) -> Tuple[datetime.datetime, datetime.datetime]:
        """Returns the start and end datetime of a session date in UTC."""
        dt_open = datetime.datetime.combine(d, self.open_time, tzinfo=self.tz)
        dt_close = datetime.datetime.combine(d, self.close_time, tzinfo=self.tz)
        return dt_open.astimezone(datetime.timezone.utc), dt_close.astimezone(datetime.timezone.utc)

def get_calendar(exchange: str) -> TradingCalendar:
    tz = "Asia/Kolkata" if exchange == "NSE" else "America/New_York"
    return TradingCalendar(exchange, tz)
