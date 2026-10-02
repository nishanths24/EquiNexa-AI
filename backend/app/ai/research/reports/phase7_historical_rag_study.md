# Phase 7: Point-in-Time Historical NLP/RAG Study

## 1. Objective
Determine whether genuinely point-in-time historical financial news provides incremental predictive or calibration information beyond technical features and deterministic patterns.

## 2. Frozen Phase 6.1 Benchmark
- **Dataset**: Multi-year (2018-2024), 12 Tickers, US + India
- **Architecture**: HistGradientBoosting + Deterministic Pattern Fusion
- **Evaluation**: Walk-forward, 1-bar embargo
- **Leakage Controls**: Dynamic targets (strictly isolated from features)
- **Status**: FROZEN.

## 3. Historical Corpus Source & Limitations (CRITICAL STOP CONDITION)
A rigorous search for a legitimate historical point-in-time news corpus under zero-budget constraints was conducted.
- High-quality historical news (with strict publication timestamps, full text, and canonical URLs for 6 years across 12 tickers) is exclusively behind premium APIs (e.g., Bloomberg, Reuters, FactSet, premium EOD).
- Open-source scraping violates TOS and fails the strict `published_at` timestamping integrity requirement necessary for point-in-time backtesting.
- **Decision:** As per the strict rules, synthetic historical news was **NOT** generated, and random noise was **NOT** injected.

**Conclusion:** Historical RAG is architecturally implemented but its historical predictive contribution remains unvalidated because a legitimate point-in-time historical news corpus was unavailable.

## 4. Point-in-Time Methodology & Architecture Tested
Despite the lack of a corpus, the architectural components for RAG were strictly implemented and validated via unit testing (`test_historical_rag.py`):
1. **HistoricalNewsProvider Interface**: Implemented to enforce strict `HistoricalArticle` schemas.
2. **Retrieval Architecture**: `Retriever.py` strictly forces `published_at < T`. Any news from the prediction date `T` or later is dropped prior to reranking.
3. **Sentiment Extraction**: Strongly typed `SentimentOutput` structures the LLM responses to provide `positive_prob`, `neutral_prob`, `negative_prob`, `confidence`, and array of `evidence_ids`.
4. **Security Controls**: The retrieval system treats all payload content as raw, untrusted text, preventing prompt injections from affecting evaluation boundaries.

## 5. Incremental-Information Analysis & Calibration
- Because no legitimate news could be ingested, the ablation matrix (Experiments A-E) evaluates to a mathematically identical technical baseline.
- **RAG Participation**: 0.0%
- **Missing-news Rate**: 100.0%

## 6. Tests Passed
```bash
pytest backend/tests/ai/test_historical_rag.py
```
Tests proved that:
- Future articles (`> T`) are excluded.
- Same-day articles (`== T`) are aggressively excluded.
- Valid historical articles (`< T`) are cleanly retrieved.

## 7. Conclusions
- We have completely finalized the robust machine learning, walk-forward, embargo, evaluation, and strict leakage architectures.
- The system achieves an honest, leakage-free 61.91% generalization accuracy using purely technical indicators and deterministic patterns.
- The fundamental AI limitation is now strictly data-sourcing for historical context, rather than pipeline architecture.

**Recommendation for Next Phase:** 
Suspend historical evaluation research. Pivot the system to **Live Paper Trading / Production Mode**. By running purely in real-time, the system can ingest live current news (which is freely and legitimately available via APIs like Yahoo Finance) without suffering from historical data procurement constraints. This will allow the system to organically build its own legitimate point-in-time RAG database going forward.
