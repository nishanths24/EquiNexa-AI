from typing import Dict, Any
from backend.app.ai.trader.costs import CostCalculator
from backend.app.ai.trader.risk import RiskEngine

class ScenarioPlanner:
    def __init__(self):
        self.risk_engine = RiskEngine()
        
    def create_plan(self, ticker: str, direction: str, entry: float, stop_loss: float, target: float, capital: float, risk_pct: float = 1.0) -> Dict[str, Any]:
        """
        Validates and creates a trading plan. Refuses if invalidation (stop_loss) is missing.
        """
        if not stop_loss or stop_loss <= 0:
            return {"status": "error", "reason": "A valid Stop Loss (invalidation level) is strictly required."}
            
        if direction.upper() not in ["LONG", "SHORT"]:
            return {"status": "error", "reason": "Direction must be LONG or SHORT"}
            
        if direction.upper() == "LONG" and stop_loss >= entry:
            return {"status": "error", "reason": "For LONG, Stop Loss must be below Entry"}
            
        if direction.upper() == "SHORT" and stop_loss <= entry:
            return {"status": "error", "reason": "For SHORT, Stop Loss must be above Entry"}
            
        risk_res = self.risk_engine.calculate_position_size(capital, risk_pct, entry, stop_loss)
        if risk_res["status"] == "error":
            return risk_res
            
        qty = risk_res["quantity"]
        cost_calc = CostCalculator(is_intraday=True)
        entry_costs = cost_calc.calculate_costs(entry, qty)
        exit_costs = cost_calc.calculate_costs(target, qty)
        
        total_costs = entry_costs["total_estimated_cost"] + exit_costs["total_estimated_cost"]
        
        potential_profit = abs(target - entry) * qty
        net_profit = potential_profit - total_costs
        
        risk_amount = risk_res["risk_per_trade"]
        reward_risk_ratio = potential_profit / risk_amount if risk_amount > 0 else 0
        
        # P3: Cost as % of expected move
        cost_pct_of_move = (total_costs / potential_profit) * 100 if potential_profit > 0 else 100.0
        
        return {
            "status": "ok",
            "ticker": ticker,
            "direction": direction.upper(),
            "quantity": qty,
            "metrics": {
                "risk_amount": round(risk_amount, 2),
                "potential_profit": round(potential_profit, 2),
                "net_profit": round(net_profit, 2),
                "reward_risk_ratio": round(reward_risk_ratio, 2),
                "total_estimated_costs": round(total_costs, 2),
                "cost_pct_of_move": round(cost_pct_of_move, 2)
            }
        }
