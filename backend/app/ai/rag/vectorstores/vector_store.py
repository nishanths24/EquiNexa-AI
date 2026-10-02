from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class VectorItem(BaseModel):
    id: str
    vector: List[float]
    payload: Dict[str, Any]

class ScoredItem(BaseModel):
    id: str
    score: float
    payload: Dict[str, Any]

class MetadataFilter(BaseModel):
    # Abstract syntax tree for filters (and/or/eq/in/range)
    pass

class UpsertResult(BaseModel):
    success: bool
    count: int

class ProviderHealth(BaseModel):
    status: str
    latency_ms: Optional[float] = None
    message: Optional[str] = None

class VectorStore(ABC):
    @abstractmethod
    def upsert(self, collection: str, items: List[VectorItem]) -> UpsertResult:
        pass

    @abstractmethod
    def search(self, collection: str, query_vector: List[float], top_k: int, filters: Optional[MetadataFilter] = None, score_threshold: Optional[float] = None) -> List[ScoredItem]:
        pass

    @abstractmethod
    def delete(self, collection: str, ids: Optional[List[str]] = None, filters: Optional[MetadataFilter] = None) -> int:
        pass

    @abstractmethod
    def count(self, collection: str, filters: Optional[MetadataFilter] = None) -> int:
        pass

    @abstractmethod
    def health_check(self) -> ProviderHealth:
        pass

    @abstractmethod
    def ensure_collection(self, name: str, dim: int, distance: str = "cosine", payload_indexes: Optional[List[str]] = None):
        pass
