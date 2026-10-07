import datetime
from typing import List, Dict, Any

def aggregate_candles(candles: List[Dict[str, Any]], target_interval: str, calendar_obj) -> List[Dict[str, Any]]:
    """
    Aggregates lower timeframe candles (e.g. 1m) into a target interval (e.g. 5m, 1h).
    Handles session bucketing and partial buckets.
    """
    if not candles:
        return []
        
    # A mapping of interval string to minutes
    interval_mins = {
        "1m": 1, "5m": 5, "10m": 10, "15m": 15, "30m": 30, "1h": 60, "4h": 240
    }
    
    if target_interval not in interval_mins:
        return candles # Passthrough if not intraday aggregatable
        
    target_m = interval_mins[target_interval]
    
    buckets = {}
    
    for c in candles:
        # Time is ISO UTC string
        ts = datetime.datetime.fromisoformat(c['time'].replace('Z', '+00:00'))
        local_ts = ts.astimezone(calendar_obj.tz)
        session_date = local_ts.date()
        
        # Calculate bucket start time
        session_open_dt = datetime.datetime.combine(session_date, calendar_obj.open_time, tzinfo=calendar_obj.tz)
        
        # Minutes since session open
        delta = local_ts - session_open_dt
        minutes_since_open = int(delta.total_seconds() // 60)
        
        if minutes_since_open < 0:
            continue # Pre-market ignored
            
        bucket_index = minutes_since_open // target_m
        bucket_start_local = session_open_dt + datetime.timedelta(minutes=bucket_index * target_m)
        bucket_key = bucket_start_local.astimezone(datetime.timezone.utc).isoformat()
        
        if bucket_key not in buckets:
            buckets[bucket_key] = []
        buckets[bucket_key].append(c)
        
    # Finalize buckets
    aggregated = []
    sorted_keys = sorted(list(buckets.keys()))
    
    for key in sorted_keys:
        bucket_candles = buckets[key]
        bucket_start_dt = datetime.datetime.fromisoformat(key)
        local_bucket_start = bucket_start_dt.astimezone(calendar_obj.tz)
        local_session_close = datetime.datetime.combine(local_bucket_start.date(), calendar_obj.close_time, tzinfo=calendar_obj.tz)
        
        # Calculate expected length in minutes
        max_possible = min(target_m, int((local_session_close - local_bucket_start).total_seconds() // 60))
        
        is_partial = False
        if max_possible < target_m:
            is_partial = True
            
        aggregated.append({
            "time": key,
            "open": bucket_candles[0]['open'],
            "high": max(c['high'] for c in bucket_candles),
            "low": min(c['low'] for c in bucket_candles),
            "close": bucket_candles[-1]['close'],
            "volume": sum(c['volume'] for c in bucket_candles),
            "is_partial": is_partial,
            "constituents": len(bucket_candles)
        })
        
    return aggregated
