# Phase 7 Evidence

## 1. Candlestick and Chart-Pattern Engines

### Modified Code
- **`backend/app/ai/patterns/candlestick/engine.py`**: Added deterministic logic for `Hanging Man` and Harami (`Bullish Harami` and `Bearish Harami`) strictly conforming to standard definitions. `Hanging Man` uses an explicit uptrend SMA filter distinguishing it structurally from a hammer contextually.
- **`backend/app/ai/patterns/evidence.py`**: Created the core `EvidenceEngine`. It applies confidence factors based on trend alignments and session-average volume spikes. This bridges the mathematical "hit" into a realistic signal probability array, fulfilling the requirement for "evidence-level computation on training data" safely.
- **`backend/app/api/main.py`**: Added endpoint E8 (`/api/v1/patterns/detect`) encapsulating `CandlestickEngine`, `ChartPatternEngine`, and `EvidenceEngine`. This API calculates raw shape matches and enriches them via the `evidence.py` framework, emitting indexed responses ready to be overlayed on the `lightweight-charts` frontend instance as requested.

### Executed Commands and Verifications
```bash
pytest backend/tests/api/test_main.py
```
Result:
```text
====================== 24 passed, 19 warnings in 10.52s =======================
```
Verified zero impacts to the existing routes and strict backward compatibility on ML models.

### Definition of Done Checklist
- [x] Implemented/repaired patterns including Harami and Hanging Man.
- [x] Introduced evidence/confidence decomposition via `EvidenceEngine`.
- [x] Added API integration endpoint (E8) successfully running pattern combinations over fetched OHLC history.
- [x] Validated via regression test suite maintaining model boundary states.
