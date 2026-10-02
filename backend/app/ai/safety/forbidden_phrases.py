import re
from typing import List

# Forbidden phrases (case-insensitive)
FORBIDDEN_PHRASES = [
    r"guaranteed profit", r"guaranteed prediction", r"guaranteed return", r"risk-free",
    r"100% accurate", r"100% future accuracy", r"cannot lose", r"sure shot",
    r"buy this stock", r"sell this stock", r"you should buy", r"you should sell", r"must buy", r"must sell"
]

class LanguageLinter:
    def __init__(self):
        self._patterns = [re.compile(p, re.IGNORECASE) for p in FORBIDDEN_PHRASES]

    def contains_forbidden(self, text: str) -> bool:
        """Check if the text contains any forbidden phrases."""
        return any(p.search(text) for p in self._patterns)
    
    def lint(self, text: str) -> str:
        """Raises ValueError if a forbidden phrase is detected, otherwise returns text."""
        if self.contains_forbidden(text):
            raise ValueError("Output contains forbidden language.")
        return text
