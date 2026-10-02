# PHASE 10.1: API INTEGRATION

## 1. Context and Objective
This phase transitions the React dashboard from a static, hardcoded frontend into a live system actively reading from the Python backend infrastructure via FastAPI.

## 2. API Routes Implemented
The following routes are available in `backend/app/api/main.py`:
- `GET /api/v1/health`: Basic system check.
- `GET /api/v1/research/status`: Reads live counts via `ObservationMonitor` (returns current `Evaluated`, `Required`, `Pending`, etc.).
- `GET /api/v1/markets/indices`: Returns explicit `UNAVAILABLE` because there is no robust cached pricing pipeline explicitly designated for read-only access in the existing system.
- `GET /api/v1/markets/search`: Returns `UNAVAILABLE` (no instrument master built).
- `GET /api/v1/predictions/latest?ticker={ticker}`: Seeks the `prospective_ledger.jsonl` and returns the latest un-resolved prediction (if it exists). 

## 3. Strict Research Safeguards Maintained
- **Read-Only:** All endpoints strictly use the `GET` verb.
- **Model Version Frozen:** `1.0.0` is strictly enforced.
- **Performance Hiding:** `prospective_status` intentionally drops metric arrays (`accuracy`, `ROC`) from the REST payload because `N` is less than `100`.

## 4. Run Instructions
Start Backend:
```bash
set PYTHONPATH=. 
python -m backend.app.api.main
```
Start Frontend:
```bash
cd frontend
npm run dev
```

## 5. Limitations
Market Indices, Search, and technical chart components render explicitly as "Unavailable". We refused to fabricate standard metrics to make the UI look populated in compliance with research rules.
