from typing import Dict, Any

class PaperTradingEngine:
    """
    Paper trading engine that applies conservative fill rules (slippage).
    """
    def execute_fill(self, price: float, direction: str, is_market: bool = True) -> Dict[str, Any]:
        # Apply conservative slippage for market orders
        slippage = 0.0005 # 0.05% slippage
        
        if is_market:
            fill_price = price * (1 + slippage) if direction.upper() == "LONG" else price * (1 - slippage)
        else:
            fill_price = price
            
        return {
            "status": "filled",
            "requested_price": price,
            "fill_price": round(fill_price, 2),
            "slippage_applied": is_market
        }
