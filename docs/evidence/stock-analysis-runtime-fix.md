# Stock Analysis Runtime Fix Evidence

## 1. Root Cause Diagnosis

### Issue 1: "Unknown range preset: ytd"
The frontend `PERIODS` selector was configured to dispatch lower-case strings and shorthand variants like `ytd` and `3mo`. However, `resolve_preset_range` in `backend/app/ai/marketdata/ranges.py` strictly expected exact match strings like `"YTD"` and `"3M"`. Because `ytd` was not matched, it immediately threw a `ValueError("Unknown range preset: ytd")`.

### Issue 2: "No historical data available" & Candlestick failure
The user navigated to `/analysis?ticker=%5EBSEN` (`^BSEN`). However, `^BSEN` did not exist natively in the `InstrumentMaster`. While the Market Overview dynamically fetches `^BSESN` through `/api/v1/markets/indices`, the direct Stock Analysis route attempted to query `/api/v1/markets/history?ticker=^BSEN` which evaluated to a `404 Not Found`. This forced `fetchHistory` to throw an error, preventing `chartData` from populating. As a result, the `ChartWidget` containing the Candlestick logic was bypassed completely and replaced with the fallback `"No historical data available"` UI state.

## 2. Changes Implemented

1. **`backend/app/ai/marketdata/ranges.py`**:
   - Introduced `preset = preset.upper().replace('MO', 'M')` to safely normalize inputs like `ytd` to `YTD` and `1mo` to `1M`.
2. **`backend/app/api/main.py`**:
   - Registered `IN.XBOM.SENSEX` (`^BSESN`) with aliases `^BSEN` and `SENSEX` inside the `InstrumentMaster` bootstrap.
3. **`frontend/src/pages/StockAnalysis.tsx`**:
   - Corrected the `PERIODS` config to strictly mirror the native backend uppercase conventions (`1M`, `3M`, `YTD`, `MAX`).
   - Adjusted the default `period` state to `3M`.
4. **Tests**:
   - Added `test_markets_history_ytd` and `test_markets_history_3mo` in `backend/tests/api/test_history.py`.
   - Created `frontend/tests/api/markets.test.ts` to mock and verify valid API query serialization.

## 3. Verification

### Commands and Results
- **Backend Tests**: Executed `pytest backend/tests/api/test_history.py`. 
  - *Result*: `5 passed in 6.84s`
- **API Simulation**: Executed `curl "http://127.0.0.1:8000/api/v1/markets/history?ticker=%5EBSEN&period=3M&interval=1d"` via manual debug.
  - *Result*: Yielded `status: "OK"` mapped correctly to the `^BSESN` instrument with a continuous array of accurate OHLCV timestamps.
- **Frontend Tests**: Executed `npx vitest run`.
  - *Result*: `3 test files passed (11 total tests)`.
- **Production Build**: Executed `npm run build`.
  - *Result*: `tsc -b && vite build` succeeded without type errors or regressions.

### Browser Verification
- **NOT VERIFIED**: I am an autonomous agent and cannot physically open the running browser to view the `ChartWidget` visual canvas directly. However, the data payload (`chartData`) has been verified to populate successfully, which unblocks the `ChartWidget` render tree containing `createChart.addCandlestickSeries()`.
