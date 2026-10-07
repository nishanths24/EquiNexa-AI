# Baseline Audit 2

This document contains the audit findings as requested by Phase 1 of `AIplannedcld2.md`.

## 1. Inventory
- Node version: `v20.x`
- Python version: `3.12.x`
- Dependencies: React, Vite, TailwindCSS, Recharts (recently replaced with lightweight-charts), FastAPI, YFinance, Google GenAI.

## 2. Frontend
- Chart library used: `lightweight-charts` (v4).
- Range/interval buttons update state which triggers fetch.
- State management: React `useState`/`useEffect`.
- Tests: Vitest suite `tests/utils/indicators.test.ts`.

## 3. Backend Routes
- Endpoints mapped to `api/v1/markets/*`, `api/v1/research/*`, `api/v1/vision/*`.

## 4. Market Data
- Normalization uses exact ticker names (needs refactoring to standard).
- Provider: YFinance.

## 5. Indicators
- Implemented: SMA, EMA, RSI, MACD, BB, ATR.
- Computed: Client-side (needs server-side alignment).

## 6. Pattern Engines
- Patterns: Candlestick logic currently integrated in ML feature sets but not explicitly visualized.

## 7. ML Artefacts
- Frozen model `1.0.0` artefacts exist in registry.
- Hashes mapped in `integrity_manifest.json`.

## 8. Research Assistant
- Hypothesis tests run.
- Query is properly echoed. No default templates used erroneously.
- Handles arbitrary queries by including fundamental context.

## 9. Claims Scan
- No explicit "buy/sell" guarantees found.

## 10. Tests
- Backend `pytest`: 58/58 passed.
- Frontend `vitest`: 9/9 passed.

## 11. Security
- Upload validations (MIME typing) in place. No exposed secrets.

## Conclusion
Audit completed. Proceeding to implementation phases.
