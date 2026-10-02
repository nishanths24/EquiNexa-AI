# PHASE 9.4: FROZEN PROSPECTIVE REVIEW

## 1. Executive Summary
This Phase implements the mathematical evaluation machinery that will ultimately determine the prospective performance of EquiNexa AI under strictly controlled, read-only out-of-sample conditions. It currently remains structurally blocked from execution until the active experimental constraints are satisfied.

## 2. Frozen Configuration
- **Model Version:** 1.0.0
- **Target:** 5-day return > 2%

## 3. Integrity Gate
The `run_phase_9_4_review` gate unconditionally blocks any mathematical processing of the prospective ledgers if:
1. `Evaluated N < 100`.
2. Any temporal, version, or hashing integrity violations are found via the Phase 9.3 `ProspectiveAuditor`.

## 4. Predefined Metric Battery
When the gate legitimately unblocks, the dataset builder produces the final DataFrame and runs:
- **Classification:** Accuracy, Balanced Accuracy, Precision, Recall, F1.
- **Probabilistic / Calibration:** Brier Score, ECE.
- **Stratified Analysis:** Time series, Regimes, Ticker, Market (US/IN), and RAG presence.

*None of these metrics have been computed. No optimization, retraining, or threshold adjustments have taken place.*

## 5. Current Execution Status
Running the review engine natively produces:
**`PHASE_9_REVIEW_BLOCKED`**
Reason: `evaluated_count=0, required=100`

The system continues its pure accumulation phase.
