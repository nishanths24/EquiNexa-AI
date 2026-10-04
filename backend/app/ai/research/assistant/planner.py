import re
from typing import Dict, Any, List

class QueryPlanner:
    """
    Extracts entities, dates, and intents from the user question.
    Falls back to deterministic regex if LLM is unavailable.
    """
    def __init__(self):
        pass
        
    def plan(self, query: str) -> Dict[str, Any]:
        """
        Produce a plan specifying what tools to use based on the query.
        """
        # Very simple deterministic planner for robustness
        query_lower = query.lower()
        tools_to_run = []
        
        # Entity extraction (simple uppercase ticker heuristic)
        tickers = re.findall(r'\b[A-Z]{2,5}\b', query)
        
        if "fundamental" in query_lower or "pe" in query_lower or "market cap" in query_lower:
            tools_to_run.append("fundamentals")
            
        if "pattern" in query_lower or "chart" in query_lower or "technical" in query_lower:
            tools_to_run.append("patterns")
            
        if "news" in query_lower or "latest" in query_lower:
            tools_to_run.append("news")
            
        # Default fallback: if no specific tools detected but we have a ticker, get news and fundamentals
        if not tools_to_run and tickers:
            tools_to_run.extend(["news", "fundamentals"])
            
        return {
            "query_echo": query,
            "entities": tickers,
            "tools": tools_to_run
        }
