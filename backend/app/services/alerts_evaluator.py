import uuid
from typing import List, Dict, Any
from backend.app.models.domain.alerts import AlertRule, AlertEvent

def evaluate_price_alerts(rules: List[AlertRule], current_prices: Dict[str, float]) -> List[AlertEvent]:
    """
    Phase 14 Centralized Evaluator:
    Evaluates all active price rules across ALL users in a single pass 
    using the current market tick, rather than polling per-user.
    """
    triggered_events = []
    
    # Filter for active price rules
    price_rules = [r for r in rules if r.is_active and r.alert_type == "PRICE_CROSSES"]
    
    for rule in price_rules:
        current_price = current_prices.get(rule.symbol)
        if current_price is None:
            continue
            
        is_triggered = False
        if rule.condition == "ABOVE" and current_price >= rule.threshold:
            is_triggered = True
        elif rule.condition == "BELOW" and current_price <= rule.threshold:
            is_triggered = True
            
        if is_triggered:
            event = AlertEvent(
                id=str(uuid.uuid4()),
                rule_id=rule.id,
                user_id=rule.user_id,
                symbol=rule.symbol,
                message=f"{rule.symbol} crossed {rule.condition} {rule.threshold} (Current: {current_price})"
            )
            triggered_events.append(event)
            # In a real engine, we might set rule.is_active = False here for one-shot alerts.
            
    return triggered_events
