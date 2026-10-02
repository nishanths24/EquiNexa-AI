# Benchmark Claims Register

This document tracks the status of performance claims made in the project's documentation and specifications.

## Claim 1: "100% Relative Improvement" (48% → 96%)

* **Claim:** RAG-enhanced directional accuracy achieves ≈96% compared to a technical-only baseline of ≈48%, representing a 100% relative improvement.
* **Source:** `AIplannedcld.md` (Section 24).
* **Target Definition:** 5-trading-day forward return > 2%.
* **Evaluation Method:** Retrospective simulation / walk-forward.
* **Current Status:** **UNVERIFIED / NOT REPRODUCED**.
* **Reason:** While the test harnesses and leakage barriers exist (Stage 4, Stage 20), there is currently no generated reproducible artifact (`experiments/results/...`) proving this metric on a leakage-free walk-forward test.
* **Limitation:** As mandated by the scientific constraints, this claim must NOT be presented to users as a guaranteed live-market performance metric. The prospective engine has currently evaluated 0 real-world observations.

## Claim 2: Leakage-Free Architecture

* **Claim:** The system is protected against lookahead bias, overlapping labels, and future-data leakage in RAG.
* **Source:** `AIplannedcld.md` (Sections 7, 53).
* **Current Status:** **REPRODUCED / VERIFIED**.
* **Evidence:** The automated test suite (`tests/ai/test_leakage.py`, `tests/ai/test_historical_rag.py`) explicitly passes boundary checks for `published_at <= T` constraints and overlapping walk-forward embargoes.

---
**Last Updated:** 2026-10-02
