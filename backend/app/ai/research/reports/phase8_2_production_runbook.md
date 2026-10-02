# Phase 8.2: Production Deployment & Prospective Runbook

## 1. Objective
EquiNexa AI is now designed to reliably collect unbiased prospective observations over time, completely avoiding historical lookahead bias or accidental model modification. This runbook details the production deployment, operational health checking, backup systems, and recovery plans.

## 2. Model Freeze (CRITICAL)
- **Status:** **FROZEN**
- **Model Version:** `1.0.0`
- **Target:** `> 2.0%` for a 5-day horizon.
- The AI parameters are absolutely forbidden from auto-tuning based on emerging prospective metrics. Changing `model_version` immediately invalidates the prospective chain.

## 3. Architecture & Deployment
The system consists of three logical operational layers:
1. **FastAPI Backend (API):** Serves predictions, metrics, and paper trading state for the dashboard.
2. **Scheduler Daemon (Worker):** Continuously running process invoking `job_generate_predictions` sequentially based on `schedule`.
3. **Outcome Resolver (Cron):** A distinct background loop validating T+5 trading days.

### Environment Requirements
- Python 3.12+
- Persistent Volume for `/backend/app/ai/research/registry/`
- No database required (JSONL Immutable ledgers).
- Secrets: Provided via `.env` (API Keys for Yahoo Finance, Vector Store, LLM) — **never committed**.

### Startup Command
```bash
# Start backend API
uvicorn backend.main:app --host 0.0.0.0 --port 8000

# Start Scheduler Worker
python backend/scripts/run_scheduler.py
```

## 4. Health Checks and Observability
The API layer exposes health checks separating **System Health** from **Model Performance**.
- `GET /api/v1/health`: Returns API readiness.
- `GET /api/v1/scheduler/health`: Returns scheduler heartbeat, last prediction timestamp, and failure counters.
- **Do not assume the model is profitable simply because the API is healthy.**

## 5. Security & Leakage Rejection
Extensively tested and verified:
- **Temporal Rejection:** Future prices and news articles are aggressively excluded by strict `< T` constraints.
- **Idempotency:** SHA-256 prevents duplicate records.
- **Data Mutation:** Raw ledger updates are strictly Append-Only.

## 6. Backup & Restore
- **Backup:** Simply compress the `registry/` directory.
  `tar -czvf equinexa_prospective_backup_$(date +%F).tar.gz backend/app/ai/research/registry/`
- **Restore:** Unpack the tarball. **NEVER** overwrite existing files if restoring a smaller subset, only merge.

## 7. Metrics Presentation
- Metrics are calculated purely on `EVALUATED` predictions.
- The dashboard is required to prominently display `N=` (sample size).
- Small sample sizes will visually display a **"Insufficient Data"** flag.

## 8. Failure Recovery
- **Provider Outage:** If a market data API fails during prediction, the scheduler retries (bounded). If it fails permanently, no prediction is made.
- **Outcome Outage:** If the API fails to provide exit prices at T+5, the prediction safely remains in `PENDING` state until the provider is restored.

## 9. Conclusion
EquiNexa AI is now robustly deployed for prospective observation collection. Do not optimize or retrain. Wait for the data.
