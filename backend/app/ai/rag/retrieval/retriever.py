from datetime import datetime, timezone
from typing import List, Optional
from backend.app.ai.rag.vectorstores.vector_store import VectorStore, ScoredItem
from backend.app.ai.embeddings.embedding_provider import EmbeddingProvider

class Retriever:
    def __init__(self, vector_store: VectorStore, embedder: EmbeddingProvider):
        self.vector_store = vector_store
        self.embedder = embedder

    def retrieve(self, ticker: str, as_of: datetime, collection: str, top_k: int = 5) -> List[dict]:
        """
        As-of safe retrieval logic.
        """
        if as_of.tzinfo is None:
            raise ValueError("as_of must be timezone aware")
            
        # 1. Embed query (using ticker as a simple query for now)
        q_vec = self.embedder.embed_query(ticker)
        
        # 2. Search
        # In a real implementation, we would construct a MetadataFilter for `published_at <= as_of`
        # and `ticker == ticker`.
        results = self.vector_store.search(collection, q_vec.tolist(), top_k=top_k * 2)
        
        # 3. As-of guard assertion and filtering
        valid_results = []
        for r in results:
            pub = r.payload.get("published_at")
            if pub:
                pub_dt = datetime.fromisoformat(pub)
                # Hard as-of check: strictly less than
                if pub_dt >= as_of:
                    continue # Skip future and same-timestamp leaks
            valid_results.append(r)
            
        # 4. Reranking / MMR
        if len(valid_results) > top_k:
            final = self._mmr_rerank(q_vec, valid_results, top_k)
        else:
            final = valid_results
            
        # Defensive runtime assertion
        for f in final:
            pub = f.payload.get("published_at")
            if pub:
                pub_dt = datetime.fromisoformat(pub)
                assert pub_dt < as_of, f"Leakage detected: document from {pub_dt} returned for as_of {as_of}"
                
        return [f.payload for f in final]

    def _mmr_rerank(self, q_vec, candidates: List[ScoredItem], top_k: int, lambda_mult: float = 0.5) -> List[ScoredItem]:
        """
        Maximal Marginal Relevance (MMR) reranking.
        """
        import numpy as np
        
        if not candidates:
            return []
            
        # For simplicity, if vectors are not returned by the vector store, 
        # we re-embed the candidate texts. 
        # In a real system, the vector store should return the vectors if requested.
        texts = [c.payload.get("text", "") or c.payload.get("content", "") or "empty" for c in candidates]
        cand_vecs = self.embedder.embed_documents(texts)
        
        q_vec = q_vec.reshape(1, -1)
        
        # Calculate similarities to query
        sims_to_query = np.dot(cand_vecs, q_vec.T).flatten()
        
        # Initialize selected indices
        selected = []
        unselected = list(range(len(candidates)))
        
        # Select first item (most similar to query)
        best_idx = int(np.argmax(sims_to_query))
        selected.append(best_idx)
        unselected.remove(best_idx)
        
        while len(selected) < top_k and unselected:
            selected_vecs = cand_vecs[selected]
            unselected_vecs = cand_vecs[unselected]
            
            # Similarities between unselected and selected
            sims_to_selected = np.dot(unselected_vecs, selected_vecs.T)
            max_sims_to_selected = np.max(sims_to_selected, axis=1)
            
            # MMR score
            mmr_scores = lambda_mult * sims_to_query[unselected] - (1 - lambda_mult) * max_sims_to_selected
            
            best_unselected_idx = int(np.argmax(mmr_scores))
            best_idx = unselected[best_unselected_idx]
            
            selected.append(best_idx)
            unselected.remove(best_idx)
            
        return [candidates[i] for i in selected]
