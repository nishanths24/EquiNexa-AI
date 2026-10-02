# Phase 8.1: Automated Prospective Prediction Collection and Outcome Evaluation

## 1. Objective
Turn the Phase 8 prediction architecture into a reliable, recurring prospective evaluation system that runs autonomously, tracks point-in-time predictions immutably, properly counts forward trading days, resolves outcomes honestly, and handles failures elegantly.

## 2. Ledger and Idempotency
- **Prediction Ledger:** Predictions are written sequentially to `backend/app/ai/research/registry/prospective_ledger.jsonl`. This ledger acts as an append-only immutable store.
- **Idempotency:** A SHA-256 hash representing `(market + ticker + prediction_timestamp + model_version + config_hash)` operates as a unique execution key. If the CRON job or scheduler accidentally triggers twice, the system inherently prevents the duplicate prediction from being recorded.

## 3. Outcome Resolution and Trading Calendars
- **Outcome Ledger:** `backend/app/ai/research/registry/prospective_outcomes.jsonl` tracks target resolution.
- **5-Trading-Day Logic:** The `TradingCalendar` explicitly calculates valid business days between entry and evaluation, ensuring weekends and known market holidays do not artificially truncate the required forecast horizon. 
- **Transition Status:** A prediction gracefully waits in `PENDING` status. Once 5 trading days elapse and the market data API supplies the closing candle, the resolver computes `actual_target = future_return > 0.02` and transitions the record to `EVALUATED`.

## 4. RAG, News Handling & Failure Constraints
- **News/RAG Coverage:** Continues to be strictly extracted purely bounded by `published_at < T`. 
- **Failures:** If Yahoo Finance fails to deliver market data, or the vector store is offline, the resolver logs a failure but the historical prediction is left strictly unmodified.

## 5. Model Versioning & Freeze
The system is explicitly operating under `model_version: 1.0` reflecting the frozen `EXP-6-HGB-TH-2` Phase 6 configuration. 
- Retraining is structurally disabled in this runtime loop. 
- Model parameters are never optimized based on emerging live metrics, thereby retaining pure out-of-sample legitimacy.

## 6. Paper Portfolio Status
The isolated paper simulator awaits evaluated execution feeds. Profitability metrics remain structurally separated from Model Accuracy. **No real brokerage keys are permitted.**

## 7. Metrics and Dashboard (CRITICAL RULE)
- **Do NOT** report a live "Accuracy" metric if `N=1` or `N=10`.
- All Live Metrics require a statistically meaningful sample threshold prior to visualization. 
- PENDING predictions DO NOT negatively impact accuracy.

## 8. Reproducibility & Tests
```bash
pytest backend/tests/ai/test_prospective_operations.py
```
Test Coverage Provided:
- Idempotency / Duplicate protection
- T+5 calendar logic
- PENDING -> EVALUATED lifecycle assertions

## 9. Limitations & Next Steps
- **Limitations:** The calendar algorithm uses a simplified weekday approximation for immediate portability. A production Indian equities deploy would require tight integration with NSE holiday schedules (`nsepy` etc).
- **Next Step:** We are officially complete with Phase 8.1. We now transition simply to "wait and see." Genuinely accumulating prospective observations is the only remaining task.
