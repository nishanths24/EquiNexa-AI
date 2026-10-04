import yfinance as yf
from typing import Dict, Any

class FundamentalsEngine:
    """
    Retrieves and structures fundamental data for a given ticker with a scoring heuristic.
    """
    def get_fundamentals(self, ticker: str) -> Dict[str, Any]:
        try:
            t = yf.Ticker(ticker)
            info = t.info
            
            if not info:
                return {"status": "unavailable"}
                
            pe = info.get("trailingPE")
            fwd_pe = info.get("forwardPE")
            pb = info.get("priceToBook")
            
            # Simple value score heuristic (0-10)
            score = 5
            if pe and pe < 20: score += 2
            elif pe and pe > 50: score -= 2
            
            if pb and pb < 3: score += 2
            elif pb and pb > 10: score -= 2
            
            return {
                "status": "ok",
                "ticker": ticker,
                "fundamentals": {
                    "market_cap": info.get("marketCap"),
                    "pe_ratio": pe,
                    "forward_pe": fwd_pe,
                    "price_to_book": pb,
                    "dividend_yield": info.get("dividendYield"),
                    "debt_to_equity": info.get("debtToEquity")
                },
                "value_score": max(0, min(10, score))
            }
        except Exception as e:
            return {"status": "error", "reason": str(e)}
