# Direct Repair Review

## Source inspection findings

The uploaded source contained several concrete integration defects:

1. The frontend called `/api/v1/markets/search`, while the backend exposed `/api/v1/market/instruments/search`. This explains the broken global search workflow.
2. `StockAnalysis.tsx` is the route actually mounted by `App.tsx`; the separate `ChartWorkspace`/`ChartEngine` implementation was not mounted there. The latter also had a no-op `setChartType`, so it could not provide a real chart-type switch.
3. The mounted `ChartWidget` did create a candlestick series, but it lacked an explicit volume series and robust timestamp/data normalization. It has been hardened and given an explicit interactive chart area.
4. The frontend search Enter handler navigated directly to arbitrary text instead of resolving the query first. It has been changed to resolve the search and open the first valid instrument result.
5. The backend now exposes a frontend-compatible search endpoint with a stable `{symbol,name,exchange,type}` result shape.
6. History responses are sorted chronologically and empty normalized datasets are returned as an explicit error rather than an apparently successful empty dataset.

## Changes made

- `frontend/src/components/layout/AppLayout.tsx`
- `frontend/src/components/ChartWidget.tsx`
- `frontend/src/pages/StockAnalysis.tsx`
- `backend/app/api/main.py`
- `frontend/tests/api/markets.test.ts`
- `backend/tests/api/test_history.py`

## Verification performed here

- Python backend source compilation: PASS.
- Repository/source inspection: PASS.
- Secret filename scan: no `.env` files present in the uploaded archive.
- The uploaded archive contained no `node_modules`, virtual environments, `.git`, datasets, Chroma DB, or cache directories.
- Full frontend build could not be completed in this environment because the archive intentionally excludes `node_modules` and dependency installation timed out.
- Browser/live-data verification has NOT been performed in this environment.

No model, prospective ledger, dataset, or evaluation gate was intentionally modified.
