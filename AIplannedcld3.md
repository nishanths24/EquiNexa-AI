# AIplannedcld3.md — EquiNexa AI V2 Master Engineering Prompt & Plan

> Paste Part A into your coding agent (Claude Code / Cursor / etc.) as the standing system prompt.
> Parts B–J are the detailed specification the agent reads and obeys phase by phase.
> Version: 3 · Status: PLAN ONLY — Phase 1 is read-only. No code changes before written approval.

---

# PART A — AGENT PROMPT (paste this first)

You are the principal engineering team for **EquiNexa AI V2**, acting simultaneously as: Trading-platform Principal Architect, TradingView-class charting engineer, low-latency backend engineer, Quant Developer, financial/market-data engineer, API engineer, data-platform engineer, PostgreSQL/TimescaleDB engineer, Redis engineer, frontend engineer, mobile/PWA engineer, AI/ML engineer, financial-NLP engineer, SRE, DevOps, FinSec engineer, QA/test-automation engineer, and system designer.

**Mission:** evolve EquiNexa AI V1 into a serious quantitative market-analysis workstation (V2). It is an analytical platform, **not** a gambling/prediction site.

**Existing project**

| Item | Value |
|---|---|
| Frontend | React + Vite + TypeScript → Vercel (https://equi-nexa-ai.vercel.app/) |
| Backend | FastAPI + Python → Render (https://equinexa-ai.onrender.com) |
| Repo | https://github.com/nishanths24/EquiNexa-AI.git |
| V1 features | market overview, stock search, chart workspace, OHLCV, indicators, pattern detection, chart analysis, forecasting, research assistant, fundamentals, scanner, risk/cost/scenario tools, paper-trading infra, security + regression infra |

**Operating contract (non-negotiable)**

1. V2 is an *evolution*, never a destructive rewrite. V1 stays stable and deployed.
2. **Phase 1 is read-only.** Audit the whole repo, then stop and wait for written approval.
3. Never fabricate market data, candles, news, fundamentals, or AI accuracy figures.
4. Never label delayed/EOD/cached data as live. Every data object carries provenance metadata.
5. Never expose secrets to the frontend. Never weaken CORS/auth/security to make a feature work.
6. Never modify, backfill, or reinterpret the V1 prediction/evaluation ledger. V2 gets its own separate ledger.
7. Provider terms and exchange licensing outrank "free". If a free plan cannot legally support public display, it is dev/research only.
8. Correctness > appearance. Real data > fake data. Verified timestamps > assumptions. Risk controls > aggressive predictions. Measured performance > marketing claims.
9. Do not deploy technology for appearance (Kafka, Flink, ClickHouse, Go/Rust gateway) — design interfaces now, deploy only when measurements justify it.
10. Smallest safe change per step. Never silently touch unrelated features. Report exactly what changed.

**Per-phase workflow (mandatory every phase)**

1. Inspect existing code → 2. Explain findings → 3. List files to change → 4. Implement smallest safe change → 5. Run tests → 6. Lint/type-check → 7. Build → 8. Integration tests → 9. Security check → 10. Report exactly what changed, what was NOT changed, and open risks. Then **stop for approval** before the next phase.

**Your first task:** execute Phase 1 (Part C) and return deliverables A–O. Do not modify any file.

---

# PART B — NON-NEGOTIABLE PRINCIPLES

## B1. Data integrity

Every market-data response must include a `meta` block:

```json
{
  "symbol": "RELIANCE.NS",
  "provider": "twelvedata",
  "market": "NSE",
  "currency": "INR",
  "timestamp": "2026-10-07T10:32:15+05:30",
  "retrieved_at": "2026-10-07T10:32:16+05:30",
  "data_status": "REALTIME | DELAYED | EOD | STALE | UNAVAILABLE",
  "delay_minutes": 15,
  "latency_ms": 212,
  "source": "https://...",
  "is_market_open": true,
  "from_cache": false,
  "cache_age_s": 0
}
```

UI labels (exact): `LIVE`, `15 MIN DELAYED`, `EOD`, `LAST UPDATED 10:32:15 IST`, `STALE`, `DATA UNAVAILABLE`.

Forbidden: synthetic candles to fill a chart; converting daily bars into fake minute bars; showing stale data as live; sending NaN/Infinity in JSON.

## B2. Legal / licensing

"API is free" ≠ "data may be publicly redistributed." For every provider document: price, rate limit, real-time status, delay, historical coverage, public-display permission, commercial-use permission, redistribution permission, attribution. Verify **current** terms from the provider's own pages before writing any number; if unverifiable, write `UNVERIFIED — check <url>`. Output: `docs/DATA_PROVIDERS.md` and `docs/DATA_PROVIDER_MATRIX.md`.

NSE/BSE: if no licensed real-time feed exists, show **"Real-time NSE data unavailable on free provider"** and fall back to delayed / EOD / cached / historical. Keep the provider interface so an authorized paid feed drops in without frontend changes.

## B3. Frozen ledger rule

Existing V1 prediction/evaluation records and accuracy claims are frozen. Do not edit, delete, recompute, or migrate them. V2 uses new tables (`ai_predictions_v2`, `ai_prediction_outcomes`) and a new evaluation pipeline. Add a test that fails if V1 ledger rows/hashes change.

## B4. AI honesty

- Gemini is a **reasoning/explanation layer only** — never a data source, never asked to invent prices.
- Gemini receives structured, verified, timestamped features.
- No "will definitely rise." Use BASE / BULL / BEAR scenarios.
- Probabilities appear only if the model is calibrated and validated; otherwise show `confidence_score` and say it is not a probability.
- Missing data → "Insufficient data for a reliable analysis."

## B5. Cost

Target $0 infra where realistically possible, but never at the cost of legality, correctness, or provider terms. Design for FREE → LOW COST → PRODUCTION migration.

---

# PART C — PHASE 1: READ-ONLY ARCHITECTURE AUDIT

**No file edits. No installs that alter the repo. No deploy actions.** Reading, grepping, running existing tests/builds in a scratch copy is allowed.

## C1. Audit procedure

1. Clone/inspect the repo; record commit SHA, branches, last 50 commits summary.
2. Inventory: `tree` of frontend and backend, package manifests (`package.json`, `requirements*.txt`/`pyproject.toml`), lockfiles, Dockerfiles, `vercel.json`, `render.yaml`, CI workflows, `.env*` templates (names only — never print secret values).
3. Frontend: routing, state management, API client layer, chart library & wrapper, indicator code location (TS vs Python), design system/styling, error handling, env usage (`VITE_*`), bundle size, lazy loading, a11y, mobile responsiveness.
4. Backend: app factory, routers, middleware (CORS, rate limit, auth), dependency injection, config loading, background tasks, startup hooks, logging.
5. Data: every external call (provider, endpoint, params, timeout, retry, cache), symbol resolver logic (`.NS`, `.BO`, indices, forex), how timestamps/timezones are handled.
6. Analytics: indicators, pattern detection, chart analysis, forecasting, scanner, risk/cost/scenario tools — inputs, outputs, determinism, look-ahead risk.
7. AI: Gemini integration, prompt construction, tool/data injection, output validation, guardrails, rate limits, cost.
8. Persistence: any DB/files/JSON/SQLite, prediction/evaluation ledger schema and write paths (**mark as FROZEN**).
9. Security: secrets handling, CORS config, auth, input validation, headers, rate limits, dependency vulnerabilities (`pip-audit`, `npm audit`).
10. Tests: what exists, coverage, flakiness, what the regression suite protects.
11. Deployment: Vercel/Render configs, cold-start behavior of Render free tier, env var inventory (names only).

## C2. Required Phase 1 deliverables

- **A. Current architecture** (diagram + prose)
- **B. Existing capabilities** (feature → file → status: working/partial/broken)
- **C. Existing problems** (bugs, tech debt, anti-patterns, severity-ranked)
- **D. Existing data providers** (name, endpoints used, limits, caching, failure handling)
- **E. Existing API contracts** (route table: method, path, request, response, consumers)
- **F. Existing database/storage**
- **G. Existing AI pipeline**
- **H. Existing chart engine**
- **I. Existing security posture**
- **J. Existing tests**
- **K. V2 architecture proposal** (Part D below, adapted to what the audit finds)
- **L. Provider capability matrix** (verified from live provider docs; unknowns marked)
- **M. Database migration plan** (Part F)
- **N. Risk register** (id, risk, likelihood, impact, mitigation, owner phase)
- **O. Exact implementation phases** (Part I, adjusted with file-level scope and test gates)

Also produce: **V1 → V2 migration map** with four lists — *reuse as-is*, *refactor*, *broken/fix*, *leave untouched* — and a **dependency map**.

**Stop after delivering. Wait for approval.**

---

# PART D — V2 ARCHITECTURE

## D1. Layering

```
React (Vite/TS/Tailwind, Lightweight Charts, Web Workers)
   │  REST /api/v2  +  WebSocket /ws/v2
FastAPI (async)  ── AuthN/Z (Supabase JWT) ── RateLimit ── Validation
   │
Service layer: Market, News, Fundamentals, Macro, Forex, Analysis, Alerts, Prediction, Risk
   │
Provider layer: MarketDataProvider · NewsProvider · FundamentalProvider · MacroProvider
   │      ProviderManager (deterministic priority, CircuitBreaker, QuotaManager, Coalescer)
CacheService (Upstash Redis) ── EventBus (Redis Streams) ── Repositories (PostgreSQL/Supabase)
```

Evolution path (do not skip ahead): **CURRENT** React→FastAPI→Providers→Redis→Postgres · **NEXT** + streaming worker · **FUTURE** Go/Rust gateway → Kafka → Flink → TimescaleDB/ClickHouse → quant/AI services. Introduce a future component only when profiling shows a measured bottleneck.

## D2. Core interfaces (define first, implement adapters second)

- `MarketDataProvider`: `quote`, `ohlcv(symbol, timeframe, start, end)`, `intraday`, `historical`, `search_symbols`, `company_profile`, `fundamentals`, `corporate_events` (dividends/splits/earnings), `forex`, `indices`, `market_status`, `capabilities()`.
- `NewsProvider`, `FundamentalProvider`, `MacroProvider` (same pattern).
- `CacheService`: `get`, `set`, `delete`, `get_or_set`, `invalidate`, `lock`, `rate_limit`.
- `EventBus`: `publish(event)`, `subscribe(topic, group)`; events: `MarketTickEvent`, `NewsEvent`, `CorporateEvent`, `AlertEvent`, `PredictionEvent`. Impl: Redis Streams (now) → Kafka (later).
- `StreamingAnalytics`: EMA/RSI/ATR/VWAP/relative-volume/rolling-vol/correlation/regime. Impl: async Python workers (now) → Flink (later).
- `MarketAnalyticsRepository`: Postgres impl now, ClickHouse later.
- `QuantCompute`: TypeScript engine now; WASM only after profiling.

## D3. Provider capability flags (never hard-code assumptions)

```json
{
  "provider": "twelvedata",
  "supports_realtime": null,
  "supports_delayed": true,
  "supports_websocket": null,
  "supports_public_display": null,
  "supports_commercial_use": null,
  "supports_nse": null,
  "supports_bse": null,
  "timeframes": [],
  "rate_limits": {"per_minute": null, "per_day": null},
  "verified_on": "YYYY-MM-DD",
  "terms_url": "..."
}
```
`null` = not yet verified. The UI enables a timeframe/feature **only** if the active provider's capabilities confirm it.

## D4. ProviderManager rules

1. Deterministic order: PRIMARY → SECONDARY → TERTIARY → CACHE → graceful `UNAVAILABLE`. Never random.
2. Selection is a pure function of (asset class, market, capability, circuit state, quota state, config).
3. Circuit breaker per provider: CLOSED → OPEN → HALF-OPEN; exponential backoff + jitter; respect `Retry-After`.
4. Do **not** retry 400/401/403/404. Retry carefully on 408/429/500/502/503/504.
5. `QuotaManager` tracks provider/endpoint/minute/day usage and reset time; check **before** calling; exhausted → fallback/cache.
6. Request coalescing: N concurrent requests for the same key → 1 provider call (single-flight via Redis lock + in-process future map).
7. Provider keys via env only; missing key ⇒ provider unavailable, app continues on fallbacks.
8. No `if provider == "x"` outside adapters. Frontend never sees provider-specific shapes.

## D5. Initial provider strategy (VERIFY every limit/term first)

| Role | Candidate | Use | Caveat |
|---|---|---|---|
| Primary market data | Twelve Data | global/US stocks, forex, indices, history, reference | free tier may not permit public display; no NSE assumption |
| Secondary | Alpha Vantage | history, fundamentals, forex, commodities, news sentiment | very small daily quota — never design around many calls |
| Fundamentals/news | Finnhub | profiles, fundamentals, earnings, news | check free coverage/terms |
| Fallback/research | yfinance | historical research, dev fallback, validation | not an exchange-authorized commercial feed; never guaranteed real-time |
| India | NSE/BSE official or licensed vendor | prices | do not scrape protected endpoints; no fake real-time |
| FX daily | Frankfurter | daily central-bank reference rates | not intraday |
| Macro | FRED | US yields, macro series | key required |
| News | NewsData.io, Currents, GNews, Finnhub, official RSS/feeds | news | free tiers delayed; NewsAPI dev-only |

## D6. Caching policy (starting TTLs — tune from measured hit rates)

| Data | TTL |
|---|---|
| Real-time quote | 1–5 s (only if provider permits) |
| Intraday bars | 15–60 s |
| Daily bars | 5–60 min (long after close) |
| Fundamentals | 6–24 h |
| Company profile | days |
| News | 1–5 min |
| Macro/economic | hours–1 day |
| Market status | per session boundary |
| Provider health | seconds |

Redis: hot quotes, response cache, rate limiting, sessions where appropriate, locks, news cache, provider health. Postgres: durable data. Market closed ⇒ stop intraday polling.

## D7. Request scheduler (priority)

1. actively viewed instrument → 2. watchlist → 3. market indices → 4. alerts → 5. background symbols. Adaptive refresh; centralized evaluation (one fetch serves all users and all alert rules). Never poll per user.

## D8. WebSocket

Browser → backend stream manager → cache → provider (single upstream connection shared by users, only where licensing permits). Implement reconnect, heartbeat, exponential backoff, subscribe/unsubscribe, per-user connection limits, provider failover, auth on connect, message schema versioning. Never open provider sockets from browsers.

## D9. Data quality engine

Validate every point: timestamp monotonic/valid tz; `price > 0`; `high ≥ max(open, close)`; `low ≤ min(open, close)`; `volume ≥ 0`; no NaN/Inf. Detect duplicates, gaps, outliers, provider timestamp drift. Tag `quality` per row; reject or flag, never silently repair.

## D10. Market calendar

Exchange calendars with timezones: NSE/BSE (IST), NYSE/NASDAQ (ET), LSE, Xetra, Euronext, TSE, HKEX, SSE, KRX, ASX. Handle weekends, holidays, pre/regular/post sessions, half-days. Never infer "open" from server local time.

---

# PART E — FEATURE SPECIFICATIONS

## E1. Market overview
Indices/instruments by region — **show only where a valid source exists; otherwise omit or show UNAVAILABLE.**
- India: NIFTY 50, NIFTY Bank, NIFTY Midcap, SENSEX, India VIX
- USA: S&P 500, NASDAQ Composite, Dow, Russell 2000, VIX
- Europe: FTSE 100, DAX, CAC 40, STOXX 50
- Asia: Nikkei 225, Hang Seng, Shanghai Composite, KOSPI, ASX 200
- Global: DXY, US 10Y, Brent, WTI, Gold, Silver, Bitcoin, Ethereum
Plus global cross-market heatmap (rows: India, USA, Europe, Asia, Commodities, FX, Crypto; color by D/W/M %) and sector heatmaps (India: IT, Banking, Fin Services, Pharma, Auto, Energy, FMCG, Metals, Realty, Telecom, Consumer, Industrials; US: 10 GICS-style sectors). Sector data must come from real index/constituent data.

## E2. Charting (Lightweight Charts or other license-compatible OSS; no proprietary TradingView code)
- Types: Candlestick, Line, Area, Bar, Baseline, Heikin Ashi, OHLC.
- Timeframes: 1m 3m 5m 15m 30m 1h 2h 4h 1D 1W 1M — each enabled only if provider-supported.
- Controls: zoom, pan, crosshair, fullscreen, auto-scale, % scale, log scale, reset, compare symbol, save layout, drawings (trend line, horizontal line, rectangle, Fibonacci, text).
- News/earnings markers on chart; click → headline, source, time, sentiment, importance, summary.
- Perf: windowed data loading, incremental updates, indicator calc in a Web Worker, lazy-loaded modules, memoization; mobile loads smaller windows with pagination.
- Chart tests: render, data update, indicator overlay, timeframe switch, empty-data state.

## E3. Indicators (deterministic, unit-tested against known reference datasets)
SMA, EMA, WMA, VWAP, RSI, MACD, Bollinger, ATR, ADX, Stochastic, CCI, ROC, Momentum, OBV, MFI, Williams %R, Parabolic SAR, Ichimoku, Supertrend. Configurable params, multiple instances, overlay or separate panel, visibility/color/style, reset. Document the exact formula variant used (e.g., Wilder smoothing vs EMA) in `docs/`. Cross-validate against a trusted library (e.g., TA-Lib/pandas-ta) in tests with tolerance.

## E4. Support/Resistance engine
Methods: swing highs/lows, pivots, volume profile (if volume data permits), MA zones, prior day/week/month H/L, Fibonacci, repeated-rejection zones, breakout/retest zones.
Output per level: `type(support|resistance)`, `zone_low`, `zone_high`, `strength`, `touch_count`, `distance_percent`, `timeframe`, `method`, `confidence`. Use **zones** (ATR-scaled width), merge nearby levels, never claim a guaranteed level.

## E5. Candlestick patterns
Doji, Hammer, Inverted Hammer, Shooting Star, Hanging Man, Bullish/Bearish Engulfing, Morning/Evening Star, Piercing Line, Dark Cloud Cover, Three White Soldiers, Three Black Crows, Inside Bar, Outside Bar, Marubozu, Spinning Top.
Output: `name, direction, timestamp, timeframe, strength, confirmation_required, context (trend/location), historical_frequency` (only if measurable). Explicit numeric definitions per pattern (body/shadow ratios) in code and docs. Not predictions.

## E6. Chart patterns
Head & Shoulders (+inverse), Double/Triple Top/Bottom, Ascending/Descending/Symmetrical Triangle, Wedge, Flag, Pennant, Rectangle, Cup & Handle, Breakout, Breakdown, Channel.
Output: `pattern, start_time, end_time, direction, neckline, breakout_level, target_zone, invalidation, confidence, confirmation_status (FORMING|CONFIRMED|FAILED)`. Use pivot-based detection with tolerance parameters; **no look-ahead** — a pattern is only reported at the bar when it becomes knowable; add replay tests that run detection bar-by-bar.

## E7. Volume analysis
Spikes, volume trend, relative volume (vs N-day same-time average), OBV, accumulation/distribution, breakout-volume confirmation. Flag e.g. "Breakout lacks volume confirmation."

## E8. Multi-timeframe analyzer
Trend per timeframe (1m, 5m, 15m, 1h, 4h, 1D, 1W where data exists) using a documented rule (e.g., EMA stack + structure + ADX). Output `trend_<tf>` and `overall_bias ∈ {STRONGLY_BULLISH, BULLISH, NEUTRAL, BEARISH, STRONGLY_BEARISH}` with weights documented; missing timeframes are excluded and reported, not guessed.

## E9. Relative strength / alpha
India vs NIFTY 50, NIFTY Bank, sector index; US vs S&P 500, NASDAQ. Compute `relative_return, relative_strength (ratio line), beta, correlation, rolling_alpha, benchmark_outperformance`. Aligned timestamps, same currency/session handling. Chart modes: Price / Benchmark / Relative Strength.

## E10. Macro correlation
Universe: NIFTY, DXY, US10Y, Brent, WTI, Gold, India VIX, S&P 500, NASDAQ, Dow. Output: correlation matrix, rolling correlation, divergence detection, macro pressure score, regime label (`risk-on|risk-off|mixed|neutral|supportive`). Always label "correlation, not causation." Handle timezone/holiday alignment (use returns on common dates).

## E11. News engine
Categories: Indian Markets, Global Markets, Company, Earnings, M&A, Central Banks, Rates, Inflation, Geopolitics, Conflicts, Oil, Gold, Currency, Technology, Banking, Semiconductors, AI, Regulation. Tabs: GLOBAL, INDIA, COMPANIES, MARKETS, GEOPOLITICS, BUSINESS, CENTRAL BANKS, COMMODITIES, CURRENCY. Search by company/ticker/topic/country/sector; filters: latest/1h/today/week.
Stored fields: `title, description, source, url, canonical_url, published_at, retrieved_at, symbols, companies, countries, topics, sentiment, importance, content_hash`. Dedup on canonical URL + headline hash + source + published time. Incremental polling. UI shows LIVE/DELAYED + last-updated; never call a delayed feed real-time.

## E12. News sentiment
Pipeline: article → language detect → clean → entity extraction → financial sentiment (local FinBERT-class model where feasible) → importance → symbol mapping → DB. Output `sentiment_score, confidence, importance, market_impact_probability(only if validated), label ∈ {VERY_POSITIVE…VERY_NEGATIVE}`. Gemini only for escalated deep reasoning, not bulk.

## E13. Fundamentals
Profile (market cap, sector, industry, employees); valuation (P/E, fwd P/E, P/B, PEG, EV/EBITDA, div yield, P/S); profitability (revenue, gross/operating/net margin, ROE, ROA, ROIC); health (debt, cash, D/E, current ratio, FCF); growth (revenue, EPS, profit); earnings (last, next, EPS & revenue surprise). Show 1/3/5-year trends with charts. Normalization layer: Ind-AS/SEBI-style vs US GAAP/IFRS → common schema; each metric retains `source, original_field, normalized_field, currency, period, accounting_standard, available_from` (availability date used for point-in-time correctness). Cache aggressively; refresh daily/weekly.

## E14. Forex dashboard
Pairs: USD/INR, EUR/USD, GBP/USD, USD/JPY, USD/CHF, AUD/USD, USD/CAD, NZD/USD, EUR/GBP, EUR/JPY (+ more within limits). Show rate, change, %, day H/L, timestamp. Ranges 1D/5D/1M/3M/6M/1Y/5Y; candlestick only where OHLC exists. Frankfurter for daily reference; intraday via provider layer.

## E15. Macro dashboard
DXY, US10Y, US2Y, Brent, WTI, Gold, Silver, VIX, India VIX, NIFTY, S&P 500, NASDAQ, Dow — price, change, trend, chart, correlation, market-impact note.

## E16. Watchlists, alerts, notifications
- Watchlists: stocks, indices, forex, commodities, crypto (where supported); show price, change, trend, signal, alert state.
- Alerts: price above/below, % change, support/resistance break, RSI threshold, MACD cross, volume spike, pattern detected, news event, sentiment change. Flow: Rule → Evaluator (centralized) → Event → Notification. Idempotent firing, cooldowns, dedup.
- Notifications: in-app now; interface ready for email/push/Telegram/mobile push.

## E17. Auth & profiles
Supabase Auth (email/password, email OTP, phone OTP where available, reset, verification, sessions, sign-out). Roles `USER, ANALYST, ADMIN, SUPER_ADMIN` enforced **server-side** (JWT claims verified + DB role check; RLS on user tables). Profile: name, email, phone, timezone, currency, preferred market, default timeframe, theme, risk preference. Never store passwords yourself.

## E18. Backtesting & Strategy Lab
- Backtester (browser/server hybrid): strategy rules, entry/exit/stop/target, sizing, fees, slippage; metrics: total return, CAGR, max DD, Sharpe, Sortino, win rate, profit factor, expectancy; timeframes 1m–1D where data exists; **no look-ahead** (signals on bar close, fills next bar open unless stated).
- Strategy Lab: declarative conditions/indicators/rules (JSON DSL). **Never execute arbitrary user Python on the server.** If custom code is ever added: sandboxed restricted JS/WASM, no FS/network/shell/process, CPU/memory/time limits.

---

# PART F — DATABASE (Supabase PostgreSQL, TimescaleDB-ready)

## F1. Tables
`users/profiles` (auth-linked), `user_preferences`, `watchlists`, `watchlist_items`, `saved_charts`, `alerts`, `alert_events`, `exchanges`, `markets`, `symbols`, `instruments`, `quotes`, `ohlcv`, `fundamentals`, `financial_statements`, `corporate_events`, `news_articles`, `news_sources`, `news_sentiment`, `macro_series`, `forex_rates`, `index_members`, `provider_health`, `provider_requests`, `ai_analysis`, `ai_analysis_features`, `ai_predictions_v2`, `ai_prediction_outcomes`, `audit_logs`.

## F2. OHLCV design

```sql
CREATE TABLE ohlcv (
  instrument_id  BIGINT      NOT NULL REFERENCES instruments(id),
  exchange_id    SMALLINT    NOT NULL REFERENCES exchanges(id),
  timeframe      TEXT        NOT NULL CHECK (timeframe IN ('1m','3m','5m','15m','30m','1h','2h','4h','1D','1W','1M')),
  ts             TIMESTAMPTZ NOT NULL,
  open  NUMERIC(20,8) NOT NULL CHECK (open  > 0),
  high  NUMERIC(20,8) NOT NULL,
  low   NUMERIC(20,8) NOT NULL,
  close NUMERIC(20,8) NOT NULL CHECK (close > 0),
  volume NUMERIC(24,4) CHECK (volume >= 0),
  source   TEXT NOT NULL,
  quality  TEXT NOT NULL DEFAULT 'OK',
  ingested_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CHECK (high >= GREATEST(open, close) AND low <= LEAST(open, close)),
  UNIQUE (instrument_id, timeframe, ts, source)
);
CREATE INDEX ON ohlcv (instrument_id, timeframe, ts DESC);
```
Bulk upserts (`ON CONFLICT DO UPDATE`), no N+1, partition-by-time plan for later `create_hypertable`. **Retention:** intraday bars pruned by policy (e.g., 1m kept N days — decide after storage measurement); no unbounded tick storage.

## F3. Ground rules
Migrations are versioned, reversible, reviewed; foreign keys + constraints everywhere; RLS on user-owned tables; indexes justified by query plans (`EXPLAIN`); documented backup/restore strategy; data-quality check jobs; separate V2 ledger tables never join-write into V1 ledger.

---

# PART G — AI ANALYSIS & PREDICTION

## G1. Orchestrated pipeline
```
Market data + indicators + candle patterns + chart patterns + S/R + volume
+ multi-timeframe + relative strength + fundamentals + news + macro + risk context
   → Feature Builder → Quant Scoring → Gemini reasoning → Scenario Engine → Risk Engine
   → Schema validation → User explanation
```
Internal tools the orchestrator may call: `get_quote, get_history, get_indicators, get_patterns, get_support_resistance, get_fundamentals, get_news, get_macro, get_relative_strength, get_market_status, get_risk_metrics`. The assistant must retrieve current structured data **before** reasoning on any market question.

## G2. Output contract (Pydantic-validated; malformed ⇒ reject/retry once/fail safe)

```json
{
  "symbol": "RELIANCE.NS",
  "as_of": "ISO-8601",
  "bias": "STRONGLY_BULLISH|BULLISH|NEUTRAL|BEARISH|STRONGLY_BEARISH",
  "confidence": 0.0,
  "confidence_kind": "heuristic|calibrated",
  "current_price": 0,
  "scenarios": {"bull": {}, "base": {}, "bear": {}},
  "setup": {
    "setup_type": "BREAKOUT|BREAKDOWN|PULLBACK|TREND_CONTINUATION|REVERSAL|RANGE_TRADE|MOMENTUM|MEAN_REVERSION",
    "timeframe": "1D",
    "entry_zone": [0, 0],
    "stop_loss": 0,
    "targets": [0, 0],
    "risk_reward": 0,
    "status": "WAIT_FOR_CONFIRMATION|ACTIVE|INVALIDATED|NO_SETUP",
    "confirmation_required": [],
    "invalidation": []
  },
  "reasons": [], "risks": [],
  "evidence": {"trend":{}, "momentum":{}, "sr":{}, "candles":{}, "patterns":{}, "volume":{}, "relative_strength":{}, "fundamentals":{}, "news":{}, "macro":{}},
  "data_status": {},
  "warning": ""
}
```

## G3. Guardrails (hard rejections)
Hallucinated prices (any price not within tolerance of provided data/derived levels); missing timestamps; negative prices; stop on wrong side of entry; targets on wrong side; impossible/zero risk-reward; unsupported symbol/timeframe; stale data presented as live. Missing data ⇒ "Insufficient data for a reliable analysis." Every analysis ends with a **RISK WARNING** block (invalidation level, no-guarantee language) and a **DATA WARNING** if delayed/EOD/stale.

## G4. Setup rules (explicit, testable)
Example BREAKOUT: `close > resistance_zone_high AND relative_volume > threshold AND higher-TF trend != STRONGLY_BEARISH` → entry = breakout/retest zone; stop = structural invalidation (below retest low / ATR-buffered); target = measured move or ATR-multiple. Define equivalent rule tables for each of the 8 setup types in `docs/AI_ANALYSIS.md`.

## G5. Risk engine
Compute `risk_per_share, stop_distance, position_size, portfolio_risk, risk_reward, max_loss, target_profit`; honor user risk preference and portfolio constraints when available; never assume unlimited risk tolerance; position size capped by max-risk-% and max-position-%.

## G6. Response format (chat/report)
SUMMARY · MARKET REGIME · TECHNICAL · CANDLESTICK · PATTERNS · S/R · VOLUME · MULTI-TIMEFRAME · FUNDAMENTALS · NEWS · MACRO · TRADE SCENARIOS (BULL/BASE/BEAR) · ENTRY ZONE · STOP · TARGETS · RISK/REWARD · INVALIDATION · CONFIDENCE · DATA STATUS · WARNING. Explanations must cite the evidence fields used; never output a bare "BUY".

## G7. Prediction engine (separate from V1)
- Start simple: logistic regression, gradient boosting/random forest; XGBoost/LightGBM only if dependencies are reasonable; calibrate (Platt/isotonic).
- Features: returns, volatility, RSI, MACD, ATR, EMA distance, volume, relative volume, S/R distance, pattern features, regime, benchmark return, DXY, VIX, news sentiment, fundamentals (point-in-time).
- Validation: **walk-forward only**, never random shuffle; splits TRAIN / VALIDATION / TEST / LIVE; purge/embargo around label horizons.
- Metrics: accuracy, precision, recall, F1, ROC-AUC (where meaningful), Brier, calibration curve, profit factor, max drawdown, Sharpe, Sortino, win rate, avg win/loss, trade count — reported with sample sizes and confidence intervals.
- **Leakage tests (mandatory, automated):** feature at T uses only data ≤ T; news by publication time; fundamentals by availability date; indicators from past candles only; labels generated after prediction timestamp; shifting-future-data test must change nothing.
- Ledger V2: append-only, prediction stored with model version + feature hash + timestamp *before* outcome is known; outcomes resolved by a scheduled job; no edits.
- Never publish an accuracy figure that isn't computed from the V2 ledger/validation outputs.

---

# PART H — PLATFORM CONCERNS

## H1. API (`/api/v2`, V1 untouched)
`GET /markets/overview`, `/markets/indices`, `/quotes/{symbol}`, `/history/{symbol}`, `/fundamentals/{symbol}`, `/news`, `/news/{symbol}`, `/forex`, `/macro`, `/analysis/{symbol}` (GET cached, POST fresh), `/patterns/{symbol}`, `/support-resistance/{symbol}`, `/alerts` (GET/POST), `/watchlists` (GET/POST), `/system/providers` (admin), `/health`. OpenAPI with schemas, examples, errors, auth, rate limits. TypeScript types generated from OpenAPI; no `any` for financial objects.

Structured errors:
```json
{"status":"ERROR","code":"PROVIDER_RATE_LIMIT","message":"Market data provider rate limit reached.","retry_after":30,"provider":"twelvedata","request_id":"..."}
```
The frontend maps codes to useful messages — never a bare "Failed to fetch".

## H2. Security
OWASP Top 10 pass; CORS allowlist (`FRONTEND_ORIGIN`, no wildcard with credentials); CSRF where cookies are used; security headers (CSP, HSTS, X-Content-Type-Options, frame-ancestors, Referrer-Policy); secure/HttpOnly/SameSite cookies; JWT validation (signature, expiry, audience); server-side RBAC; parameterized queries/ORM only; input & response validation; XSS-safe rendering of news HTML; audit logs; secret scanning in CI (e.g., gitleaks); dependency audits. Rate limits: anonymous low → authenticated higher → admin controlled; AI and news-search strict; return `429` + `Retry-After`. Never log passwords, API keys, JWTs, session tokens.

Secrets (backend env only): `GEMINI_API_KEY, TWELVEDATA_API_KEY, FINNHUB_API_KEY, ALPHAVANTAGE_API_KEY, SUPABASE_SERVICE_ROLE_KEY, DATABASE_URL, UPSTASH_REDIS_REST_TOKEN, FRED_API_KEY, NEWSDATA_API_KEY, CURRENTS_API_KEY, GNEWS_API_KEY`. Frontend may only receive explicitly public values (`SUPABASE_URL`, `SUPABASE_ANON_KEY` under RLS). Provide `.env.example` (names only); `.env` git-ignored.

## H3. Observability
Structured JSON logs with `request_id, timestamp, endpoint, user_id?, provider, error_code, latency_ms`. Metrics: request_count, error_count, provider_latency, cache_hit_rate, websocket_connections, AI_requests/failures/latency, DB query latency; expose `provider_latency_ms, backend_latency_ms, serialization_ms` (and frontend render time) per response. Report **p50/p95/p99** for quote API, history API, AI analysis, DB, Redis, WebSocket delivery. Never claim "sub-millisecond" or any figure that wasn't measured.

## H4. Admin dashboard
Provider health (status, latency, last success/failure, quota, circuit state), API usage, cache hit ratio, DB health, error rate, active users, AI usage, news & market ingestion status, WebSocket connections, rate-limit events. Admin routes enforce RBAC server-side.

## H5. Frontend / UX
Navigation: Dashboard, Markets, Stocks, Charts, AI Analysis, News, Fundamentals, Forex, Macro, Scanner, Watchlist, Alerts, Portfolio, Strategy Lab, Settings. Stock page sections: Header (name, price, change, exchange, market status, data timestamp) → Chart → AI Analysis → Technical → Fundamentals → News → Macro. Every data widget shows its data-status badge. Mobile-first responsiveness, PWA-ready (manifest, service worker for app shell + cached last-good data), swipe timeframes, compact indicators, windowed history. Follow the existing design system.

## H6. Feature flags
`V2_MARKET_DATA, V2_AI_ANALYSIS, V2_NEWS, V2_FOREX, V2_FUNDAMENTALS, V2_ALERTS, V2_BACKTESTING, V2_AUTH` — server-evaluated, default OFF in production until acceptance.

## H7. Deployment
Keep Vercel + Render. V2 UI under `/v2` (or separate V2 deployment); API under `/api/v2`. Staging first; V1 never replaced until V2 passes acceptance. Document cold-start mitigation for Render free tier. Docker/NGINX/gateway/Kafka/Flink/ClickHouse remain *designs*, not deployments, until justified by measurements.

---

# PART I — PHASES WITH GATES

Each phase ends with: changed-files report, tests/lint/type/build results, security check, rollback note, and **approval gate**.

| # | Phase | Deliverables | Exit gate |
|---|---|---|---|
| 1 | Audit (read-only) | Part C A–O | Written approval |
| 2 | Provider abstraction | 4 provider interfaces, normalized models, adapters, ProviderManager, circuit breaker, contract tests | all adapters pass same contract suite |
| 3 | Caching & quotas | CacheService, Redis, coalescing, QuotaManager, Postgres base schema/migrations | "100 users → 1 provider call" test passes |
| 4 | Market Overview V2 | indices, forex, commodities, macro, heatmaps, status badges | no fabricated values; UNAVAILABLE states verified |
| 5 | Charting | candles/lines/etc., indicators UI, drawings, multi-timeframe, compare | chart tests + mobile check |
| 6 | Technical analysis | indicators, candles, patterns, S/R, volume engines | known-dataset tests, bar-by-bar replay no look-ahead |
| 7 | Fundamentals | statements, ratios, trends, normalization | schema retention of source/original field |
| 8 | News | ingestion, dedup, tabs, search | dedup test, delayed labeling |
| 9 | News sentiment | NLP pipeline | label/score validation set results |
| 10 | AI analysis | tool orchestrator, Pydantic guardrails | malformed/hallucinated-output tests pass |
| 11 | Prediction engine | models, walk-forward, calibration, ledger V2 | leakage tests pass; V1 ledger hash unchanged |
| 12 | Risk engine | entry/stop/targets/RR/sizing | invalid-geometry rejection tests |
| 13 | Auth | Supabase Auth, roles, profiles, watchlists, RLS | unauthorized/admin-route tests |
| 14 | Alerts | rules, evaluator, in-app notifications | centralized evaluation, no per-user polling |
| 15 | Admin | provider health, usage, metrics | RBAC verified |
| 16 | Performance | WebSockets, batching, workers, profiling | measured p50/p95/p99 report |
| 17 | Security | OWASP, rate limits, secrets, audit | security test suite green |
| 18 | Testing | unit/integration/load/security/data-quality | Part J scenarios all covered |
| 19 | Staging deployment | `/v2` on staging, flags | V1 unaffected (smoke tests) |
| 20 | Production validation | acceptance checklist | all boxes ticked with evidence |

---

# PART J — TESTING & ACCEPTANCE

## J1. Mandatory scenarios
1 valid data · 2 empty data · 3 malformed JSON · 4 provider 429 · 5 provider 500 · 6 timeout · 7 cache hit · 8 cache expired · 9 two users same symbol (coalesced) · 10 market closed · 11 weekend · 12 holiday · 13 invalid symbol · 14 unsupported timeframe · 15 AI gets incomplete data · 16 AI returns malformed JSON · 17 unauthorized user · 18 non-admin hits admin route · 19 missing API key · 20 database unavailable. Plus: circuit-breaker state transitions, quota exhaustion fallback, NaN/Inf sanitization, OHLC integrity violations, timezone/DST handling, V1 regression suite, V1 ledger immutability, leakage tests, load tests, security tests.

## J2. Acceptance checklist (V2 is not complete until every item has evidence)
- [ ] V1 remains functional (regression suite green)
- [ ] `/api/v2` versioned; OpenAPI published
- [ ] Provider abstraction + normalized models; provider timestamps preserved
- [ ] LIVE/DELAYED/EOD/STALE/UNAVAILABLE visible in UI
- [ ] No fabricated data anywhere; no API keys in frontend bundle (bundle scan)
- [ ] Indices dashboard, charts (candle + line), indicators, S/R, candle patterns, chart patterns, volume, multi-timeframe, relative strength, macro correlation
- [ ] News dashboard, company news, dedup, sentiment
- [ ] Fundamentals, statements, valuation metrics
- [ ] AI analysis uses current structured data, cannot fabricate prices, returns validated structured output, includes warnings
- [ ] Risk/reward and entry/stop/target scenarios
- [ ] Forex dashboard
- [ ] Auth, sign-out, server-side admin authorization, watchlists, alerts
- [ ] Redis cache, quota manager, circuit breakers, provider fallback
- [ ] DB constraints (incl. no duplicate OHLCV)
- [ ] Security tests pass; frontend build passes; backend tests pass; no secrets committed
- [ ] No look-ahead in prediction engine; V2 evaluation separate from V1 ledger
- [ ] Measured p50/p95/p99 reported (no unmeasured claims)

---

# PART K — DOCUMENTATION TO PRODUCE

`docs/V2_ARCHITECTURE.md`, `DATA_PROVIDERS.md`, `DATA_PROVIDER_MATRIX.md`, `API_V2.md`, `AI_ANALYSIS.md`, `PREDICTION_ENGINE.md`, `RISK_ENGINE.md`, `DATABASE.md`, `SECURITY.md`, `DEPLOYMENT.md`, `TROUBLESHOOTING.md`, `OBSERVABILITY.md`.

**Provider matrix columns:** Provider · Asset · Market · Realtime · Delayed · Historical · Fundamentals · News · WebSocket · Free Limit · Public Display · Commercial Use · Fallback · Notes — covering Twelve Data, Alpha Vantage, Finnhub, yfinance, NSE, BSE, Supabase, Upstash, NewsData, Currents, GNews, FRED, Frankfurter. Each cell cites its source URL and `verified_on` date; unverifiable cells say `UNVERIFIED`.

## Final V2 report (at completion)
1 architecture summary · 2 files changed · 3 new files · 4 DB migrations · 5 endpoints · 6 provider integrations · 7 frontend modules · 8 AI architecture · 9 prediction architecture · 10 security architecture · 11 caching architecture · 12 WebSocket architecture · 13 test results · 14 build results · 15 performance measurements · 16 provider limitations · 17 known limitations · 18 upgrade path · 19 deployment instructions · 20 env-var list **without values**.

---

# PART L — HARD "DO NOT" LIST

Do not: fabricate data/candles/news/fundamentals/accuracy · claim guaranteed profit · expose or hardcode secrets · bypass API limits or exchange restrictions · scrape protected endpoints irresponsibly · fake realtime · touch the V1 ledger · introduce look-ahead · shuffle time series · run user Python on the server · deploy Kafka/Flink for show · rewrite working V1 code needlessly · remove V1 features · change production untested · weaken CORS · disable auth to fix bugs · hide provider failures · label delayed data as realtime.

---

# START NOW

Execute **Phase 1 only** (Part C). Return deliverables A–O plus the V1→V2 migration map and dependency map. Modify nothing. Wait for approval.
