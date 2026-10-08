# EquiNexa AI: V2 Architecture Audit & Proposal

## A. Current Architecture
- **Frontend**: React + Vite + TypeScript. Deployed on Vercel. 
  - Styling with TailwindCSS. 
  - Charting primarily handled by `lightweight-charts` and `recharts`.
- **Backend**: FastAPI + Python. Deployed on Render. 
  - Uses `pydantic` for schema validation and `httpx` for external API requests.
- **AI/ML Layer**: Integrates with Google GenAI (`google-genai`), OpenAI (`openai`), `chromadb`, and `sentence-transformers` for embeddings, RAG, and sentiment analysis.
- **Infrastructure**: V1 currently lacks fully wired caching and persistent RDBMS drivers in its production dependencies (no PostgreSQL drivers like `asyncpg` or Redis clients like `redis` yet), suggesting reliance on in-memory state, third-party APIs directly, or mock implementations.

## B. Existing Capabilities
- **Market Data**: Quotes, historical data (OHLCV).
- **Charting**: Lightweight interactive charts.
- **Analysis Engine**: Technical indicators, pattern recognition, support/resistance detection, candlestick analysis.
- **AI Orchestration**: Research assistant, forecasting, evaluation splits, embeddings, prompt registries.
- **Fundamentals**: Core fundamental objects exist in `models/domain/fundamentals.py`.
- **News**: Domain models for news exist in `news.py`.

## C. Existing Problems
1. **Tight Coupling to Free APIs**: Over-reliance on potentially restrictive APIs (e.g., `yfinance` for production is brittle and legally restricted for commercial display).
2. **Missing Persistence Layer**: Lacks formal integration of robust data stores (PostgreSQL / Redis) into the API lifecycle despite `migrations` existing in `db/`.
3. **Data Quality/Status**: The UI does not consistently label data as `REALTIME`, `DELAYED`, or `STALE` with corresponding timestamps from the provider.
4. **Rate Limiting & Coalescing**: Requests are not aggressively cached or coalesced, risking exhaustion of free-tier API keys.
5. **Security/Secrets**: Need to enforce strict server-side RBAC and secret injection via `.env` without exposing them to the React app.

## D. Existing Data Providers
- `yfinance` (Adapter present)
- `alphavantage` (Adapter present)
- `twelvedata` (Adapter present)

## E. Existing API Contracts
The current API contracts are largely structured in `backend/app/api/main.py`. These contracts heavily map to Pydantic models in `backend/app/models/domain/`.
- Needs versioning (`/api/v2/`).
- Responses lack standardized data-status metadata (`source`, `timestamp`, `latency_ms`, `is_market_open`).

## F. Existing Database/Storage
- **Schemas Provided**: Extensive schemas exist for Supabase/PostgreSQL across two migrations (`V1__BaseSchema.sql` and `V2__FullSchema.sql`), including support for TimescaleDB expansion (OHLCV metrics) and RLS (Row Level Security) for user profiles and watchlists.
- **Current State**: The backend lacks the driver implementations (`psycopg`, `asyncpg`, `supabase-py`) to actually connect to these schemas.

## G. Existing AI Pipeline
Located in `backend/app/ai/`:
- **Modules**: Contains a sophisticated folder structure for RAG, embeddings, risk, safety, schemas, explainability, vision, and technical analysis.
- **Models**: Built primarily around Gemini and OpenAI.
- **Limitation**: AI pipeline needs to guarantee structured output without hallucinations or look-ahead bias and use proper feature engineering instead of raw prompt injection.

## H. Existing Chart Engine
- `lightweight-charts` by TradingView (Open Source) and `recharts`.
- Suitable for V2, provided data is fed asynchronously and correctly typed.

## I. Existing Security
- Basic setup using `PyJWT` for tokens.
- **Needs Improvement**: OWASP implementation, CORS hardening, rate limiting per user/IP, and Supabase Auth integration.

## J. Existing Tests
- Comprehensive test suite existing in `tests/`, covering `api`, `ai`, `cache`, `providers`, and scenarios (e.g. `test_phase16_performance.py`, `test_j1_mandatory_scenarios.py`).

---

## K. V2 Architecture Proposal
**Frontend**
- Build the V2 dashboard behind a `/v2` route on React.
- Mobile-first approach, PWA capabilities.
- Real-time WebSockets integration for `lightweight-charts`.

**Backend**
- Establish a strict `MarketDataProvider` abstraction.
- Create `/api/v2/` router hierarchy.
- Enforce standard metadata on all V2 responses (`timestamp`, `data_status`).

**Storage & Cache**
- Wire Supabase (PostgreSQL) using standard async drivers.
- Implement `Upstash Redis` for rate limiting, quote caching, and request coalescing to protect provider limits.

## L. Provider Capability Matrix
(See `docs/DATA_PROVIDER_MATRIX.md` for full detailed verified matrix).

## M. Database Migration Plan
1. **Provision**: Setup Supabase project.
2. **Apply Phase 3**: Execute `V1__BaseSchema.sql` (users, exchanges, instruments, ohlcv).
3. **Apply Phase 4**: Execute `V2__FullSchema.sql` (profiles, watchlists, alerts, news, AI features).
4. **Drivers**: Install `asyncpg` / `supabase` into `backend/requirements.txt`.
5. **ORM/Query Builder**: Evaluate `SQLAlchemy` or use raw async queries for OHLCV performance.

## N. Risk Register
1. **Data Provider Limits**: The free tier of Alpha Vantage (25/day) is insufficient for production frontend traffic without aggressive caching.
2. **Licensing Risks**: Free financial APIs often strictly prohibit public redistribution or commercial use. Displaying `yfinance` data in a public Vercel app is a legal/TOS risk.
3. **NSE/BSE Realtime**: Indian real-time data is not legally available for free redistribution. We must default to delayed or EOD data and explicitly label it.
4. **V1 Breakage**: Modifying `backend/app/api/main.py` directly might break the existing Vercel deployment. We must route everything new through `v2`.

## O. Exact Implementation Phases
1. **PHASE 1**: Architecture audit (Completed via this document).
2. **PHASE 2**: Provider abstraction (Implement `MarketDataProvider`, `NewsProvider`).
3. **PHASE 3**: Caching & DB (Implement Redis request coalescing & PostgreSQL connections).
4. **PHASE 4**: Market Overview V2 (Indices, forex, heatmaps).
5. **PHASE 5**: Professional charting (WebSockets, `lightweight-charts` multi-timeframe).
6. **PHASE 6**: Technical analysis engine.
7. **PHASE 7**: Fundamentals engine.
8. **PHASE 8 & 9**: News and News Sentiment.
9. **PHASE 10 & 11**: AI Analysis and Walk-forward Prediction engine.
10. **PHASE 12**: Risk engine.
11. **PHASE 13 & 14**: Auth & Alerts.
12. **PHASE 15 - 18**: Admin, Performance, Security, Testing.
13. **PHASE 19 & 20**: V2 Deployment & Validation.
