import pytest
from datetime import datetime, timezone, timedelta
from backend.app.ai.embeddings.fake_provider import FakeEmbeddingProvider
from backend.app.ai.rag.vectorstores.fake_vectorstore import FakeVectorStore
from backend.app.ai.rag.vectorstores.vector_store import VectorItem
from backend.app.ai.rag.retrieval.retriever import Retriever

def test_embeddings():
    emb = FakeEmbeddingProvider(dimension=128)
    vecs = emb.embed_documents(["hello", "world"])
    assert vecs.shape == (2, 128)
    
def test_vectorstore():
    vs = FakeVectorStore()
    vs.ensure_collection("news", dim=128)
    
    item = VectorItem(id="1", vector=[0.1]*128, payload={"text": "hello"})
    res = vs.upsert("news", [item])
    assert res.success
    assert res.count == 1
    
    assert vs.count("news") == 1
    
    search_res = vs.search("news", [0.1]*128, top_k=5)
    assert len(search_res) == 1
    assert search_res[0].id == "1"

def test_retriever():
    vs = FakeVectorStore()
    vs.ensure_collection("news", dim=128)
    
    now = datetime.now(timezone.utc)
    future = now + timedelta(days=1)
    past = now - timedelta(days=1)
    
    vs.upsert("news", [
        VectorItem(id="past", vector=[0.1]*128, payload={"published_at": past.isoformat()}),
        VectorItem(id="future", vector=[0.2]*128, payload={"published_at": future.isoformat()})
    ])
    
    emb = FakeEmbeddingProvider(dimension=128)
    retriever = Retriever(vs, emb)
    
    results = retriever.retrieve("AAPL", as_of=now, collection="news")
    assert len(results) == 1
    
    # Test MMR Reranking
    vs.upsert("news", [
        VectorItem(id="dup1", vector=[0.1]*128, payload={"text": "Apple announces new iPhone", "published_at": past.isoformat()}),
        VectorItem(id="dup2", vector=[0.11]*128, payload={"text": "Apple announces new iPhone model", "published_at": past.isoformat()}),
        VectorItem(id="diff", vector=[0.9]*128, payload={"text": "Apple changes battery suppliers", "published_at": past.isoformat()})
    ])
    
    results = retriever.retrieve("Apple iPhone", as_of=now, collection="news", top_k=2)
    # MMR should pick one of the dupes and the diff, rather than both dupes (if lambda is low enough)
    assert len(results) == 2
