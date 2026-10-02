from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
from backend.app.ai.embeddings.embedding_provider import EmbeddingProvider

class LocalEmbeddingProvider(EmbeddingProvider):
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self._model = None
        
    @property
    def model(self):
        if self._model is None:
            self._model = SentenceTransformer(self.model_name)
        return self._model
        
    @property
    def dimension(self) -> int:
        # all-MiniLM-L6-v2 dimension
        return 384
        
    def embed_text(self, text: str) -> np.ndarray:
        return self.model.encode(text)
        
    def embed_query(self, text: str) -> np.ndarray:
        return self.model.encode(text)
        
    def embed_documents(self, texts: List[str]) -> np.ndarray:
        return self.model.encode(texts)
        
    def health_check(self) -> bool:
        return True
