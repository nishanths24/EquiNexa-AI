# Phase 8: Prospective Live Prediction and Paper-Trading Research Infrastructure

## 1. Objective
Build a prospective, leakage-safe live evaluation system that generates and records predictions strictly using information available at prediction time `T`, and systematically measures real prospective performance by explicitly waiting for future outcomes. 

The core question transitions from theoretical backtesting to:
*"Can EquiNexa generate reproducible point-in-time predictions and measure real prospective performance?"*

## 2. Frozen Historical Benchmark
The system inherits the **Frozen Phase 6.1 Benchmark** (61.91% Accuracy) for purely technical baseline evaluation (using HistGradientBoosting, Deterministic Patterns, and 1-bar embargo over multi-year/multi-ticker data). The primary objective target remains locked at `> 2.0%` for a 5-day horizon. 

*Crucial Context: Historical RAG remains unvalidated. Phase 8 transitions RAG directly into a prospective experiment via live execution.*

## 3. Point-in-Time Live Architecture
A `LivePredictionPipeline` was engineered to natively run at a given `T` (e.g., current time `now()`) guaranteeing absolutely no forward-looking data contamination:
1. **Market Data As-Of Filter:** All incoming pricing data natively excludes timestamps `> T`.
2. **Technical & Pattern Snapshotting:** Deterministic formulas natively execute on the truncated dataset.
3. **Live News Ingestion:** `HistoricalNewsProvider` enforces strict `published_at < T`.
4. **Sentiment & RAG Generation:** Safely isolates unstructured LLM inputs.
5. **Prediction Freezing:** The outcome is instantly frozen into an immutable `PredictionSnapshot`.

## 4. Snapshot Schemas
Every execution produces a cryptographically trackable `PredictionSnapshot`:
- `prediction_id`: Unique trace ID.
- `prediction_timestamp`, `as_of_timestamp`
- `config_hash`, `model_version`, `feature_version`
- `predicted_probability`, `predicted_class`
- **Snapshots:** `technical_feature_snapshot`, `pattern_snapshot`, `news_hashes`

Upon waiting 5 trading days, the system joins this record with an `OutcomeSnapshot` (logging actual forward return and target match).

## 5. Parallel Ablation Methodology
To answer the secondary question regarding RAG's prospective value, the system is designed to execute triple-predictions at `T`:
1. Technical Only
2. Technical + Patterns
3. Technical + Patterns + RAG/Sentiment
This builds an objective prospective comparison log.

## 6. Paper Trading Simulation
A distinct `PaperPortfolio` layer was developed. It acts completely autonomously from the pure ML evaluation metrics.
- Uses virtual cash (`$100,000`).
- Models fractional transaction costs and entry/exit times.
- Explicitly decouples "Strategy Profitability" from "Machine Learning Accuracy."

## 7. Security and Observability
The `test_live_pipeline.py` suite formally validated the strict data segregation:
- **Leakage Rejection:** Providing a DataFrame containing future rows correctly resulted in the pipeline truncating the set instantly.
- **Future-News Rejection:** Live APIs returning "tomorrow's" timestamps are strictly filtered before RAG.
- **Data Provenance:** Configuration and Snapshot parameters securely hash parameters for complete traceability.

## 8. Dashboard Status
The underlying ML logic output formats are structured seamlessly for frontend ingestion (e.g., via Streamlit), ready to display probabilistic calibration, underlying features, and cumulative metrics strictly separated by sample size thresholds.

## 9. Reproducibility & Commands
```bash
# Run Security and Point-in-Time Pipeline Validation
pytest backend/tests/ai/test_live_pipeline.py
```

## 10. Limitations & Future Research
- The paper trading simulation lacks advanced order-book slippage modeling. 
- *Crucially: Do not claim live RAG improves prediction or that the model is profitable until hundreds of prospective, multi-regime observations have naturally accumulated.*

**Next Step:** Integration of the Live Pipeline directly into a daemonized service for forward-tracking, officially kicking off Live Paper Trading.
