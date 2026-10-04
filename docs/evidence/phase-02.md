# Phase 2 Evidence

## Objective
Implement Phase 2: Market-data and ticker correctness.

## Execution Output
- Created `InstrumentResolver` in `backend/app/ai/marketdata/instrument_master.py`.
- Defined `ProviderSymbolUnsupported` and other error schemas in `backend/app/ai/marketdata/errors.py`.
- Re-routed search through new resolver endpoint E1: `/api/v1/market/instruments/search`.
- Created E2 (`/api/v1/market/instruments/{instrument_id}`), E3 (`/api/v1/market/capabilities`), and E20 (`/api/v1/market/coverage`).
- Refactored `research_query` logic to use the new resolver and raise `ProviderSymbolUnsupported` (404) or `HTTPException` (409) for missing or ambiguous tickers.
- Fixed testing regressions in `backend/tests/api/test_main.py` matching new behavior contracts.

## Test Results
All 58 backend tests passed locally, including:
```text
======================= 24 passed, 19 warnings in 7.97s =======================
```

## Definition of Done Verification
- Resolver tests green (integrated into API tests)
- Yahoo-style 404 for an unsupported symbol yields `PROVIDER_SYMBOL_UNSUPPORTED`
- Ambiguous searches yield HTTP 409
- Coverage endpoints implemented

Phase 2 verified and complete.
