import yfinance as yf
import pandas as pd
from typing import List, Dict, Any
from backend.app.ai.technical.indicators import INDICATOR_CATALOGUE

class ScannerEngine:
    """
    Scans a pre-defined universe of tickers for technical filters.
    Respects strict budgets to avoid rate limits.
    """
    def __init__(self, universe: List[str] = None):
        # Default to Nifty 50 constituents proxies for testing
        self.universe = universe or ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS"]
        
    def scan(self, filter_type: str = "oversold_rsi", budget: int = 5) -> Dict[str, Any]:
        """
        Executes a scan over the universe up to the allowed budget.
        """
        results = []
        scanned = 0
        
        for ticker in self.universe[:budget]:
            try:
                t = yf.Ticker(ticker)
                df = t.history(period="3mo", interval="1d")
                scanned += 1
                
                if df.empty or len(df) < 14:
                    continue
                    
                df.columns = [c.lower() for c in df.columns]
                
                if filter_type == "oversold_rsi":
                    rsi_series = INDICATOR_CATALOGUE["RSI"]["func"](df)
                    if not rsi_series.empty and rsi_series.iloc[-1] < 30:
                        results.append({
                            "ticker": ticker,
                            "value": round(rsi_series.iloc[-1], 2),
                            "signal": "Oversold"
                        })
                elif filter_type == "overbought_rsi":
                    rsi_series = INDICATOR_CATALOGUE["RSI"]["func"](df)
                    if not rsi_series.empty and rsi_series.iloc[-1] > 70:
                        results.append({
                            "ticker": ticker,
                            "value": round(rsi_series.iloc[-1], 2),
                            "signal": "Overbought"
                        })
            except Exception:
                continue
                
        return {
            "status": "ok",
            "filter_type": filter_type,
            "scanned_count": scanned,
            "matches": results
        }
