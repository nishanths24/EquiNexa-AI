import numpy as np
from typing import List
from backend.app.ai.embeddings.embedding_provider import EmbeddingProvider, ProviderHealth

class FakeEmbeddingProvider(EmbeddingProvider):
    def __init__(self, dimension: int = 384):
        self.name = "fake-embeddings"
        self.model = "fake-model-v1"
        self.dimension = dimension
        self.max_tokens = 512
        self.normalize = True
        self.version_id = f"{self.model}|dim={self.dimension}|norm={self.normalize}"

    def embed_documents(self, texts: List[str]) -> np.ndarray:
        # Return random normalized vectors
        vecs = np.random.rand(len(texts), self.dimension)
        if self.normalize:
            norms = np.linalg.norm(vecs, axis=1, keepdims=True)
            vecs = vecs / norms
        return vecs

    def embed_query(self, text: str) -> np.ndarray:
        vec = np.random.rand(self.dimension)
        if self.normalize:
            vec = vec / np.linalg.norm(vec)
        return vec

    def health_check(self) -> ProviderHealth:
        return ProviderHealth(status="ok", latency_ms=2.0)
