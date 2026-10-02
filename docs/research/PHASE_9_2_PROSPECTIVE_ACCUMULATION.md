# PHASE 9.2: PROSPECTIVE OBSERVATION ACCUMULATION

## 1. Purpose
The purpose of Phase 9.2 is strictly passive data accumulation. The operational system will now collect genuine prospective observations over time, rigorously enforcing out-of-sample purity until the predetermined review threshold (N=100) is reached.

## 2. Frozen Configuration
The prospective data engine runs in a strictly locked configuration:
- **Model Version:** 1.0.0
- **Target Definition:** 5-day return > 2%
- **Review Threshold:** N=100 Evaluated Predictions

Any deviation or drift from this configuration will intentionally trip `IntegrityViolationError` exceptions in the monitoring subsystem, halting the pipeline rather than contaminating the dataset.

## 3. Observation Lifecycle
1. **Prediction Generation:** `scheduler.py` wakes up, truncates data safely at `T`, extracts features/RAG, and generates the prediction.
2. **Snapshot Storage:** Results are dumped persistently into the JSONL ledger alongside their exact inputs and SHA-256 idempotency key.
3. **Wait Cycle:** The prediction is flagged as `PENDING`.
4. **Outcome Resolution:** After exactly 5 legitimate trading days elapse on the respective exchange, the outcome resolver appends the true label in `outcomes.jsonl` and transitions to `EVALUATED`.

## 4. Integrity Controls
The system actively monitors for:
- Unique idempotency keys (prevents duplicates).
- Immutable `1.0.0` model version string.
- Valid `prediction_timestamp` values strictly adhering to correct timezones.

## 5. N=100 Threshold & Trigger Flag
When `Evaluated >= 100`, the monitor emits the `PHASE_9_READY_FOR_REVIEW` log message and writes a lockfile flag `phase9_review_flag.txt`. This is an idempotent emission.
*Crucial Note: This event purely means the dataset has accumulated. It does NOT signal model success, profitability, or automated recalibration.*

## 6. Prohibited Actions During Accumulation
- No Hyperparameter Tuning.
- No Retraining on live data.
- No Feature Engineering modifications.
- No modifying pending prediction records manually to force a positive outcome.

## 7. Current Observation Count
Current Evaluated Observations: **0**
Current Pending Observations: **0**

*(No prospective performance conclusion can be made until legitimate observations accumulate).*

## 8. CLI Status Dashboard
Monitor status autonomously with:
```bash
python -m backend.app.ai.research.prospective_status
```
