import chromadb
from typing import List
from backend.app.ai.rag.vectorstores.vector_store import VectorStore, VectorItem, ScoredItem

class ChromaVectorStore(VectorStore):
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        
    def ensure_collection(self, collection_name: str, dim: int):
        # Chroma handles dimensions automatically based on inserted embeddings
        self.client.get_or_create_collection(name=collection_name)
        
    def upsert(self, collection_name: str, items: List[VectorItem]):
        collection = self.client.get_collection(name=collection_name)
        
        ids = [item.id for item in items]
        embeddings = [item.vector for item in items]
        metadatas = [item.payload for item in items]
        
        collection.upsert(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas
        )
        
    def search(self, collection_name: str, query_vector: 'np.ndarray', top_k: int = 5) -> List[ScoredItem]:
        collection = self.client.get_collection(name=collection_name)
        
        results = collection.query(
            query_embeddings=[query_vector.tolist()],
            n_results=top_k,
            include=["metadatas", "distances"]
        )
        
        scored_items = []
        if results['ids'] and results['ids'][0]:
            for i in range(len(results['ids'][0])):
                scored_items.append(ScoredItem(
                    id=results['ids'][0][i],
                    score=results['distances'][0][i], # Note: Chroma returns distances (lower is better for L2)
                    payload=results['metadatas'][0][i]
                ))
                
        return scored_items

    def count(self, collection_name: str) -> int:
        collection = self.client.get_collection(name=collection_name)
        return collection.count()
        
    def delete(self, collection_name: str, ids: List[str]):
        collection = self.client.get_collection(name=collection_name)
        collection.delete(ids=ids)
        
    def health_check(self) -> bool:
        return True
