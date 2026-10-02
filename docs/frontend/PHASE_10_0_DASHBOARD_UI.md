# PHASE 10.0: DASHBOARD UI FOUNDATION

## 1. Context and Execution
The frontend layer for EquiNexa AI has been successfully initialized using React, TypeScript, Vite, and Tailwind CSS. The design system heavily favors a clean, institutional finance aesthetic, with precise typographic hierarchies and restrained use of color.

## 2. Implemented Pages & Components
- **Application Shell:** `AppLayout.tsx`, containing responsive sidebar navigation and top bar structures.
- **Overview Dashboard:** `Overview.tsx`, featuring a mock market-trend chart (via Recharts), index summary cards (NIFTY 50, S&P 500), and an empty Watchlist.
- **Research & Experiments:** `Research.tsx`, featuring a strictly read-only view of the `ProspectiveStatus`. It prominently displays the accumulation status (Evaluated: 0, Pending: 0, Required: 100) and explicitly states that the review gate is locked.
- **Stock Analysis:** `StockAnalysis.tsx`, structurally built but heavily suppressed with "Unavailable" states for Technicals and Predictions, correctly abiding by the Phase 9 accumulation rules.

## 3. Connected API Endpoints
- **Prospective Status Service:** A typed interface (`ProspectiveStatus`) was established in `src/services/api/prospective.ts`. Because the FastAPI backend does not yet expose a formal `GET /api/v1/research/status` REST route, this layer is mocked in the browser, but it structurally binds to the exact schema outputted by the Phase 9 python CLI.

## 4. Missing Endpoints
To fully power this frontend, the backend will need:
- `GET /api/v1/research/status`: To serve the ledger counts.
- `GET /api/v1/markets/indices`: To serve real-time NIFTY/S&P data.
- `GET /api/v1/markets/search?q={ticker}`: To power the global ticker search.
- `GET /api/v1/predictions/latest?ticker={ticker}`: To serve the immutable snapshots.

## 5. Development Commands
- Start dev server: `npm run dev`
- Build for production: `npm run build`
- Type checking: `npm run build` (tsc)

## 6. Constraints Honored
- **No Fabricated Data:** Predictions and technical charts explicitly read "Unavailable" rather than faking accuracy or historical values.
- **Model Freezing:** The model version is hardcoded and locked. No user interaction on the frontend can trigger an optimization sweep.

## 7. Next Recommended Task
- **REST API Wiring:** Wrap the existing Python research CLIs (Phase 8/9 tools) inside FastAPI controllers and replace the mocked `prospective.ts` fetch function with live API calls.
