from typing import Dict, Any, Optional

class CostCalculator:
    """
    Computes trading costs based on standard Indian equity delivery/intraday rates.
    """
    def __init__(self, is_intraday: bool = True):
        self.is_intraday = is_intraday
        
    def calculate_costs(self, price: float, quantity: int) -> Dict[str, float]:
        turnover = price * quantity
        
        # Approximations for typical discount broker (e.g., Zerodha) in India
        if self.is_intraday:
            brokerage = min(20.0, turnover * 0.0003)
            stt = 0.0 # No STT on intraday buy, 0.025% on sell. For simplicity, cost per leg.
        else:
            brokerage = 0.0
            stt = turnover * 0.001
            
        exchange_txn_charge = turnover * 0.0000345
        sebi_charges = turnover * 0.000001
        stamp_duty = turnover * 0.00003 if not self.is_intraday else turnover * 0.00003
        gst = (brokerage + exchange_txn_charge + sebi_charges) * 0.18
        
        total_cost = brokerage + stt + exchange_txn_charge + sebi_charges + stamp_duty + gst
        
        return {
            "turnover": round(turnover, 2),
            "brokerage": round(brokerage, 2),
            "stt": round(stt, 2),
            "exchange_txn_charge": round(exchange_txn_charge, 2),
            "sebi_charges": round(sebi_charges, 2),
            "stamp_duty": round(stamp_duty, 2),
            "gst": round(gst, 2),
            "total_estimated_cost": round(total_cost, 2)
        }
