import time
from typing import Dict, Any

class SessionManager:
    """
    Manages chat history and cache keys for the assistant.
    """
    def __init__(self):
        self.cache = {}
        
    def generate_cache_key(self, query: str, entities: list) -> str:
        # Normalised query + entities + as_of bucket (hourly)
        bucket = int(time.time() // 3600)
        norm_q = query.lower().strip()
        return f"{norm_q}_{'_'.join(entities)}_{bucket}"
        
    def get_cached(self, key: str) -> Dict[str, Any]:
        return self.cache.get(key)
        
    def set_cached(self, key: str, data: Dict[str, Any]):
        self.cache[key] = data
