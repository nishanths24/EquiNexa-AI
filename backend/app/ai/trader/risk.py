from typing import Dict, Any

class RiskEngine:
    """
    Position sizing and risk analytics.
    """
    def calculate_position_size(self, capital: float, risk_pct: float, entry: float, stop_loss: float) -> Dict[str, Any]:
        if entry <= 0 or stop_loss <= 0 or capital <= 0:
            return {"status": "error", "reason": "Invalid inputs"}
            
        if entry == stop_loss:
            return {"status": "error", "reason": "Entry and Stop Loss cannot be the same"}
            
        risk_per_trade = capital * (risk_pct / 100.0)
        risk_per_share = abs(entry - stop_loss)
        
        quantity = int(risk_per_trade // risk_per_share)
        
        if quantity == 0:
            return {"status": "error", "reason": "Risk tolerance too low for this stop loss distance"}
            
        return {
            "status": "ok",
            "quantity": quantity,
            "risk_per_trade": round(risk_per_trade, 2),
            "total_exposure": round(quantity * entry, 2)
        }
