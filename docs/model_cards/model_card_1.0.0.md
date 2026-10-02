# Model Card: EquiNexa AI version 1.0.0

## 1. Model Identity
* **Version:** `1.0.0`
* **Status:** FROZEN / COLLECTING PROSPECTIVE DATA.
* **Intended Use:** AI-driven financial intelligence, combining deterministic technical indicators with LLM-based sentiment (RAG). Intended as a research tool, NOT for automated trading.

## 2. Target and Horizon
* **Target Definition:** 5-trading-day forward return > 2%.
* **Prediction Horizon:** 5 Trading Days.

## 3. Architecture
* **Technical Baseline:** Scikit-learn based baseline model utilizing Technical Indicators (RSI, MACD, etc.).
* **News Intelligence:** RAG-backed sentiment extraction (LLM Provider).
* **Fusion:** Configured for early/late fusion of technical and sentiment signals.

## 4. Prospective Evaluation Status (Review Gate)
* **Evaluated Observations:** `0`
* **Pending Observations:** `0`
* **Required Threshold:** `100`
* **Review Gate Status:** **LOCKED** (Review Status: COLLECTING)
* **Metrics:** Performance metrics are intentionally SUPPRESSED until N=100 legitimate prospective observations are collected and resolved by the outcome ledger.

## 5. Baselines and Reproducible Evaluation
* **Retrospective Performance:** Benchmarks (e.g., 96% accuracy) are currently marked **UNVERIFIED**.
* **Calibration:** To be validated on the prospective dataset once the review gate opens.

## 6. Prohibited Uses & Limitations
* **NOT FINANCIAL ADVICE:** The model outputs probabilities and confidences, which are heuristic estimates, not frequency guarantees.
* **Out of scope:** High-frequency trading (HFT), options pricing, and fully autonomous order execution are strictly prohibited uses.

## 7. Data Provenance
* **Market Data:** Sourced via `yfinance`. Subject to survivorship bias if delisted tickers are not manually included.
* **News Data:** Sourced via RSS/APIs. Susceptible to missing timestamps and third-party API outages.

---
**Last Updated:** 2026-10-02 (Frozen State Confirmed)
