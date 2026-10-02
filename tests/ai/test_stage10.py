import pytest
from datetime import datetime, timezone, timedelta
from backend.app.ai.sentiment.events.extractor import EventExtractor, SentimentAnalysis
from backend.app.ai.rag.retrieval.retriever import Retriever
from backend.app.ai.prompts.chain import StructuredChain
from backend.app.ai.providers.fake_llm import FakeLLMProvider
from backend.app.ai.embeddings.fake_provider import FakeEmbeddingProvider
from backend.app.ai.rag.vectorstores.fake_vectorstore import FakeVectorStore
from backend.app.ai.rag.vectorstores.vector_store import VectorItem

def test_event_extractor():
    vs = FakeVectorStore()
    vs.ensure_collection("news", dim=128)
    emb = FakeEmbeddingProvider(dimension=128)
    retriever = Retriever(vs, emb)
    
    provider = FakeLLMProvider()
    chain = StructuredChain(provider, system_template="Context: {context}")
    
    extractor = EventExtractor(retriever, chain)
    
    as_of = datetime.now(timezone.utc)
    
    # Test fallback on empty retrieval
    res_empty = extractor.analyze("AAPL", as_of)
    assert res_empty.score == 0.0
    assert res_empty.summary == "No recent news available."
    
    # Test with data
    vs.upsert("news", [
        VectorItem(id="1", vector=[0.1]*128, payload={"text": "Good news", "published_at": (as_of - timedelta(hours=1)).isoformat()})
    ])
    
    res = extractor.analyze("AAPL", as_of)
    # FakeLLMProvider returns empty schema instance
    assert isinstance(res, SentimentAnalysis)
