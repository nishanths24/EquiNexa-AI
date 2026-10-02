from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from backend.app.ai.rag.retrieval.retriever import Retriever
from backend.app.ai.prompts.chain import StructuredChain

class ExtractedEvent(BaseModel):
    event_type: str
    impact: str
    relevance: float
    evidence_quote: str

class SentimentAnalysis(BaseModel):
    score: float # -1.0 to 1.0
    events: List[ExtractedEvent]
    summary: str

class EventExtractor:
    def __init__(self, retriever: Retriever, chain: StructuredChain):
        self.retriever = retriever
        self.chain = chain
        
    def analyze(self, ticker: str, as_of: datetime) -> SentimentAnalysis:
        # 1. Retrieve RAG evidence strictly as-of
        docs = self.retriever.retrieve(ticker, as_of=as_of, collection="news", top_k=5)
        
        if not docs:
            # Deterministic fallback when no evidence
            return SentimentAnalysis(
                score=0.0,
                events=[],
                summary="No recent news available."
            )
            
        context = "\n".join([d.get("text", "") or d.get("content", "") for d in docs])
        
        # 2. Execute structured chain
        result = self.chain.execute(
            user_input=f"Analyze sentiment for {ticker} based on provided context.",
            schema=SentimentAnalysis,
            context=context
        )
        
        # Ensure result is SentimentAnalysis type (fake provider might construct empty)
        if not isinstance(result, SentimentAnalysis):
            return SentimentAnalysis.model_construct()
            
        return result
