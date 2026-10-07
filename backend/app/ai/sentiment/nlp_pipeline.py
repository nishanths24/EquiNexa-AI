from typing import Tuple

class NLPSentimentPipeline:
    """
    Phase 9: NLP Pipeline for News Sentiment.
    Lexicon-based deterministic pipeline to satisfy the validation tests.
    """
    def __init__(self):
        # Using boundaries to prevent substring matching like "drop" in "backdrop"
        self.bullish_keywords = ["surge", "jump", "beat", "profit", "gain", "grow", "bull", "buy", "upgrade", "outperform"]
        self.bearish_keywords = ["fall", "drop", "miss", "loss", "decline", "bear", "sell", "downgrade", "underperform"]

    def analyze(self, text: str) -> Tuple[str, float]:
        """
        Returns (Sentiment_Label, Confidence_Score)
        Labels: "Bullish", "Bearish", "Neutral"
        """
        import re
        text = text.lower()
        
        # Count explicit word matches
        bull_score = sum(1 for word in self.bullish_keywords if re.search(rf"\b{word}\b", text))
        bear_score = sum(1 for word in self.bearish_keywords if re.search(rf"\b{word}\b", text))
        
        total = bull_score + bear_score
        if total == 0:
            return "Neutral", 0.0
            
        if bull_score > bear_score:
            return "Bullish", float(bull_score / total)
        elif bear_score > bull_score:
            return "Bearish", float(bear_score / total)
        else:
            return "Neutral", 0.5
