from typing import Dict
import time

class QuotaManager:
    def __init__(self):
        # provider -> endpoint -> minute/day tracking
        self._usage: Dict[str, Dict[str, Dict[str, int]]] = {}
        self._limits: Dict[str, Dict[str, int]] = {}
        self._minute_reset = time.time() // 60
        
    def set_limit(self, provider: str, limit_per_minute: int, limit_per_day: int):
        self._limits[provider] = {
            "per_minute": limit_per_minute,
            "per_day": limit_per_day
        }
        if provider not in self._usage:
            self._usage[provider] = {"per_minute": 0, "per_day": 0}

    def check_and_consume(self, provider: str) -> bool:
        current_minute = time.time() // 60
        if current_minute > self._minute_reset:
            self._minute_reset = current_minute
            for p in self._usage:
                self._usage[p]["per_minute"] = 0
                
        # If no limits are set, allow
        if provider not in self._limits:
            return True
            
        limits = self._limits[provider]
        usage = self._usage[provider]
        
        if usage["per_minute"] >= limits["per_minute"] or usage["per_day"] >= limits["per_day"]:
            return False
            
        usage["per_minute"] += 1
        usage["per_day"] += 1
        return True
