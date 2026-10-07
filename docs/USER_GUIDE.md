# EquiNexa AI - User Guide

## Introduction
EquiNexa AI is an advanced trading research, evaluation, and journaling platform. It utilizes deterministic pattern recognition and constrained LLM generation to help retail traders formulate safe, mathematically-sound risk frameworks.

## 🚨 Risk Warning
EquiNexa AI provides **technical evaluation and quantitative setup scanning only**. 
**IT DOES NOT PROVIDE FINANCIAL ADVICE.**
Any predictions, target ranges, or setup probabilities are algorithmic calculations, not guarantees of performance. Intraday trading carries a significant risk of capital loss. Always trade within a predefined risk percentage using the built-in Scenario Planner.

## Core Modules

### 1. Market Context & Scanner (Phase 11)
Use the `/api/v1/trader/context` endpoint to identify broader market conditions (e.g. "Trend Up"). Use the `/api/v1/trader/scanner` to sweep your watchlist for specific indicators (e.g. RSI Oversold) to formulate hypotheses.

### 2. Scenario Planner & Risk Engine (Phase 12)
Before taking any live position, use the Scenario Planner (`/api/v1/trader/plan`). You *must* supply an invalidation level (stop loss). The engine will calculate your precise position sizing and estimate your net profitability after Indian brokerage and STT taxes.

### 3. Setup Lab (Phase 13)
Submit custom technical criteria in the Safe DSL format to test patterns against live tickers. Review the results on the frontend dashboard to see if a stock currently matches your edge parameters.

### 4. AI Research Assistant (Phase 10)
Ask the assistant queries about fundamental valuation and recent news. The assistant strictly aggregates data without injecting subjective recommendations, shielding you from hallucinated advice.
