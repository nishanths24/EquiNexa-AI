from datetime import datetime, timedelta, timezone

def validate_timestamp(published_at: datetime, ingested_at: datetime, max_future_skew_minutes: int = 5) -> bool:
    """
    Reject timestamps in the future relative to ingested_at.
    """
    if published_at.tzinfo is None:
        # Reject naive timestamps
        return False
        
    future_limit = ingested_at + timedelta(minutes=max_future_skew_minutes)
    if published_at > future_limit:
        return False
        
    return True
