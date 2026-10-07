from typing import Dict

class RiskEngine:
    def __init__(self, account_size: float, max_portfolio_risk_pct: float = 0.02, max_position_pct: float = 0.1):
        self.account_size = account_size
        self.max_portfolio_risk_pct = max_portfolio_risk_pct
        self.max_position_pct = max_position_pct

    def compute_risk(self, entry_price: float, stop_loss: float, target: float) -> Dict:
        if entry_price <= 0 or stop_loss <= 0 or target <= 0:
            raise ValueError("Prices must be positive")
            
        is_long = target > entry_price
        
        if is_long and stop_loss >= entry_price:
            raise ValueError("Long stop loss must be below entry")
        if not is_long and stop_loss <= entry_price:
            raise ValueError("Short stop loss must be above entry")

        stop_distance = entry_price - stop_loss if is_long else stop_loss - entry_price
        risk_per_share = stop_distance
        
        if risk_per_share == 0:
            raise ValueError("Zero risk per share - invalid stop loss")
            
        target_distance = target - entry_price if is_long else entry_price - target
        risk_reward = target_distance / risk_per_share

        max_risk_amount = self.account_size * self.max_portfolio_risk_pct
        position_size_by_risk = int(max_risk_amount / risk_per_share)
        
        max_position_value = self.account_size * self.max_position_pct
        position_size_by_capital = int(max_position_value / entry_price)
        
        position_size = min(position_size_by_risk, position_size_by_capital)
        total_exposure = position_size * entry_price
        max_loss = position_size * risk_per_share
        target_profit = position_size * target_distance

        return {
            "entry_price": entry_price,
            "stop_loss": stop_loss,
            "target": target,
            "risk_per_share": risk_per_share,
            "stop_distance_pct": (stop_distance / entry_price) * 100,
            "risk_reward": risk_reward,
            "position_size": position_size,
            "total_exposure": total_exposure,
            "max_loss": max_loss,
            "target_profit": target_profit
        }
