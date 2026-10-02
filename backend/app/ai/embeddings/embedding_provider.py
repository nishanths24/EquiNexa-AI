from abc import ABC, abstractmethod
import numpy as np
from pydantic import BaseModel
from typing import List, Optional

class ProviderHealth(BaseModel):
    status: str
    latency_ms: Optional[float] = None
    message: Optional[str] = None

class EmbeddingProvider(ABC):
    name: str
    model: str
    dimension: int
    max_tokens: int
    normalize: bool
    version_id: str

    @abstractmethod
    def embed_documents(self, texts: List[str]) -> np.ndarray:
        pass

    @abstractmethod
    def embed_query(self, text: str) -> np.ndarray:
        pass

    @abstractmethod
    def health_check(self) -> ProviderHealth:
        pass
