from typing import List, Optional
from backend.app.ai.rag.vectorstores.vector_store import VectorStore, VectorItem, ScoredItem, MetadataFilter, UpsertResult, ProviderHealth

class FakeVectorStore(VectorStore):
    def __init__(self):
        self.collections = {}
        
    def ensure_collection(self, name: str, dim: int, distance: str = "cosine", payload_indexes: Optional[List[str]] = None):
        if name not in self.collections:
            self.collections[name] = {"dim": dim, "items": {}}

    def upsert(self, collection: str, items: List[VectorItem]) -> UpsertResult:
        if collection not in self.collections:
            return UpsertResult(success=False, count=0)
        
        for item in items:
            self.collections[collection]["items"][item.id] = item
            
        return UpsertResult(success=True, count=len(items))

    def search(self, collection: str, query_vector: List[float], top_k: int, filters: Optional[MetadataFilter] = None, score_threshold: Optional[float] = None) -> List[ScoredItem]:
        if collection not in self.collections:
            return []
            
        # Return dummy results
        results = []
        for i, item in enumerate(self.collections[collection]["items"].values()):
            if i >= top_k:
                break
            results.append(ScoredItem(id=item.id, score=0.9 - (i * 0.01), payload=item.payload))
        return results

    def delete(self, collection: str, ids: Optional[List[str]] = None, filters: Optional[MetadataFilter] = None) -> int:
        if collection not in self.collections:
            return 0
        
        count = 0
        if ids:
            for item_id in ids:
                if item_id in self.collections[collection]["items"]:
                    del self.collections[collection]["items"][item_id]
                    count += 1
        return count

    def count(self, collection: str, filters: Optional[MetadataFilter] = None) -> int:
        if collection not in self.collections:
            return 0
        return len(self.collections[collection]["items"])

    def health_check(self) -> ProviderHealth:
        return ProviderHealth(status="ok", latency_ms=1.0)
