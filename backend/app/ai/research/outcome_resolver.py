from datetime import datetime, timedelta, timezone
from typing import List, Dict
import pandas as pd
from backend.app.ai.schemas.prediction import OutcomeSnapshot

class TradingCalendar:
    @staticmethod
    def get_trading_days_passed(market: str, start: datetime, end: datetime) -> int:
        """
        Calculate trading days between start and end.
        For Phase 8.1 we approximate by counting weekdays and stripping standard holidays if possible.
        A production implementation would use pandas_market_calendars (US) or nsepy (India).
        """
        # Mock calculation: count weekdays
        days = 0
        current = start + timedelta(days=1)
        while current <= end:
            if current.weekday() < 5: # Monday-Friday
                days += 1
            current += timedelta(days=1)
        return days

class OutcomeResolver:
    def __init__(self, ledger, market_data_provider):
        self.ledger = ledger
        self.market_data_provider = market_data_provider
        
    def resolve_pending(self, current_time: datetime):
        pending = self.ledger.get_pending_predictions()
        
        for p in pending:
            pred_time = datetime.fromisoformat(p['prediction_timestamp'])
            
            # 1. Check Trading Calendar (Wait 5 trading days)
            trading_days_passed = TradingCalendar.get_trading_days_passed(p['market'], pred_time, current_time)
            
            horizon = p['target_definition'].get('horizon', 5)
            if trading_days_passed < horizon:
                continue # Still waiting
                
            # 2. Try to evaluate
            try:
                # Fetch data strictly up to current_time to see if we have T+5
                df = self.market_data_provider.fetch_live_data(p['ticker'])
                df = df[df.index <= current_time]
                
                # Check if we have the entry bar and the exit bar
                # Entry bar = the bar strictly at or just before pred_time
                entry_df = df[df.index <= pred_time]
                if len(entry_df) == 0:
                    continue # missing entry data
                entry_price = float(entry_df.iloc[-1]['close'])
                
                # Exit bar = the most recent bar (assuming trading_days_passed >= horizon)
                exit_price = float(df.iloc[-1]['close'])
                
                future_return = (exit_price / entry_price) - 1.0
                thresh = p['target_definition'].get('threshold', 0.02)
                
                actual_target = 1 if future_return > thresh else 0
                
                outcome = OutcomeSnapshot(
                    prediction_id=p['prediction_id'],
                    actual_forward_return=future_return,
                    actual_target=actual_target,
                    outcome_timestamp=current_time,
                    evaluation_status="EVALUATED"
                )
                self.ledger.record_outcome(outcome)
                
            except Exception as e:
                # Provider failure or missing data, remain pending or mark failed
                pass
