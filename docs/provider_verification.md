# Provider Verification Log

This document records the implemented and configured external AI and data providers used in EquiNexa AI. 

## 1. Large Language Models (LLMs)

### FakeLLMProvider
* **Implementation:** `backend/app/ai/providers/fake_llm.py`
* **Status:** VERIFIED (Code-level offline tests).
* **Capabilities:** Deterministic outputs, structured JSON schema bypass, token counting stubs.
* **Env Vars:** None.
* **Limitations:** Not a real model; used exclusively for deterministic unit testing and CI pipelines.

### OpenAIProvider
* **Implementation:** `backend/app/ai/providers/openai_provider.py`
* **Status:** CONFIGURED. Live connectivity check requires a valid API key.
* **Capabilities:** `supports_vision=True`, `supports_tools=True`, `supports_json_schema=True` (using `client.beta.chat.completions.parse`).
* **Env Vars:** `OPENAI_API_KEY` (Required).
* **Limitations / Rate Limits:** Subject to OpenAI Tier limits. Not a free-tier guaranteed provider for massive batch jobs.
* **Data Licensing:** OpenAI does not train on API inputs by default, satisfying enterprise privacy requirements.

## 2. Embedding Models

### LocalProvider (Sentence Transformers)
* **Implementation:** `backend/app/ai/embeddings/local_provider.py`
* **Status:** VERIFIED (Offline).
* **Capabilities:** CPU-based local embeddings.
* **Limitations:** Requires RAM/CPU to run locally; cold starts can impact initial latency on free-tier hosting.

### FakeEmbeddingProvider
* **Implementation:** `backend/app/ai/embeddings/fake_provider.py`
* **Status:** VERIFIED (Offline).
* **Capabilities:** Hash-based deterministic vectors for testing RAG.

## 3. Vector Stores

### ChromaStore
* **Implementation:** `backend/app/ai/rag/vectorstores/chroma_store.py`
* **Status:** VERIFIED (Offline).
* **Capabilities:** Local persistence for document embeddings.
* **Limitations:** Ephemeral on stateless free-tier hosts without a mounted volume.

### FakeVectorStore
* **Implementation:** `backend/app/ai/rag/vectorstores/fake_vectorstore.py`
* **Status:** VERIFIED (Offline).

## 4. Market Data & News

### YFinance (MarketDataProvider)
* **Implementation:** `backend/app/ai/marketdata/market_data_provider.py`
* **Status:** VERIFIED (Offline/Live).
* **Limitations:** Unofficial API. Subject to rate limits. Intraday history is heavily restricted. Redistribution of raw data is against ToS.

---
**Last Verification Date:** 2026-10-02
