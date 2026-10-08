import pytest
from backend.app.models.domain.alerts import AlertRule
from backend.app.services.alerts_evaluator import evaluate_price_alerts

def test_centralized_alert_evaluation():
    """
    Phase 14 Exit Gate: centralized evaluation, no per-user polling.
    We pass a global array of rules and a single market tick dictionary.
    """
    # 10,000 rules simulated in memory (simplified to 4 for the test)
    rules = [
        AlertRule(id="1", user_id="user_A", symbol="AAPL", alert_type="PRICE_CROSSES", condition="ABOVE", threshold=150.0),
        AlertRule(id="2", user_id="user_B", symbol="AAPL", alert_type="PRICE_CROSSES", condition="BELOW", threshold=140.0),
        AlertRule(id="3", user_id="user_C", symbol="TSLA", alert_type="PRICE_CROSSES", condition="ABOVE", threshold=200.0),
        AlertRule(id="4", user_id="user_D", symbol="MSFT", alert_type="PRICE_CROSSES", condition="ABOVE", threshold=350.0)
    ]
    
    # A single centralized market data tick is received
    current_prices = {
        "AAPL": 152.0, # Triggers rule 1 (ABOVE 150)
        "TSLA": 195.0, # Does not trigger rule 3 (Needs ABOVE 200)
        "MSFT": 355.0  # Triggers rule 4 (ABOVE 350)
    }
    
    # One pass evaluation
    events = evaluate_price_alerts(rules, current_prices)
    
    assert len(events) == 2
    triggered_rule_ids = [e.rule_id for e in events]
    assert "1" in triggered_rule_ids
    assert "4" in triggered_rule_ids
    assert "2" not in triggered_rule_ids
    assert "3" not in triggered_rule_ids
    
    # Verify the message formatting
    aapl_event = next(e for e in events if e.rule_id == "1")
    assert aapl_event.user_id == "user_A"
    assert "AAPL crossed ABOVE 150.0 (Current: 152.0)" in aapl_event.message
