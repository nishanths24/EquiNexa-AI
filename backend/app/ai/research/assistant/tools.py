from typing import Dict, Any, List
import yfinance as yf

class AssistantTools:
    """
    Executes specific research tools safely, failing gracefully.
    """
    def get_fundamentals(self, ticker: str) -> Dict[str, Any]:
        try:
            t = yf.Ticker(ticker)
            info = t.info
            if not info:
                return {"status": "unavailable"}
            return {
                "market_cap": info.get("marketCap"),
                "pe_ratio": info.get("trailingPE"),
                "forward_pe": info.get("forwardPE"),
                "dividend_yield": info.get("dividendYield"),
                "52_week_high": info.get("fiftyTwoWeekHigh"),
                "52_week_low": info.get("fiftyTwoWeekLow"),
            }
        except Exception:
            return {"status": "unavailable"}
            
    def get_news(self, ticker: str) -> List[Dict[str, str]]:
        try:
            t = yf.Ticker(ticker)
            news = getattr(t, 'news', [])
            return [{"title": n.get('title'), "publisher": n.get('publisher'), "link": n.get('link')} for n in news[:5]]
        except Exception:
            return []
