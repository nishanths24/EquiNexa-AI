import yfinance as yf
from datetime import datetime
from typing import Dict, Any

class MarketContextEngine:
    """
    Extracts top-level market context (e.g. index performance, gap states, breadth proxies).
    """
    def __init__(self, index_symbol: str = "^NSEI"):
        self.index_symbol = index_symbol
        
    def get_context(self) -> Dict[str, Any]:
        """
        Returns index context and day-type labels.
        """
        try:
            tkr = yf.Ticker(self.index_symbol)
            df = tkr.history(period="5d", interval="1d")
            
            if df.empty or len(df) < 2:
                return {"status": "unavailable", "reason": "Insufficient index data"}
                
            last_close = df['Close'].iloc[-1]
            prev_close = df['Close'].iloc[-2]
            
            pct_change = ((last_close - prev_close) / prev_close) * 100
            
            day_type = "Neutral"
            if pct_change > 1.0:
                day_type = "Trend Up"
            elif pct_change < -1.0:
                day_type = "Trend Down"
                
            return {
                "status": "ok",
                "index_symbol": self.index_symbol,
                "latest_close": round(last_close, 2),
                "pct_change": round(pct_change, 2),
                "day_type": day_type,
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {"status": "error", "reason": str(e)}
