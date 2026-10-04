import datetime
from dateutil.relativedelta import relativedelta
from typing import Tuple, Dict, Any
from backend.app.ai.marketdata.calendars import get_calendar

def resolve_preset_range(preset: str, exchange: str, ref_utc: datetime.datetime) -> Tuple[datetime.datetime, datetime.datetime]:
    """
    Resolves a preset string into an exchange-local snapped [start, end] UTC window.
    Presets: 1D, 5D, 1M, 3M, 6M, YTD, 1Y, 3Y, 5Y, MAX
    """
    cal = get_calendar(exchange)
    
    # Defaults to max lookback if not specified
    preset = preset.upper().replace('MO', 'M')
    if preset == "MAX":
        start = ref_utc - relativedelta(years=20)
        return start, ref_utc
        
    last_session = cal.get_last_completed_session(ref_utc)
    
    if preset == "1D":
        start_utc, end_utc = cal.get_session_window(last_session)
        # if the session is currently ongoing, end_utc might be in future compared to ref_utc.
        end_utc = min(end_utc, ref_utc)
        return start_utc, end_utc
        
    if preset == "5D":
        d = last_session
        sessions_found = 0
        while sessions_found < 4: # 1 (last) + 4 = 5
            d -= datetime.timedelta(days=1)
            if not cal.is_holiday_or_weekend(d):
                sessions_found += 1
        start_utc, _ = cal.get_session_window(d)
        _, end_utc = cal.get_session_window(last_session)
        end_utc = min(end_utc, ref_utc)
        return start_utc, end_utc
        
    # Month/Year presets
    deltas = {
        "1M": relativedelta(months=1),
        "3M": relativedelta(months=3),
        "6M": relativedelta(months=6),
        "1Y": relativedelta(years=1),
        "3Y": relativedelta(years=3),
        "5Y": relativedelta(years=5),
    }
    
    if preset in deltas:
        target_date = last_session - deltas[preset]
        # Snap to next valid session >= target_date
        d = target_date
        while cal.is_holiday_or_weekend(d):
            d += datetime.timedelta(days=1)
        start_utc, _ = cal.get_session_window(d)
        _, end_utc = cal.get_session_window(last_session)
        return start_utc, min(end_utc, ref_utc)
        
    if preset == "YTD":
        target_date = datetime.date(last_session.year, 1, 1)
        d = target_date
        while cal.is_holiday_or_weekend(d):
            d += datetime.timedelta(days=1)
        start_utc, _ = cal.get_session_window(d)
        _, end_utc = cal.get_session_window(last_session)
        return start_utc, min(end_utc, ref_utc)
        
    raise ValueError(f"Unknown range preset: {preset}")
