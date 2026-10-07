# AIplannedcld2.md — EquiNexa AI: Trading-Platform Upgrade Specification (Phase 2)

| Item | Value |
|---|---|
| Document type | Planning / implementation blueprint (NOT an implementation report) |
| Baseline specification | `AIplannedcld.md` (uploaded; **left unmodified**; SHA-256 `61c0f22c7d38acbef3c17a94bd595d73b31d9554953ccaea98d057c957c0aaed`, 1,930 lines) |
| Written | 2026-10-03 |
| Audience | A coding agent / senior engineer executing phase by phase |
| Product | EquiNexa AI — AI-driven market intelligence, charting, prediction and research |
| Hard constraints | No brokerage/order placement. No profit guarantees. No fabricated data, citations, results or provider capabilities. Frozen model `1.0.0` and all historical/prospective records are immutable. |

---

## 0. Purpose, Scope and How to Use This Document

### 0.1 Purpose
`AIplannedcld.md` specifies the AI/ML core (RAG, LLM abstraction, technical features, pattern engines, ensemble, calibration, leakage prevention). It is **daily-bar centric** and treats intraday as best-effort/[FUTURE]. It says nothing about a professional charting workspace, a trader's daily workflow, fundamentals, risk tooling, journaling, or setup-level evidence.

This document **extends** the baseline. It adds:

1. A full charting workspace (ranges, intervals, chart types, indicators, drawings) comparable in *function* to retail platforms such as Angel One, with EquiNexa branding.
2. Data-driven (OHLCV) chart analysis and horizon-explicit forecasting, separate from screenshot analysis.
3. A fixed Research Assistant that answers the question actually asked.
4. Market-data and LLM-provider correctness and resilience.
5. A **trader toolkit** the baseline lacks: intraday session indicators, index/market context, fundamentals, scanners, scenario-based trade plans, risk/cost math, paper trading, journaling, setup-level evidence ("setup lab") and a prospective intraday signal ledger.

### 0.2 Authoring stance (read this)
Section 2 and the trader modules are written from a **risk-first intraday-practitioner lens**: most retail intraday traders lose money, costs are a hard hurdle, and discipline failures (oversizing, revenge trading, no stop) cause more damage than weak signals. The product should therefore make *good process easy* and *bad process visible*. I am an AI; I have no trading track record and this document does not promise that any user will profit. It specifies **tools for research, risk control and honest self-measurement**, not a money machine.

### 0.3 Status legend (extends baseline §0.1)

| Tag | Meaning |
|---|---|
| **[CONFIRMED]** | Verified from material actually inspected in this task (the baseline file). |
| **[CLAIMED-UNVERIFIED]** | Stated in the task brief but not verifiable from the material available here. The coding agent must verify in Phase 1. |
| **[REQUIRED]** | Needed for acceptance. |
| **[PLANNED]** | Intended design; details may be refined. |
| **[EXPERIMENTAL]** | Must be flag-gated and labelled in UI and API. |
| **[OPTIONAL]** | Only if free data/time permit. |
| **[FUTURE]** | Deferred; keep interfaces extensible. |
| **[VERIFY]** | A provider/library/regulatory fact (quota, fee rate, license, API shape) that must be checked against current official sources at implementation time and logged with date. |

### 0.4 Evidence rule for the coding agent
A phase is complete only when `docs/evidence/phase-NN.md` exists containing: commit hash, commands run, test output summaries, screenshots (UI phases), and a checked acceptance list. "Looks right" is not evidence. Do not mark anything done on the basis that a file/function/route/test exists.

### 0.5 Non-fabrication rules (inherited from baseline §0.2, restated)
No invented prices, news, citations, filings, fundamentals, metrics, quotas, fee rates or capabilities. Mock data is allowed **only** in files under `tests/`, `fixtures/`, `demo/` and must carry a `synthetic: true` marker; production code paths must fail closed (return `unavailable`) rather than substitute sample data. A startup check and a CI grep gate must block importing fixtures from production modules.

---

## 1. Baseline Audit

### 1.1 Materials available vs. unavailable (limitation statement)

| Material required by the brief | Available in this task? | Consequence |
|---|---|---|
| `AIplannedcld.md` | **Yes** (uploaded) | Fully read; findings in §1.2–1.4 are **[CONFIRMED]** *about the specification*. |
| Frontend source (routes, components, state, chart library, API client, styles) | **No** | Cannot state what is implemented. All frontend facts are **[CLAIMED-UNVERIFIED]**. |
| Backend source (providers, ticker normalisation, schemas, indicators, pattern engines, ML inference, news ingestion, research endpoints, provider config) | **No** | Same. |
| Existing tests, evaluation scripts, model cards | **No** | Same. |
| `docs/FINAL_ACCEPTANCE_AUDIT.md` | **No** | Same; baseline file does not reference it (0 matches). |

**Therefore this document contains no code-level audit findings.** Inventing them would violate the brief ("state the limitation instead of inventing findings"). Instead §1.6 defines a mandatory, scripted Phase 1 audit that produces the real baseline, and every later phase has a *"Files to inspect"* list to be resolved against actual paths.

### 1.2 What the baseline specification contains **[CONFIRMED]**
- 65 numbered sections + appendices; every component tagged `[IMPLEMENTED LATER]/[PLANNED]/[EXPERIMENTAL]/[OPTIONAL]/[FUTURE]` — i.e. the baseline itself is a *plan*, not proof of implementation.
- Provider-agnostic LLM layer (§3), embeddings (§4), vector store abstraction (§5), news RAG (§6), leakage prevention (§7, with ten automated tests), technical features (§8), targets (§9), baseline model (§10), sentiment (§11–14), 13 candlestick patterns (§15), 14 chart patterns (§16), screenshot analysis (§17), multimodal fusion (§18–19), ensemble/calibration/validation/evaluation/ablation (§20–25), research-only backtesting (§26), explainability (§27–28), research assistant (§29–31), multi-market/commodity (§32–35), events (§37–38), confidence (§39), missing data (§40), caching (§41), cost control (§42), fallback (§43), security (§44–45), `/api/ai/*` endpoints (§46), canonical output schema (§47), registry/tracking/reproducibility (§48–50), tests (§51–54), drift/regime (§55–56), directory layout (§57), MLOps (§58), free-tier architecture (§59), acceptance (§62), report format (§63).
- The 48% → 96% figure is treated as a **reported, unverified** benchmark requiring leakage-free reproduction (baseline §10.3, §24).
- Language policy forbidding "buy this stock", guarantees, etc. (baseline §1.3).

### 1.3 Gap analysis against the new brief **[CONFIRMED against the baseline text]**
Match counts are from case-sensitive `grep -c` on `AIplannedcld.md`.

| Capability requested now | Baseline coverage | Evidence | Gap |
|---|---|---|---|
| Range selector incl. 1D…Max + custom dates; real re-fetch | Not specified | No "range"/UI sections; caching table mentions `(symbol, interval, range, provider)` only | **Full spec needed** |
| Intraday intervals 1m–4H | "Daily by default; intraday only if data source provides it" (§15.5); "Intraday / real-time streaming [FUTURE]" (App. A) | `intraday`: 4 matches | **Conflict** with new brief → upgrade to [REQUIRED] where provider allows |
| Chart types (line/area/OHLC/candles/Heikin-Ashi) | Not specified | `Heikin`: 0 | **Full spec needed** |
| Indicator UI + params | Indicator *features* for ML only (§8) | `VWAP`: 0, `Supertrend`: 0 | VWAP, Supertrend, parameterised overlay/panel UX missing |
| Drawing tools | Not specified | — | **Full spec needed** |
| Candlestick patterns incl. Harami, Hanging Man | 13 patterns (§15.2) | `Harami`: 0, `hanging`: 0 | Add Harami (bull/bear), Hanging Man; define trend-context tests |
| Chart patterns incl. flags/pennants/wedges/channels | 14 patterns (§16.2) | Present | Needs deterministic acceptance fixtures; calibration |
| Data-driven chart analysis workflow | Partially (technical + patterns + ML inside `/api/ai/analyze`, §46) | — | Needs explicit selected-range/timeframe contract, no silent symbol fallback |
| Forecast with explicit horizon/target/threshold/OOD warnings | Horizons 1–20D (§9); no intraday horizons; no OOD warning | — | Add intraday horizons, threshold targets, OOD + "not validated for this ticker/timeframe" |
| Research assistant for arbitrary queries | Pipeline specified (§29) but with enum intents incl. `out_of_scope` | — | Add planner/tool-use design, query-preservation tests, follow-ups, section statuses |
| Provider resilience incl. Yahoo 404, Gemini 503 | Generic (§3.4, §43) | `Yahoo`: 1, `404`: 0, `503`: 0 | Add error taxonomy per HTTP class, permanent-vs-transient rules |
| Fundamental analysis | **None** | `fundamental`/`Fundamental`: 0 | **New module** |
| Index analytics (breadth, VIX, flows, global cues) | Index listed as instruments only; `India VIX`: 1 mention (regime) | — | **New module** |
| Intraday-trader tooling: opening range, pivots/CPR, gap analysis, RVOL-by-time | `pivot`: 5 (chart pivots only) | — | **New** |
| Scanner/screener | None | `screener`: 0 | **New** |
| Watchlist | None | `watchlist`: 0 | **New** |
| Trade journal / paper trading | None | `journal`: 0, `paper`: 0 | **New** |
| Position sizing, transaction-cost calculator | Backtest costs only (§26) | — | **New (user-facing)** |
| Scenario trade plan with invalidation | Pattern invalidation only (§15–16) | — | **New** |
| Setup-level evidence ("does this setup have edge after costs?") | Model-level backtest only | — | **New** |
| Frozen model `1.0.0`, prospective ledger | **Not mentioned** | `1.0.0`: 0, `prospective`: 0 | **[CLAIMED-UNVERIFIED]**; preserve whatever exists |

### 1.4 Defects / inconsistencies found in the baseline document **[CONFIRMED]**
1. **Self-title mismatch:** the file is titled `AIplanned.md` internally but supplied as `AIplannedcld.md`. Treat as the same document; do not rename either.
2. **Intraday contradiction:** baseline non-goal says "daily bars are the core" and App. A marks intraday [FUTURE]; the new brief requires 1m–4H intervals. Resolution: intraday becomes [REQUIRED] for *charting and session analytics*; **ML intraday forecasting remains [EXPERIMENTAL]** until walk-forward evidence exists (§9, §13 here).
3. **Pattern count vs brief:** brief lists Harami and Hanging Man; baseline omits them. Added in Phase 7.
4. **Endpoint prefix:** baseline uses `/api/ai/*`; real routes unknown. Phase 1 must reconcile; new market-data endpoints may live under a separate prefix (see §8).
5. **No UI/UX specification** exists in the baseline; nothing about accessibility or mobile.
6. **Benchmark language risk:** baseline requires the 48%→96% claim be reproduced; any README/UI copy asserting it as fact is an unsupported claim (check in Phase 1 §1.6 step 9).
7. **Tag semantics:** `[IMPLEMENTED LATER]` throughout means *no code is promised to exist*. Do not infer implementation from the baseline.

### 1.5 Claims in the task brief that cannot be verified here **[CLAIMED-UNVERIFIED]**
React/Vite/TypeScript frontend; Python/FastAPI backend; existing market-data integrations; AI Research Assistant; AI Chart Vision; technical indicators; ML inference; historical evaluation; prospective monitoring; frozen model version `1.0.0`; prospective ledger; `docs/FINAL_ACCEPTANCE_AUDIT.md`; Market Overview with a limited-range line chart; Yahoo Finance `404`s on unsupported symbols; Gemini `503`/model-config failures; Research Assistant failing on some queries / returning generic content; upload-security controls.

### 1.6 Mandatory Phase 1 code-audit protocol (the coding agent executes this first)

Output: `docs/audit/BASELINE_AUDIT_2.md` plus a machine-readable `docs/audit/baseline_audit.json`. Classification per feature: `IMPLEMENTED_VERIFIED` (code + passing test + manual run evidence), `IMPLEMENTED_UNVERIFIED`, `PARTIAL`, `STUB/PLACEHOLDER`, `MISSING`, `DEFECTIVE`, `UNSUPPORTED_CLAIM`.

1. **Inventory:** `git log --oneline | head -50`, `git status`, directory tree to depth 4, dependency manifests (`package.json`, lockfile, `pyproject.toml`/`requirements*.txt`), Node/Python versions, env var names (not values) from `.env.example`/settings classes.
2. **Frontend:** list routes/pages; locate Market Overview component; identify chart library & version; how range/interval state is held; whether range buttons trigger network calls (trace handler → API client → request params, and **observe in browser DevTools Network tab**); state management; API client; styling system; existing accessibility attributes; existing tests.
3. **Backend routes:** dump OpenAPI (`/openapi.json`) to `docs/audit/openapi_before.json`; list routers and schemas.
4. **Market data:** list providers, symbol normalisation function(s) (search for `.NS`, `.BO`, `suffix`, `normalize`), error handling for 404/empty/timeouts, caching, retry, rate-limit code, timezone handling, interval/range mapping tables.
5. **Indicators:** list implemented indicators, parameter handling, warm-up/NaN policy, whether computed server- or client-side; compare outputs to a reference on a fixture (see Phase 6).
6. **Pattern engines:** enumerate patterns *actually detected in code* (not docs/prompts); for each, find a unit test; record trend-context and look-ahead behaviour (does detection at bar *t* read bar *t+1*?).
7. **ML:** locate model `1.0.0` artefacts, model card, checksum; locate evaluation scripts, snapshots, prospective ledger; compute and record SHA-256 of every frozen artefact into `docs/audit/integrity_manifest.json` (this manifest is the immutability reference for §14.4).
8. **Research assistant:** trace form → payload → route → schema → prompt → retrieval → parsing → rendering. Specifically test hypotheses H1–H9 in §10.1 with recorded request/response pairs for ≥10 materially different queries.
9. **Claims scan:** grep README/docs/UI strings for `guarantee`, `100%`, `96%`, `accuracy`, `profit`, `buy`, `sell`, "live"; list unsupported claims.
10. **Tests/quality gates:** run backend tests, frontend tests, lint, type-check, production build; record pass/fail and counts. Failing baselines must be recorded, not hidden.
11. **Security review:** secrets in repo (gitleaks), upload validation code vs baseline §45, CORS, rate limit, prompt-injection handling.
12. **Reconcile** the audit against §1.3 and update the *Files to inspect/change* lists in Phases 2–16 with real paths.

### 1.7 Assumptions and unresolved questions

| ID | Question / assumption | Resolve in |
|---|---|---|
| Q1 | Which chart library is installed (e.g. Recharts, lightweight-charts, ECharts, Chart.js)? | Phase 1 |
| Q2 | Which market-data provider(s) are configured, and do they support intraday for Indian symbols? Is any paid/licensed feed available? | Phase 1–2 |
| Q3 | Is there user persistence (DB/auth)? Determines whether watchlists/journal/drawings are local-only or server-side | Phase 1 |
| Q4 | Exact route prefixes and existing request/response schemas | Phase 1 |
| Q5 | Which LLM providers/models are configured; current free-tier limits | Phase 3 |
| Q6 | Does a frozen-model artefact `1.0.0` exist and where; what horizon/universe/features does it support? | Phase 1 |
| Q7 | Which free source supplies fundamentals/filings for India and US with acceptable terms? | Phase 11 |
| Q8 | Is advance/decline, FII/DII, option-chain data obtainable from a licensed or permitted free source? (Scraping that violates ToS is **not** allowed.) | Phase 11 |
| Q9 | Deployment target and RAM/CPU limits (affects server-side indicator and scanner budgets) | Phase 16 |
| A1 | Users are individual traders; app is research/education only | — |
| A2 | Data is delayed or end-of-day unless a licensed real-time feed is configured; UI labels accordingly | Phase 2 |

---

## 2. Trader-Lens Principles

### 2.1 Why this matters
Retail intraday outcomes are poor on average (SEBI has published studies showing a majority of individual intraday and F&O traders lose money — **[VERIFY]** latest figures before quoting any number in product copy; do not hard-code statistics). A platform that only adds more signals will mostly add more trades, and more trades mean more costs. The upgrade therefore optimises for **decision quality, cost awareness, risk limits and measured feedback**.

### 2.2 Principles → product requirements

| # | Failure mode seen in losing intraday traders | Requirement in this spec |
|---|---|---|
| P1 | Trading without defined invalidation/stop | Scenario plans always carry trigger, invalidation, stop, targets; the UI refuses to show a plan without an invalidation level (Phase 12) |
| P2 | Oversizing / risking too much per trade | Position-size calculator from % risk; session risk meter; warnings when planned risk > configured cap (Phase 12) |
| P3 | Ignoring costs (brokerage, STT, fees, slippage) | Cost model in every plan; "breakeven win-rate" and "cost as % of expected move" displayed; low-edge warning (Phase 12) |
| P4 | Overtrading | Trade counters, daily trade/loss limits (advisory lock-out UI), time-of-day performance analytics (Phase 12) |
| P5 | Revenge trading / size-up after loss | Journal rules engine flags trades opened within N minutes of a loss or with larger size after a loss (Phase 12) |
| P6 | Trading illiquid / event-heavy / surveillance-listed names | Scanner liquidity filters + exclusion flags + event-calendar warnings (Phase 11) |
| P7 | Taking trades against the broader market/regime | Index context panel + day-type classifier + relative strength (Phase 11) |
| P8 | Believing a pattern/AI signal has edge without evidence | Setup lab: every named setup shows historical net-of-cost expectancy with confidence interval, or "no evidence" (Phase 13) |
| P9 | Hindsight and cherry-picked screenshots | Append-only prospective signal ledger and journal that cannot be silently edited (Phase 13) |
| P10 | Treating AI probability as certainty | Calibration-gated probability display; conflict flags; abstention (baseline §21, §28, §39 + Phase 9) |
| P11 | Late-day desperation trades; holding MIS past square-off | Session clock with broker-dependent square-off reminder (user-configurable, labelled "check your broker's time") (Phase 12) |
| P12 | Fundamentals ignored or misused (using quarterly data to time a 5-minute entry) | Fundamentals feed *selection and risk flags*, not entry timing; point-in-time dating (Phase 11) |

### 2.3 Language policy (extends baseline §1.3)
Forbidden additions: "sure shot", "jackpot", "easy money", "guaranteed target", "risk-free trade", "operator move", "must enter", "buy now", "sell now", "book profit now". Allowed trader-facing vocabulary: *scenario*, *setup*, *trigger*, *invalidation level*, *reference level*, *risk per trade*, *R-multiple*, *historical frequency*, *net of estimated costs*, *signal conflict*, *insufficient evidence*. Every plan/scenario screen carries: **"Scenario analysis for education and research. Not investment advice or a recommendation. You are responsible for your own decisions and risk."**

### 2.4 Non-goals (reaffirmed)
No order routing, no broker login, no portfolio sync, no social tips/copy-trading, no "guaranteed accuracy" marketing, no automatic execution, no scraping that violates a site's terms.

### 2.5 Profit-math primer (to be implemented in the cost/plan modules and shown in UI help)

Work in R-multiples (1R = money risked per trade = |entry − stop| × quantity). Let `R` = reward-to-risk of the plan, `p` = probability of reaching target before stop, `c` = round-trip cost expressed as a fraction of 1R (`c = total_costs / risk_amount`).

```
Net result if target hit  =  +R − c        (in R)
Net result if stop hit    =  −1 − c        (in R)
Expectancy E(R) = p·(R − c) − (1 − p)·(1 + c) = p·(R + 1) − (1 + c)
Breakeven win probability  p* = (1 + c) / (R + 1)
```
*Illustration only (not a result):* with R = 2 and c = 0.10, `p* = 1.10 / 3 ≈ 36.7%`; with R = 1 and c = 0.25, `p* = 1.25 / 2 = 62.5%`. Narrow-stop trades make `c` large (fixed costs ÷ small risk), which is why tiny-stop scalps are structurally hard after costs. The UI must show `c` and `p*` for every scenario and compare `p*` with the **historical hit-rate of that setup with its confidence interval** from the setup lab (Phase 13). If no evidence exists, display "No historical evidence for this setup on this instrument."

Position sizing:
```
risk_amount = capital × risk_pct
per_share_risk = |entry − stop| + est_slippage_per_share + est_cost_per_share
qty = floor(risk_amount / per_share_risk)           # then respect lot size / max exposure / liquidity cap
```
Liquidity cap: `qty ≤ participation_cap × typical_volume_in_trade_window` (default cap configurable, e.g. a small % of recent per-minute volume) to avoid unrealistic fills.

Daily loss limit: `lock_threshold = capital × daily_loss_limit_pct`; when realised + open P&L ≤ −lock_threshold the app shows an advisory lock-out banner ("Daily loss limit reached — consider stopping"). It cannot block broker actions (no integration) and must say so.

---

## 3. Market-Data Correctness and Provider Resilience (Foundation)

> Everything else depends on this section. Phase 2 and Phase 3 must be accepted before Phases 4+ begin.

### 3.1 Canonical instrument identity **[REQUIRED]**
Never derive a provider symbol by string concatenation. All symbols come from an **instrument master** (extends baseline §32.1).

| Field | Notes |
|---|---|
| `instrument_id` | Internal stable ID (e.g. `IN.XNSE.RELIANCE`, `US.XNAS.AAPL`, `CMDTY.COMEX.GC`) – never reused |
| `symbol`, `name`, `aliases[]` | Display symbol and legal/brand names |
| `exchange` + `mic` | XNSE, XBOM, XNYS, XNAS, … |
| `isin`, `bse_scrip_code` | Where available (disambiguates NSE/BSE listings and ADRs) |
| `instrument_type` | equity, index, etf, commodity_future, fx (if ever) |
| `currency`, `timezone`, `calendar_id` | INR/Asia-Kolkata/XNSE; USD/America-New_York/XNYS |
| `provider_symbols{provider: symbol}` | Explicit mapping, e.g. a provider's own NSE suffix—**from the master, verified by a probe** |
| `lot_size`, `tick_size`, `has_volume` | Indices usually have no meaningful volume → VWAP/volume features disabled with a reason |
| `status`, `listed_on`, `delisted_on`, `last_verified_at`, `source` | Lifecycle & provenance |

**Resolution algorithm** (`resolve(query, market_hint?) -> ResolutionResult`):
1. Exact `instrument_id` → return.
2. Exact `symbol` + explicit `exchange` → return.
3. Exact `symbol` without exchange: if exactly one active instrument matches → return it **and** echo `resolved_from` so the UI shows what was chosen; if several (e.g. an Indian listing and a US ADR sharing a ticker, NSE vs BSE, or a ticker that is also a different company elsewhere) → **HTTP 409 `AMBIGUOUS_SYMBOL` with `candidates[]`**; the UI forces a choice. No silent default.
4. Name/alias fuzzy search (token-based, normalised) → ranked candidates; never auto-select below a confidence threshold.
5. Unknown → `404 INSTRUMENT_NOT_FOUND` (this is **our** 404, distinct from a provider 404).
6. A resolved instrument is probed once against the provider (cheap history call); failure → `PROVIDER_SYMBOL_UNSUPPORTED` with negative-cache (TTL configurable, default hours) so repeated UI calls do not hammer a provider that returns Yahoo-style 404s.
The master is seeded from freely/legally downloadable exchange lists **[VERIFY terms]**, versioned, and shipped with `coverage.json`. Documentation and UI must show "N instruments supported (as of date)" – never "all stocks".

### 3.2 Provider interface (extends baseline `MarketDataProvider`)
```
capabilities(instrument) -> {
  intervals: { "1m": {max_lookback_days, max_bars_per_request, native: true}, ... },
  supports_adjusted: bool, has_volume: bool,
  data_class: "REALTIME"|"DELAYED"|"EOD",  declared_delay_minutes?: int|null,
  rate_limit: {rpm, burst}, terms_url
}
get_ohlcv(instrument, interval, start, end, adjust, deadline) -> OHLCVResult
get_quote(instrument, deadline) -> Quote           # optional; may be unsupported
```
`OHLCVResult`: `candles[{ts_open_utc, ts_close_utc, o,h,l,c,v, is_complete}]`, `series_id` (hash of instrument+interval+adjust+provider+first/last ts), `provider`, `fetched_at`, `data_class`, `adjust`, `warnings[]`. **A series always comes from exactly one provider** – never splice candles from two providers (adjustment/price-basis discontinuities); if fallback is used the whole series is re-fetched and the response flags `fallback_used=true, provider=…`.

### 3.3 Data-class labelling (UI and API) **[REQUIRED]**

| Label | When allowed |
|---|---|
| `LIVE` | Only with a licensed/contractually real-time feed **and** last-tick age below a threshold. Not assumed for unofficial sources. |
| `DELAYED` | Provider declares a delay, or measured latency (now − last bar close) exceeds expected bar latency. Show "Delayed" (+ minutes if known). |
| `DELAYED_UNVERIFIED` | Default for unofficial free sources (latency not guaranteed). |
| `HISTORICAL` | Completed bars only. |
| `CACHED` | Served from our cache; always show original `fetched_at` and age. A cached item can never be labelled `LIVE`. |
| `UNAVAILABLE` | No data; show reason code. |
The latest forming candle is flagged `is_complete=false` and rendered visually distinct; indicators/patterns/forecasts treat it as **provisional** (see §6.1, §7).

### 3.4 Error taxonomy and unified error schema **[REQUIRED]**
```json
{ "error": { "code": "UNSUPPORTED_INTERVAL_RANGE", "message": "…human readable, actionable…",
  "http_status": 422, "retryable": false, "request_id": "…",
  "details": { "interval": "1m", "requested_days": 90, "max_days": 7, "suggested": ["5m"] },
  "provider": "…", "occurred_at": "…UTC" } }
```
| Code | HTTP | Retry? | Trigger |
|---|---|---|---|
| `INSTRUMENT_NOT_FOUND` | 404 | no | not in master |
| `AMBIGUOUS_SYMBOL` | 409 | no | several matches |
| `PROVIDER_SYMBOL_UNSUPPORTED` | 404/502 | no (negative-cached) | provider 404 for mapped symbol |
| `NO_DATA` | 200/204 + `status:"unavailable"` + `reason` ∈ {holiday, weekend, outside_history, delisted, provider_empty} | no | empty provider response |
| `UNSUPPORTED_INTERVAL` / `UNSUPPORTED_INTERVAL_RANGE` | 422 | no | capability check |
| `INVALID_DATE_RANGE` | 422 | no | start ≥ end, future dates, over-span |
| `PROVIDER_RATE_LIMITED` | 429 | bounded, honour `Retry-After` up to cap | provider 429 / our limiter |
| `PROVIDER_TIMEOUT` / `PROVIDER_UNAVAILABLE` | 504/503 | bounded | timeouts, 5xx |
| `PROVIDER_SCHEMA_CHANGED` | 502 | no | unexpected payload (alert!) |
| `DATA_QUALITY_FAILED` | 200 with warnings or 422 | no | validation failure beyond tolerance |
| `LLM_NOT_CONFIGURED` / `LLM_MODEL_INVALID` | 503 | no (permanent) | see §3.7 |
| `LLM_QUOTA_EXHAUSTED` / `LLM_UNAVAILABLE` / `LLM_OUTPUT_INVALID` | 429/503/502 | per §3.7 | |
No endpoint may leak stack traces, provider keys or raw provider bodies.

### 3.5 Timeouts, retries, cancellation, concurrency
- Per-call timeout (default connect 3 s, read 10 s; configurable) plus a **request-level deadline** propagated through all calls.
- Retries only for transient classes (timeouts, 5xx, 429 with bounded wait): max 2 retries, exponential backoff with full jitter (base 0.5 s, cap 8 s). **Never** retry 4xx other than 429. Never infinite.
- Per-provider token bucket from verified limits; circuit breaker (baseline §3.4).
- **Single-flight** de-duplication for identical in-flight requests; stale-while-revalidate allowed only for HISTORICAL data.
- Cancellation: FastAPI request cancellation honoured (client disconnect aborts provider call where possible); frontend uses `AbortController` and a monotonically increasing `requestSeq` so a late response can never overwrite a newer selection.
- Fallbacks: only providers present in validated config (`MARKET_DATA_PROVIDERS` ordered list). Startup fails fast (or marks the provider `disabled` in `/health`) if a listed provider lacks required credentials. If none can serve → `NO_DATA`/`PROVIDER_UNAVAILABLE`, never sample data.

### 3.6 Data validation (extends baseline §2.2.2)
Monotonic unique timestamps; `low ≤ min(o,c) ≤ max(o,c) ≤ high`; non-negative volume; session-boundary consistency (candles outside exchange session hours flagged); duplicate/overlap detection; stale last bar relative to the calendar; price jump vs split heuristic (flag, don't delete); zero-volume streaks on liquid names; **partial-bucket detection**. Output `DataQualityReport{score, issues[]}` stored in response metadata and used in confidence (baseline §39).

### 3.7 LLM-provider resilience (Gemini 503 / model-configuration failures) **[REQUIRED]**

| Provider response | Class | Behaviour |
|---|---|---|
| 503 / "overloaded" / 500 / timeout | transient | ≤2 bounded retries (jitter) → secondary configured provider → deterministic fallback; circuit breaker opens after N failures |
| 429 / quota exhausted | quota | Do not hammer. Honour `Retry-After` only if ≤ cap; mark provider *cooling*; use fallback; surface `LLM_QUOTA_EXHAUSTED` if none left |
| 404 "model not found", 400 invalid model/param, unsupported modality (e.g. image to text-only model) | **permanent configuration** | Fail fast, no retries. Detected at **startup** by a capability probe (list-models or 1-token dry-run) and at call time. `/api/ai/health` reports `llm.status="misconfigured"` with actionable text (which env var, how to list valid models). |
| 401 / 403 | permanent auth | Fail fast; never log key; mark provider disabled |
| Safety block / empty candidates | content | Return `LLM_OUTPUT_INVALID` with reason; do not retry identical prompt more than once |
| Malformed JSON | output | Repair-retry ≤2 (baseline §11.3) then safe fallback |
Model names are **configuration, validated against the provider integration actually used** (the SDK/REST version in `requirements`), never hard-coded in code paths. Only providers that are configured *and* healthy participate in fallback. When nothing is available the API returns a structured partial result: deterministic sections `ok`, LLM sections `unavailable` with the error code (see §10.4).

### 3.8 Production sample-data ban
CI gate: `grep`/import-linter rule forbids production modules from importing `tests/`, `fixtures/`, `demo/`; every fixture file must contain `"synthetic": true`. Demo mode (if retained) must be an explicit env flag, off by default, and the UI must show a persistent "DEMO DATA" banner.

---

## 4. Range, Interval and Session Model

### 4.1 Range presets **[REQUIRED]**
Ranges are **resolved server-side into an exchange-local `[start, end]` window and fetched**. A button press must cause a new request (or a cache hit on an identical resolved window); acceptance test asserts the network call and the changed first/last candle timestamps.

| Range | Resolution (exchange-local, via trading calendar) | Default interval | Typical allowed intervals (subject to capability) |
|---|---|---|---|
| 1D | Current session if open or just closed; else last completed session (not "last 24h") | 5m | 1m, 3m, 5m, 10m, 15m, 30m, 1h |
| 5D | Last 5 trading sessions | 15m | 1m*, 5m, 10m, 15m, 30m, 1h, 4h |
| 1M | 1 calendar month back from `end`, snapped to first session ≥ start | 1D | 5m*, 15m*, 30m, 1h, 4h, 1D |
| 3M | 3 calendar months | 1D | 30m*, 1h, 4h, 1D, 1W |
| 6M | 6 calendar months | 1D | 1h, 4h, 1D, 1W |
| YTD | 1 Jan of exchange-local year → today (first session ≥ 1 Jan) | 1D | 1h*, 4h*, 1D, 1W |
| 1Y | 12 calendar months | 1D | 1D, 1W, 1M (1h/4h if provider history permits) |
| 3Y | 36 months | 1W | 1D, 1W, 1M |
| 5Y | 60 months | 1W | 1D, 1W, 1M |
| MAX | Earliest available bar for that instrument/provider | 1M | 1D, 1W, 1M |
| CUSTOM | User start/end (date or datetime for intraday) | auto | per validation |
`*` = only if the provider's intraday lookback covers it (see §4.7). UI disables unsupported combinations with an explanatory tooltip; the API returns `422 UNSUPPORTED_INTERVAL_RANGE` with `suggested` alternatives. **The app never silently changes the user's choice**; if it must (e.g. persisted preference now invalid), it shows a notice.
Bars budget: estimated bars = sessions × bars_per_session(interval); responses are capped (default 5,000 bars/request, configurable) – larger windows are served via backward pagination (§4.4), not truncated silently; any truncation sets `truncated=true, truncation_reason`.

### 4.2 Custom ranges, holidays, weekends, missing sessions
- Validation: `start < end`; `end ≤ now`; dates parsed in the **exchange timezone** unless a UTC offset is supplied; maximum span per interval from capabilities; intraday custom ranges require datetime or snap to session open/close.
- Window is **snapped** to trading sessions via the calendar; response contains `requested_start/end`, `effective_start/end`, `snapped=true|false`, `sessions_in_window`, `sessions_with_data`.
- Holidays/weekends: trading calendars per exchange (NSE special cases: Muhurat session, occasional Saturday special sessions, early closes; US half-days) **[VERIFY coverage of calendar library for NSE; otherwise maintain a reviewed holiday table]**. If the calendar is unavailable, infer sessions from data presence but **never fabricate candles** and flag `calendar_source:"inferred"`.
- Missing sessions (provider gaps): reported in `gaps[]` (session date, expected vs received bars). Charts show a subtle gap marker; indicators computed over the data present with a warning if gaps exceed threshold.
- X-axis: trading-time (category) axis for equities so weekends/overnight gaps do not leave blank space; intraday shows session separators; commodities with ~23h sessions use their own calendar.

### 4.3 Previous / next / latest
`‹ ›` shift the window by its own length (or by a user-chosen step) and issue a new request; disabled when `effective_start == earliest_available` (prev) or at the present (next). **Latest** resets `end=now`, re-enables live refresh. Live refresh (polling interval from capabilities, never below provider rate limit) updates only the last bar via `updateLastBar`; paused when tab hidden.

### 4.4 Backward pagination while panning
Request parameter `before=<ts_open_utc of oldest loaded bar>` + `limit`. Frontend triggers when the visible logical range's left edge is within ~50 bars of the oldest loaded bar; merges and de-duplicates by `ts_open_utc`; enforces a memory cap (e.g. keep ≤ 20,000 bars; evict far-right history only if user is not viewing latest). Indicators for newly loaded history are recomputed with warm-up padding (§6.1).

### 4.5 Aggregation rules (derived intervals) **[REQUIRED]**
Allowed derivations (source → target): 1m→{3m,5m,10m,15m,30m,1h,4h}; 5m→{10m,15m,30m,1h,4h}; 15m→{30m,1h,4h}; 1h→{4h}; 1D→{1W,1M}. Prefer **native provider bars**; derive only if native unsupported. Rules:
1. **Bucket by session, never across sessions**: `bucket = floor((ts_open − session_open) / interval)` within a `session_date`. Overnight/weekend gaps never merge into one candle.
2. **Anchoring**: buckets anchor at the exchange session open (NSE 09:15 IST; NYSE/Nasdaq 09:30 ET) in exchange-local time. Example NSE 1h: 09:15–10:15 … 14:15–15:15, then a **partial 15:15–15:30** bucket (flagged `is_partial=true`). NSE 4h: 09:15–13:15 and **13:15–15:30 (partial, 2h15m)**. NYSE 4h: 09:30–13:30, 13:30–16:00 (partial). Partial buckets are labelled, not padded. Pre/post-market bars excluded unless explicitly requested.
3. OHLCV: `open=first.open, high=max(high), low=min(low), close=last.close, volume=sum(volume)`; `ts_open = bucket start`, `ts_close = bucket end or last constituent close`.
4. **Missing constituents**: do not interpolate or invent. Bucket gets `constituents_expected`, `constituents_received`; if received/expected < threshold (default 0.8) → `low_integrity=true` and indicator/pattern engines may skip it.
5. Weekly/Monthly: group by exchange-local ISO week / calendar month over **trading days only**; `open` = first session's open, `close` = last session's close; a week/month in progress is `is_complete=false`. Timestamp = first trading session of the period.
6. Daily candles derived from intraday must respect session hours (exclude pre/post) so they match official daily bars within tolerance; a reconciliation test compares derived daily vs native daily (tolerance on OHLC; volume may differ by auction/closing sessions).
7. Provider quirks: some feeds timestamp bars at *close* instead of *open*; the provider adapter normalises and a test proves it with fixtures. 
8. Heikin-Ashi is a *rendering transform*, never an aggregation (§5.2).

### 4.6 Time zones and timestamps
Store/transport UTC ISO-8601 (`Z`); every instrument response includes `timezone`; the UI renders in the **exchange timezone** with a visible tz label (IST/ET); optional "device timezone" toggle. DST (US) handled by the tz database, tested around DST change weekends.

### 4.7 Intraday history limits and when another provider is needed
Free unofficial sources commonly restrict intraday history (reported limits for Yahoo-based wrappers: 1m ≈ 7-day windows within ~30 days; 2m–30m ≈ 60 days; 60m ≈ 730 days — **[VERIFY at implementation and encode in `capabilities()`, don't hard-code]**). Consequences: "3Y at 5m" cannot be served from such a source. Options, in order:
1. **Disable** unsupported combinations with explanation (default, [REQUIRED]).
2. **Self-archive** [PLANNED]: a scheduled job stores completed 1m/5m bars per tracked instrument into the project's own store from deployment day onward (only if provider ToS permits storage **[VERIFY]**). History then grows over time; series tagged `source=self_archive` with continuity checks and gap reports. This is the realistic zero-budget path to deeper intraday history.
3. **Licensed/vendor feed** [OPTIONAL]: a paid vendor or exchange feed. A broker's *market-data-only* historical API using the **user's own credentials** may be supported as an optional provider adapter **[VERIFY terms]**; the adapter must expose only whitelisted read-only market-data calls—**no order, funds or portfolio endpoints may be imported or callable** (enforced by an allow-list test).
Without option 2 or 3, deep intraday backtests (Phase 13) are limited to the available lookback and must say so.

### 4.8 Price adjustment
`adjust ∈ {none, splits, splits_dividends}` returned in metadata and shown in the chart legend ("Adj: splits"). Chart, indicators, patterns and levels are all computed on the **same adjusted series** for display. ML point-in-time rules from baseline §7.3 (revised data) still govern training features; a mismatch between display adjustment and model feature basis is documented in the forecast metadata.

---

## 5. Charting Workspace

### 5.1 Chart-engine decision (Phase 5 begins with a time-boxed spike) **[REQUIRED]**
Use the library already in the project **only if** it satisfies the must-haves below; otherwise run the evaluation and record an ADR (`docs/adr/0001-chart-engine.md`) with migration risks.

Must-haves: candlestick + OHLC + line + area; histogram volume; ≥3 synchronized panes; zoom/pan/crosshair; programmatic visible-range control & events; `updateLastBar`; handles ≥5,000 bars smoothly; dark theme; touch gestures; accessible fallback possible; compatible licence for a public project.

| Candidate | Notes **[VERIFY licence, version, size, maintenance at spike time]** |
|---|---|
| TradingView *Lightweight Charts* | Small bundle, canvas, candlesticks/OHLC/line/area/histogram, crosshair/range events; **no built-in drawing tools or indicator library** (build overlays/panes in-house; recent versions advertise multi-pane support). Open-source licence with an attribution requirement. Likely best performance/size trade-off. |
| *KLineChart* | Built-in overlays/drawing tools and indicators; canvas; open-source licence; verify docs quality, TypeScript typings, a11y, maintenance cadence. |
| Apache *ECharts* | Candlestick + dataZoom + multiple grids; large bundle; drawing tools must be custom; good flexibility. |
| *Recharts* / SVG libs | Not suitable for thousands of OHLC bars (SVG performance, no native candlestick) – acceptable only for small sparklines. |
| *TradingView Advanced Charts / Charting Library* | Feature-rich but proprietary, access by application/licence; **not assumed available**; do not embed without a granted licence. |
| Commercial stock-chart suites | Licence cost → conflicts with zero-budget constraint. |
Decision matrix (weights set in the ADR): features 30%, performance 20%, licence 15%, bundle size 10%, accessibility/mobile 10%, maintenance 10%, integration effort 5%. Spike task: render 5,000 candles + volume + 3 indicators; record FPS during pan/zoom (Chrome performance trace), gzip bundle delta, memory, mobile Safari/Chrome behaviour.
Isolation: all chart code sits behind a `ChartEngine` adapter interface (`setSeries`, `updateLastBar`, `setChartType`, `addOverlay/removeOverlay`, `addPane/removePane`, `setVisibleRange`, `onVisibleRangeChange`, `onCrosshairMove`, `drawingsApi`, `destroy`). The old Market Overview chart stays behind feature flag `chart_workspace_v2` until Phase 14 acceptance (rollback = flag off). Migration risks to list: bundle growth, loss of existing tooltips/styles, SSR/hydration, test-selector churn, mobile gestures, licence notices.

### 5.2 Chart types **[REQUIRED]**
| Type | Data | Notes |
|---|---|---|
| Line | close | Option: step line; gaps not bridged across sessions on intraday |
| Area | close | Baseline = axis min or previous close (configurable) |
| OHLC bars | O,H,L,C | Tick marks left=open, right=close |
| Candlestick | O,H,L,C | **Actual** OHLC; up/down colours plus shape/fill difference (not colour only); hollow-vs-filled option |
| Heikin-Ashi | derived | Formulas below; labelled "Heikin-Ashi (transformed)" |
Heikin-Ashi (computed over the full loaded series, in order):
```
HA_close[t] = (O[t] + H[t] + L[t] + C[t]) / 4
HA_open[0]  = (O[0] + C[0]) / 2
HA_open[t]  = (HA_open[t-1] + HA_close[t-1]) / 2
HA_high[t]  = max(H[t], HA_open[t], HA_close[t])
HA_low[t]   = min(L[t], HA_open[t], HA_close[t])
```
HA is path-dependent (seed at first loaded bar), so values may differ slightly if more history is loaded: show a tooltip note and keep the tooltip's OHLC fields as the **real** candle values. Indicators, patterns, levels and forecasts are computed on **real** OHLC. Volume panel colour = direction of the real candle (close vs open; option: vs prior close). Price scale: linear / log / percent. Legend and tooltip show O, H, L, C, change, %change, volume, and the value of each visible indicator at the crosshair.

### 5.3 State handling in the chart area
`loading` (skeleton + aria-busy), `empty` (reason code from §3.4 with plain text and suggested action), `error` (code, message, **Retry** button, request id), `stale` (banner with age), `partial` (some panes/indicators unavailable), `unsupported_selection` (explains and offers valid alternatives). None may throw to the React error boundary; every async path has a tested failure state.

### 5.4 Indicator selector UX **[REQUIRED]**
- Menu with search/categories (Trend, Momentum, Volatility, Volume, Intraday levels); each added instance gets a legend row: colour swatch, name+params, ⌖ visibility toggle, ⚙ parameters dialog (validated against ranges in §6), ✕ remove.
- Multiple instances allowed (e.g. EMA 9 and EMA 21). Readability guards: max overlays (default 6), max oscillator panes (default 3); exceeding → inline message, not silent failure. Pane resize/collapse/reorder.
- Overlays on price pane; oscillators in own panes; volume pane default on when `has_volume`.
- Persistence: per-user template (`equinexa:indicators:v1`) in localStorage (try/catch, schema-versioned, size-capped) or server profile if auth exists (Q3). Instruments without volume auto-disable volume-based indicators with an inline reason.
- Calculation source of truth: **backend** (§6) returns arrays aligned to the displayed candles (same `series_id`). The frontend may compute trivial indicators locally only if parity tests against the backend fixtures exist.

### 5.5 Drawing and interaction tools **[REQUIRED / local persistence PLANNED]**
Tools: crosshair (default), horizontal line, vertical line, trend line, ray [OPTIONAL], rectangle/zone (support/resistance band), text note, measure (Δprice, Δ%, bars, time), clear all (with confirm + undo), delete selected, lock.
Data model (stored in **time/price coordinates, never pixels**):
```json
{ "id":"uuid", "schema_version":1, "type":"trend_line|hline|vline|zone|text|measure",
  "instrument_id":"…", "interval_scope":"this|all", "points":[{"ts_utc":"…","price":0.0}],
  "style":{"color":"#…","width":1,"dash":"solid|dashed"}, "text":"…≤200 chars", "locked":false,
  "created_at":"…","updated_at":"…" }
```
Scoping: key = `(instrument_id)` plus `interval_scope`. Horizontal lines/zones default `all` intervals (price-based); trend lines and text default `this` interval (time-anchored; mapped to nearest candle on that interval); vertical lines default `all`. Not range-scoped (a drawing exists on the timeline; it is simply off-screen outside the window). Log-scale aware rendering. Text is rendered as plain text (no HTML). Persistence: localStorage with versioning, 500-drawing cap per instrument, quota/exception handling, corrupted-JSON recovery; server-side storage only if auth and user-data architecture already exist and per-user isolation is tested. Undo/redo stack (≥20 steps). **Auto-detected levels** from the engine (§7) are a separate, toggleable layer labelled "Computed" and are never mixed into the user's drawings.
No order-ticket, buy/sell buttons, P&L-from-broker, or account views anywhere.

### 5.6 Layout, responsiveness and accessibility
Desktop (≥1024px): top bar (symbol search, name, exchange, currency, data-class badge, last update, session state) → toolbar (range | interval | chart type | indicators | compare [OPT] | settings) → left vertical drawing toolbar → chart stack (price, volume, oscillators) → right tabbed panel (AI Analysis | Research | Levels & Plan | Watchlist) → status bar (timezone, provider, cache/freshness). Tablet (768–1023px): right panel collapses into a drawer. Mobile (<768px): chart-first; toolbar collapses into bottom-sheet pickers; drawing tools in a floating collapsible palette; touch pinch/drag; landscape supported; ≥44×44 px targets.
Accessibility (WCAG 2.1 AA target): semantic buttons with `aria-pressed`/`aria-expanded`; roving tabindex in toolbars; `aria-live="polite"` region announcing range/interval changes, loading and errors; keyboard: `/` focus search, `←/→` pan, `+/−` zoom, `Home` jump to oldest loaded, `End` jump to latest, `Esc` cancel drawing, `Del` delete selected drawing; visible focus ring; contrast ≥ 4.5:1 for text; up/down not conveyed by colour alone; `prefers-reduced-motion` respected; **"View as table"** alternative for the visible candles; textual summary of the last candle for screen readers. Keep EquiNexa branding, dark theme tokens and existing navigation.

### 5.7 Performance budgets (finalised after the spike)
Targets: first chart paint ≤ 1.5 s on a mid-range laptop for ≤1,500 bars (cache-warm backend); pan/zoom ≥ 50 fps at ≤5,000 bars; range/interval switch perceived response ≤ 1 s from cache or ≤ 3 s from provider (skeleton shown immediately); debounce rapid button presses; cancel in-flight requests; bundle delta recorded in ADR with a budget.

### 5.8 Watchlist and compare
Watchlist (local-first, server if auth exists): add/remove, reorder, last price + change + data-class badge, click to load chart; max size (e.g. 50) with polling budget respecting provider limits (batch quotes or round-robin refresh). Compare overlay (percent-normalised second symbol) is [OPTIONAL].

---

## 6. Technical Indicator Framework (Charting + Intraday Levels)

Extends baseline §8 (ML feature engine). The **same Python implementations** serve charting, pattern context, analysis and ML features, so a number on the chart equals the number the model sees (apart from documented scaling).

### 6.1 Indicator contract **[REQUIRED]**
- **Input:** exactly the candle series displayed (`series_id` echoed back); real OHLCV, same adjustment, same interval. Never recomputed from a different fetch.
- **Output:** arrays aligned 1:1 to candles; `null` for warm-up; `meta{name, params, warmup_bars, version, panel:"overlay|pane:<id>", scale:{min,max}?}`.
- **No look-ahead:** value at bar *t* depends only on bars ≤ *t* (trailing windows only). Truncation-invariance test (baseline §7.5 #1) runs for every indicator and every parameter set in the test grid.
- **Provisional bar:** if the last candle is incomplete, its indicator values are returned with `provisional=true`; pattern/forecast engines ignore incomplete bars.
- **Warm-up padding:** the API accepts `warmup_bars="auto"`; the server fetches the extra history needed (max indicator warm-up × safety factor, ≥ 3× for recursive indicators like EMA/Wilder/Supertrend/ADX) *before* the visible window, computes on the padded series, then trims. If padding history is unavailable, early values are `null` and `warnings:["insufficient_history"]` — never fabricated.
- **Missing/low-integrity bars:** gaps flagged (§4.5); indicators compute over available bars and return `warnings`.
- **Volume dependence:** volume-based indicators return `unavailable(reason:"instrument_has_no_volume")` for indices.
- Deterministic, versioned (`indicator_version`), independently tested against a reference (hand-computed fixtures and, where practical, a second library) with documented tolerances (≈1e-8 relative for non-recursive; seeding conventions documented for recursive ones).

### 6.2 Catalogue

| Indicator | Defaults | Param ranges | Panel | Warm-up (null bars) | Definition / conventions |
|---|---|---|---|---|---|
| SMA | n=20 | 2–500 | overlay | n−1 | mean of last n closes |
| EMA | n=20 | 2–500 | overlay | n−1 (seed = SMA of first n) | α=2/(n+1); document seed; test vs reference |
| RSI | n=14 | 2–100 | pane 0–100 (30/70 guides) | n | Wilder smoothing, seed = simple mean of first n gains/losses; `avg_loss=0 ⇒ 100`; both zero ⇒ 50 |
| MACD | 12/26/9 | fast<slow; 2–200 | pane | slow+signal−2 | line=EMA(f)−EMA(s); signal=EMA(line,sig); histogram=line−signal |
| Bollinger Bands | n=20, k=2 | n 2–200, k 0.5–5 | overlay | n−1 | mid=SMA; bands=mid±k·σ with **population** σ (ddof=0) (documented); optional %B, bandwidth |
| VWAP (session) | anchor=session | — | overlay | 0 | `VWAP_t = Σ(TP·V)/ΣV` since session open; `TP=(H+L+C)/3`; **resets each session**; intraday intervals only; ΣV=0 ⇒ `null`; optional ±1/2σ volume-weighted bands [OPT] |
| Anchored VWAP | user date/bar | — | overlay | 0 | same formula from chosen anchor; works on daily too |
| Rolling VWAP | n=20 | 2–500 | overlay | n−1 | for daily+ intervals where session VWAP is undefined |
| ATR | n=14 | 1–100 | pane (or value in legend) | n | `TR=max(H−L,|H−C₋₁|,|L−C₋₁|)`, first TR=H−L; Wilder smoothing |
| Stochastic | 14/3/3 | 1–100 each | pane 0–100 (20/80) | k+d+smooth−2 | `%K=100·(C−LL)/(HH−LL)` (HH=LL ⇒ 50), slow smoothing, `%D=SMA(%K,d)` |
| ADX (+DI/−DI) | n=14 | 2–100 | pane | ≈2n−1 | Wilder-smoothed DM/TR; `DX=100|+DI−−DI|/(+DI++DI)`; ADX = Wilder-smoothed DX |
| Supertrend | ATR=10, mult=3 | 2–50, 0.5–10 | overlay | ATR n | basic bands `hl2±mult·ATR`; final-band carry rules; direction flips when close crosses the active band. **Path-dependent** → warm-up padding mandatory. Acceptance: matches an independent implementation on ≥3 fixtures; if it cannot be verified, the indicator stays hidden (the brief says "if implemented correctly") |
| Volume + Volume MA | MA n=20 | 2–200 | pane (histogram + line) | n−1 (MA) | MA of volume |
| OBV | — | — | pane | 0 | cumulative signed volume [OPT in UI; required for ML per baseline §8] |

### 6.3 Intraday level tools (new, for traders) **[REQUIRED unless marked]**
All are deterministic functions of **completed** data at the evaluation time.

| Tool | Definition | Look-ahead rule |
|---|---|---|
| Previous-day H/L/C and gap % | From the previous completed session; `gap% = (open_today − close_prev)/close_prev` | Gap known only after today's first trade/open price |
| Day high/low so far, VWAP distance | Running; `dist_vwap_atr = (close − VWAP)/ATR_n` | Running values only |
| Opening Range (ORB) N=5/15/30 min | `OR_high/low` = extremes of the first N minutes after session open | **Levels exist only after the N-minute window completes**; before that, show "developing" in a different style and never use them in signals |
| Classic pivots | `P=(H+L+C)/3`, `R1=2P−L`, `S1=2P−H`, `R2=P+(H−L)`, `S2=P−(H−L)`, `R3=H+2(P−L)`, `S3=L−2(H−P)` using previous session H,L,C | Previous session only |
| Fibonacci pivots | `R1=P+0.382·range`, `R2=P+0.618·range`, `R3=P+range` (mirror for S) | idem |
| Camarilla | `R1=C+range·1.1/12`, `R2=C+range·1.1/6`, `R3=C+range·1.1/4`, `R4=C+range·1.1/2` (mirror for S) [OPT] | idem |
| CPR (central pivot range) | `P`, `BC=(H+L)/2`, `TC=2P−BC` (TC/BC ordered); width% = |TC−BC|/P classified narrow/normal/wide vs trailing-N-day distribution | Previous session only |
| Relative volume by time-of-day (RVOL-ToD) | `cum_vol(today, minute m) / mean_{k=1..N} cum_vol(day−k, minute m)` (N default 20, same session minute) | Needs ≥N prior sessions at the same interval; else `null` |
| Round-number / swing levels | From pivots (§7) clustered with ATR tolerance | Confirmed pivots only |
| Day-type features | Opening drive %, range-expansion vs ATR, VWAP-cross count, trend-efficiency (|ΔP|/Σ|ΔP|) | Running values |
Pivot/CPR variants differ across platforms (some use different day definitions or include the open); the implementation documents its convention in the legend tooltip so users are not misled when comparing with other apps.

### 6.4 Tests
Golden fixtures per indicator (short hand-computed series incl. edge cases: constant price, zero volume, single bar, NaN gap, very long series); property tests (scale invariance of ratio indicators; EMA monotone response); truncation-invariance; parameter-grid smoke; cross-library parity (documented tolerances); VWAP session-reset test spanning two days; ORB level-availability test; API alignment test (`len(values)==len(candles)`); frontend rendering test that each indicator toggles pane/overlay and updates on interval change.

---

## 7. Pattern Engines (Candlestick and Chart)

Baseline §15–16 define catalogues and output records. This section tightens them into **mathematically testable** definitions, adds missing patterns, and defines honest reporting. Pattern detection runs on **real candles**, completed bars only, with data ≤ prediction timestamp.

### 7.1 Audit step (Phase 1/7)
Enumerate patterns the existing code *actually detects* (function names + unit tests), compare with the table below, and record `IMPLEMENTED_VERIFIED / PARTIAL / MISSING / UNSUPPORTED_CLAIM` (e.g. a pattern named only in a prompt = unsupported claim).

### 7.2 Shared definitions (parameters in `configs/patterns/candlestick.yaml`)
```
ATR  = ATR_14 at bar t-1 for 1-candle patterns evaluated at t (no future use)
body = |C−O|; range = H−L; upper = H−max(O,C); lower = min(O,C)−L
long_body   : body ≥ 0.60·ATR            small_body : body ≤ 0.30·ATR
doji        : body ≤ 0.10·range  AND  range ≥ 0.25·ATR            (ignore micro-ranges)
eps = 0.05·ATR (comparison tolerance)
trend_ctx(t,N=5,k=1.0): UP if C[t−1]−C[t−1−N] ≥ k·ATR ; DOWN if ≤ −k·ATR ; else SIDEWAYS
```
Insufficient history (ATR undefined) ⇒ no detection and `status:"unavailable"` (not "no pattern"). Zero-range candles are ignored. For **intraday intervals**, multi-candle patterns may not span a session boundary unless the user enables it (`crosses_session=true` flagged); on daily they span days normally. Incomplete (forming) bar ⇒ pattern emitted as `provisional`.

### 7.3 Candlestick catalogue (baseline 13 + additions)

| Pattern | Candles | Formal rule (bullish/bearish as named) | Required context | Confirmation | Invalidation |
|---|---|---|---|---|---|
| Doji | 1 | doji rule | meaningful only if trend_ctx ≠ SIDEWAYS (else tagged "neutral/indecision") | next close beyond doji H/L | — |
| Hammer | 1 | `lower ≥ 2·body`, `upper ≤ 0.25·body or ≤ eps`, body in upper third of range, range ≥ 0.5·ATR | trend_ctx = DOWN | next close > hammer high | close < hammer low |
| **Hanging Man** *(new)* | 1 | same shape as Hammer | trend_ctx = UP | next close < hammer-shape body low | close > its high |
| Inverted Hammer | 1 | `upper ≥ 2·body`, `lower ≤ eps…`, body in lower third | DOWN | next close > its high | close < low |
| Shooting Star | 1 | same shape | UP | next close < its body low | close > high |
| Marubozu | 1 | `body/range ≥ 0.90`, `range ≥ 0.8·ATR` | any | — | — |
| Bullish Engulfing | 2 | bar₁ bearish, bar₂ bullish, `O₂ ≤ C₁+eps`, `C₂ ≥ O₁−eps`, `body₂ > body₁` | DOWN | next close > bar₂ high | close < bar₂ low |
| Bearish Engulfing | 2 | mirror | UP | next close < bar₂ low | close > bar₂ high |
| **Bullish Harami** *(new)* | 2 | bar₁ bearish & `long_body`; bar₂ bullish; body₂ ⊂ body₁: `max(O₂,C₂) ≤ max(O₁,C₁)` and `min(O₂,C₂) ≥ min(O₁,C₁)`; `body₂ ≤ 0.5·body₁` | DOWN | next close > bar₁ open | close < bar₁ low |
| **Bearish Harami** *(new)* | 2 | mirror | UP | next close < bar₁ open | close > bar₁ high |
| Harami Cross *(new, variant)* | 2 | Harami with bar₂ doji | as above | as above | as above |
| Piercing Line | 2 | bar₁ bearish long; bar₂ bullish, `O₂ < L₁` (gap-down open; relax to `O₂ < C₁` for 24h/gappy markets via config), `C₂ > midpoint(body₁)` and `C₂ < O₁` | DOWN | next close > bar₂ high | close < bar₂ low |
| Dark Cloud Cover | 2 | mirror: `O₂ > H₁`, `C₂ < midpoint(body₁)`, `C₂ > O₁` | UP | next close < bar₂ low | close > bar₂ high |
| Morning Star | 3 | bar₁ bearish long; bar₂ small body with `max(O₂,C₂) < C₁+eps` (gap optional via config); bar₃ bullish long with `C₃ > midpoint(body₁)` | DOWN | next close > bar₃ high | close < bar₂ low |
| Evening Star | 3 | mirror | UP | next close < bar₃ low | close > bar₂ high |
| Three White Soldiers | 3 | three bullish `long_body` bars; each opens within prior body (`O_k ≥ min(body_{k−1})`) and closes higher than prior close; each upper shadow ≤ 0.3·body | DOWN or SIDEWAYS (before) | — | close < bar₁ open |
| Three Black Crows | 3 | mirror | UP or SIDEWAYS | — | close > bar₁ open |
Output record = baseline §15.3 plus `parameters_hash`, `atr_used`, `trend_ctx`, `crosses_session`, `provisional`, `evidence_level` (below). Patterns are *evidence*; the UI wording is "Bullish Engulfing detected (context: prior decline). Awaiting confirmation: …".

### 7.4 Unit tests (per pattern) **[REQUIRED]**
≥3 positive fixtures, ≥3 near-miss negatives (each violating exactly one clause), 1 boundary (equality at tolerance), 1 insufficient-history, 1 zero-range, 1 session-boundary (intraday), scale invariance (multiply all prices by constant ⇒ same detections), **truncation invariance** (append future bars ⇒ earlier detections unchanged), `provisional` handling, and a null-data false-positive-rate check on seeded random walks (record observed rates per 1,000 bars in the model card; thresholds are set from observed rates after calibration, not asserted in advance).

### 7.5 Reporting weak and conflicting signals
- Each detection has `bias ∈ {bullish, bearish, neutral}`, `confidence ∈ [0,1]` (baseline §15.4 decomposition) and `evidence_level ∈ {none, weak, moderate}` from §7.8.
- `pattern_summary` aggregates the last K bars (default 5): net bias = Σ(sign·confidence·recency_weight); **conflict** flagged when bullish and bearish detections both have confidence ≥ 0.4 within K bars → text "Signal conflict detected: …".
- Detections with `confidence < 0.4` or `evidence_level="none"` are hidden by default behind "Show weak signals", always labelled "weak".
- Never describe a pattern as predicting a price; say "has historically been followed by … in N cases (CI …)" only when §7.8 supplies numbers, else "no historical evidence available for this instrument group."

### 7.6 Chart-pattern engine (deterministic; baseline §16 made testable)
Shared:
1. **Pivots:** zig-zag with reversal threshold `max(x·ATR, y%)` (defaults x=2.0, y=0.5%); a pivot is **confirmed** only when the reversal threshold is reached (`confirmed_at` recorded). Only pivots with `confirmed_at ≤ t` are visible to pattern logic (prevents the classic centered-pivot leak).
2. **Lines:** robust fit (Theil–Sen/RANSAC) through pivot highs/lows; slope normalised per bar by ATR; touches counted within `0.25·ATR` tolerance; R².
3. **Levels:** cluster pivots with `ε=0.5·ATR`; strength = touches × recency × volume.
4. **Minimum data:** ≥ 60 completed bars for any chart pattern; per-pattern minimum below; fewer ⇒ `unavailable(insufficient_history)`.

| Pattern | Minimum bars | Detection (summary) | Confirmation | Invalidation |
|---|---|---|---|---|
| Double Top / Bottom | 30 | Two pivot highs (lows) within `0.5–1.0·ATR`, separation ≥ 10 bars, trough/peak depth ≥ 1.5·ATR, prior trend | Close beyond neckline by ≥ 0.25·ATR | Close above/below second peak/trough by ≥ 0.25·ATR |
| Head & Shoulders / Inverse | 50 | Three pivots, head extreme, shoulders within 15% of each other (ATR-normalised), neckline from two troughs (peaks) | Close beyond neckline | Close beyond head |
| Triangles (asc/desc/sym) | 30 | ≥2 touches each line, converging (apex ahead), slope signs/flatness per type (|slope|≤0.05·ATR/bar = flat) | Close beyond a line ≥0.25·ATR after ≥ 2/3 of the way to apex | Close beyond opposite line; apex passed |
| Rising / Falling Wedge | 30 | Both lines same sign slope, converging | Close through lower (rising) / upper (falling) line | Close beyond opposite line by 0.5·ATR |
| Flag / Pennant | 20 | Pole: move ≥ 3·ATR within ≤ 10 bars; consolidation: ≤ 50% retrace, duration 5–20 bars; flag = parallel counter-trend channel, pennant = small converging triangle | Close beyond consolidation edge in pole direction | Retrace > 61.8% of pole |
| Channel (asc/desc/horizontal) | 30 | Two near-parallel lines (|slope diff| ≤ 0.02·ATR/bar), ≥ 3 total touches | — (state: position within channel) | Close outside by ≥ 0.5·ATR for 2 bars |
| Range breakout / breakdown | 25 | Close beyond prior N-bar high/low (Donchian, N=20, **excluding the current bar**) by ≥ 0.25·ATR; volume ≥ 1.5× 20-bar average when volume exists | Hold for M closes (default 2) | Close back inside range |
Statuses: `forming` (not eligible for signals), `completed`, `confirmed`, `invalidated`. Overlays are drawn on the chart in a distinct "Computed" style with labelled key points. Unit tests use synthetic series generated to contain each exact pattern (with noise ladders), random-walk null series (false-positive rate recorded), and truncation invariance. **An LLM never detects patterns.** The vision model may only *cross-check* (Phase 8).

### 7.7 Pattern confidence
`confidence = geometric_fit × context × volume × location` with each factor documented (baseline §15.4/16.4) and **then capped by evidence level** (below). Factors are never tuned on the evaluation window.

### 7.8 Empirical evidence per pattern **[REQUIRED for any claim of usefulness]**
For each pattern × instrument-group × interval, compute on the **training period only**: occurrences, forward return distribution at horizons (e.g. next 1/3/5 bars), hit-rate vs unconditional base rate, bootstrap CI, after-cost expectancy; apply multiple-testing control (Benjamini–Hochberg across the pattern family). `evidence_level`: `moderate` if CI excludes base rate after correction on both train and validation; `weak` if only one; `none` otherwise. Evidence tables are versioned artefacts (`experiments/results/pattern_evidence/`) and displayed in the pattern tooltip with sample size.

---

## 8. API Contracts

### 8.1 Principles
Inspect existing OpenAPI first (Phase 1). **Extend before adding.** Where an equivalent already exists, record the mapping in `docs/api/mapping.md` instead of creating a duplicate. Paths below use `/api/market/*` for data and `/api/ai/*` for AI (baseline §46 convention); adjust to the real prefix found in Phase 1. All responses include `request_id`; timestamps are UTC ISO-8601 with `Z` plus `timezone` where relevant; errors use §3.4's envelope; provider keys never leave the backend; pagination uses cursors; every endpoint has Pydantic models, OpenAPI examples, contract tests and regression snapshots.

### 8.2 Endpoint catalogue

| # | Method & path | Purpose | Cache | Rate limit (default, configurable) |
|---|---|---|---|---|
| E1 | `GET /api/market/instruments/search?q=&market=&type=&limit=` | Search/resolve instruments | 5 min | 60/min/IP |
| E2 | `GET /api/market/instruments/{instrument_id}` | Identity, calendar, session state, capabilities summary | 1 h | 120/min |
| E3 | `GET /api/market/capabilities?instrument_id=` | Supported intervals, ranges, max lookback, data class, has_volume | 1 h | 120/min |
| E4 | `GET /api/market/ohlcv` | Historical/latest candles (range or custom, interval, pagination) | per §3/§8.4 | 60/min |
| E5 | `POST /api/market/indicators` | Compute indicators on a referenced series | keyed by `series_id`+params | 60/min |
| E6 | `GET /api/market/levels?instrument_id=&date=` | Previous-day levels, pivots, CPR, ORB (when available), RVOL-ToD | until next bar | 60/min |
| E7 | `GET /api/market/session?market=` | Session state, next open/close, holiday info | 1 min | 120/min |
| E8 | `POST /api/ai/chart-analysis/data` | Data-driven chart analysis (selected instrument/interval/window) | 1–5 min | 20/min |
| E9 | `POST /api/ai/chart-analysis` (existing image route) | Screenshot analysis (unchanged contract) | image hash | 10/min |
| E10 | `POST /api/ai/forecast` (or extend `/api/ai/analyze`, `/prediction/{ticker}`) | Horizon-explicit forecast | until next bar | 20/min |
| E11 | `POST /api/ai/research` + `POST /api/ai/research/{session_id}/followup` | Research and follow-ups | per query hash (short TTL) | 10/min |
| E12 | `GET /api/market/index/overview?index_id=` | Index context: breadth, VIX, sector, global cues | 1–5 min | 30/min |
| E13 | `GET /api/fundamentals/{instrument_id}` | Fundamental snapshot + history + score | 12–24 h | 30/min |
| E14 | `POST /api/trader/scan` | Run a named scanner on a universe | 1–5 min | 10/min |
| E15 | `POST /api/trader/plan` | Scenario plan (levels, risk, costs) | none | 30/min |
| E16 | `POST /api/trader/risk/size` and `POST /api/trader/risk/costs` | Position sizing; cost estimate | none | 60/min |
| E17 | `/api/trader/journal` (CRUD), `/api/trader/paper/*` | Journal & paper trades (auth/local) | none | 60/min |
| E18 | `/api/trader/watchlists`, `/api/trader/alerts` (CRUD) | Watchlists, alerts | none | 60/min |
| E19 | `GET /api/trader/setups/{setup_id}/evidence` | Setup-lab results | daily | 30/min |
| E20 | `GET /api/ai/health`, `GET /api/market/coverage` | Provider/LLM/vector/model health; supported instrument counts | 30 s | 60/min |

### 8.3 E1 – Instrument search
Request: `q` (1–50 chars, `^[\w .&\-^=]+$`), optional `market ∈ {IN,US,COMMODITY}`, `limit ≤ 25`.
Response:
```json
{ "query":"infosys", "results":[
  {"instrument_id":"IN.XNSE.INFY","symbol":"INFY","name":"Infosys Ltd","exchange":"NSE","mic":"XNSE","currency":"INR","timezone":"Asia/Kolkata","type":"equity","match":"name","score":0.93},
  {"instrument_id":"US.XNYS.INFY","symbol":"INFY","name":"Infosys Ltd ADR","exchange":"NYSE","currency":"USD","type":"equity","match":"symbol","score":0.90}],
  "ambiguous": true }
```
Errors: `422` invalid query; empty results ⇒ `200` with `results:[]` (not an error).

### 8.4 E4 – OHLCV
Request params: `instrument_id` (required), `interval` ∈ {1m,3m,5m,10m,15m,30m,1h,4h,1D,1W,1M}, **either** `range` ∈ {1D,5D,1M,3M,6M,YTD,1Y,3Y,5Y,MAX} **or** `start`+`end`, optional `before` (cursor ts), `limit` (≤5000), `adjust ∈ {none,splits,splits_dividends}`, `include_partial` (default true).
Validation: mutually exclusive range/start-end; capability check; `INVALID_DATE_RANGE`; `UNSUPPORTED_INTERVAL_RANGE`.
Response:
```json
{ "instrument": {"instrument_id":"…","symbol":"…","exchange":"…","currency":"INR","timezone":"Asia/Kolkata","has_volume":true},
  "interval":"15m", "range":"5D",
  "window": {"requested_start":null,"requested_end":null,"effective_start":"2026-09-28T03:45:00Z","effective_end":"2026-10-02T10:00:00Z","snapped":true,"truncated":false,"truncation_reason":null,"sessions_in_window":5,"sessions_with_data":5},
  "candles":[{"t":"2026-09-28T03:45:00Z","tc":"2026-09-28T04:00:00Z","o":0.0,"h":0.0,"l":0.0,"c":0.0,"v":0,"complete":true,"partial_bucket":false}],
  "gaps":[], "next_before":"…", "series_id":"sha256:…",
  "meta": {"provider":"…","fallback_used":false,"data_class":"DELAYED_UNVERIFIED","declared_delay_minutes":null,"fetched_at":"…","cache":{"hit":true,"age_s":42},"adjust":"splits","calendar_source":"exchange","quality":{"score":0.98,"issues":[]}},
  "status":"ok", "warnings":[] }
```
(Placeholder numbers above are schema illustrations, not data.) Empty data ⇒ `status:"unavailable"`, `reason`, `candles:[]`.
Caching: historical completed windows long TTL (immutable); windows touching "now" short TTL (≤ bar duration, floor 15 s); key includes `adjust`, `provider`; `Cache-Control` and ETag.

### 8.5 E5 – Indicators
```json
{ "series_id":"sha256:…", "instrument_id":"…", "interval":"15m",
  "indicators":[{"id":"ema1","type":"EMA","params":{"n":20}},{"id":"rsi1","type":"RSI","params":{"n":14}},{"id":"st1","type":"SUPERTREND","params":{"atr":10,"mult":3}}],
  "warmup_bars":"auto" }
```
Server re-resolves candles by `series_id` (or accepts `instrument_id,interval,window`); a stale/unknown `series_id` ⇒ `409 SERIES_CHANGED` and client refetches. Response: per indicator `values` aligned to candle timestamps (array of numbers/nulls, or object of named arrays for multi-line), `meta`, `warnings`, `status`. Parameter validation per §6.2; `422 INVALID_INDICATOR_PARAM` lists the allowed range.

### 8.6 E8 – Data-driven chart analysis
Request:
```json
{ "instrument_id":"IN.XNSE.RELIANCE", "interval":"15m", "window":{"range":"5D"},
  "as_of":null, "horizons":["1D","5D"],
  "include":["technical","patterns","levels","news","forecast","explanation"],
  "indicators":[{"type":"RSI","params":{"n":14}}], "language":"en" }
```
Behaviour: uses **exactly** the requested instrument/interval/window; if the data cannot be served the response says so — **no silent substitution of symbol, interval or provider**. `as_of` (historical research) obeys leakage rules (§12.3).
Response (extends baseline §47): `analysis_input{instrument_id, interval, window, series_id, n_candles, last_complete_bar, data_class}`, `technical{indicator_states…}`, `levels{support[], resistance[], pivots, orb, vwap}`, `patterns{candlestick[], chart[], summary, conflicts[]}`, `news{status, window, items[], aggregate}`, `forecast{…see §9.4…}`, `drivers[]`, `risks[]`, `uncertainties[]`, `evidence[]`, `sections_status{technical, patterns, news, forecast, explanation}` (`ok|degraded|unavailable`), `metadata{…}`.

### 8.7 E10 – Forecast (see §9.4 for the object)
Request: `instrument_id`, `interval`, `horizon` (e.g. `"30m"|"1D"|"5D"`), `target` ∈ {`direction`, `exceeds_threshold`}, `threshold_pct?`, `as_of?`. Response: `forecast` object or `status:"unavailable"` with `reason ∈ {no_validated_model_for_instrument, no_validated_model_for_interval, insufficient_history, data_quality, out_of_distribution}`.

### 8.8 E11 – Research (full contract in §10.5)

### 8.9 Contract governance
Each endpoint: Pydantic request/response models; example payloads in OpenAPI; negative tests per error code; `openapi_before.json` vs `openapi_after.json` diff reviewed; breaking changes versioned (`/v2`) or gated by flags; **regression snapshot tests** on all pre-existing endpoints (Phase 15).

---

## 9. Data-Driven Chart Analysis, Forecasting and Fusion

### 9.1 Workflow (distinct from screenshot analysis) **[REQUIRED]**
```
(instrument_id, interval, window, as_of?) 
  → resolve instrument (§3.1)  → fetch OHLCV (one provider, one series_id) → validate (§3.6)
  → indicators (§6) ─┬→ levels (pivots/CPR/ORB/VWAP/S-R)  ─┐
                     ├→ candlestick + chart patterns (§7) ─┤
                     ├→ trend / volatility / structure features ─┤→ FeatureSnapshot (auditable)
  → news retrieval, as-of safe (baseline §6, §14; §9.5) ──────────┤
  → model registry lookup (§9.3) → forecast (if validated) → calibration/OOD checks
  → explanation (real attributions, baseline §27) → LLM narration of *verified* outputs only
  → response with sections_status
```
Hard rules: the analysed instrument/interval/window are exactly those requested (echoed in `analysis_input`); a failure yields `unavailable`, never a different symbol/interval; a screenshot is never treated as equivalent to market data.

### 9.2 Feature set
Baseline §8/§19 features plus intraday/charting features: distance from session VWAP in ATR units; opening-range position (above/inside/below; minutes since break); gap %; RVOL-ToD; previous-day-level proximity (in ATR); pivot/CPR proximity; trend-efficiency; ADX; Supertrend state; range expansion vs ATR; time-of-session bucket (open/mid/close); day-of-week; index-relative strength (instrument return − index return over the same window); realised volatility percentile; pattern states with age decay; news/event features (baseline §14, §38). Each feature registered in the `FeatureSpec` registry (baseline §19.2) with availability masks. Time-of-day features are categorical to avoid leakage from absolute timestamps.

### 9.3 Targets and model eligibility
- **Daily-or-longer horizons** (baseline §9): `direction`, `exceeds_threshold` (|return| > θ·ATR-scaled), three-class.
- **Intraday horizons** **[EXPERIMENTAL]**: (a) next-N-bars direction (N∈{1,3,6,12} bars of the chosen interval); (b) close-of-day direction from a fixed decision time (e.g. 30 min after open); (c) **triple-barrier label** aligned with trade plans: upper barrier `+a·ATR`, lower barrier `−b·ATR`, time barrier `H` bars → label ∈ {UP_FIRST, DOWN_FIRST, TIMEOUT}; labels use only bars after the decision bar (the decision bar's close is the reference); same-bar double-touch resolved conservatively (assume adverse barrier first) and counted in a diagnostic.
- **Cost-aware evaluation**: classification metrics are always accompanied by net-of-cost simulated expectancy (§12.4).
- **Eligibility gate** (`ModelRegistry.lookup(market, instrument_group, interval, horizon, target)`): a model may serve a request only if it was *trained and validated for that combination*. Otherwise `forecast.status="unavailable"`, `reason`, and the UI says: "No validated model for this instrument/timeframe." Cross-market or cross-interval extrapolation is not allowed silently.
- **Frozen model `1.0.0`** **[CLAIMED-UNVERIFIED]**: remains byte-identical; new models are new versions (`1.1.0`, `2.0.0`, …) registered as `candidate` and never replace `1.0.0` in place. `1.0.0` serves only the horizon/universe it was frozen for. Any code touching its loader requires an integrity test (hash equals the manifest from Phase 1).
- **Out-of-distribution (OOD)**: per-model OOD scorer fitted on training features only (e.g. robust z-score exceedance fraction + isolation-forest score); threshold chosen on validation; `ood_flag` lowers confidence and shows "Current conditions are unusual relative to the model's training data."

### 9.4 Forecast object **[REQUIRED]**
```json
{ "status":"ok|degraded|unavailable", "reason":null,
  "target": {"type":"direction|exceeds_threshold|triple_barrier","definition":"future_return_h = (close[t+h]-close[t])/close[t] > θ","threshold_pct":0.0,"barriers":{"up_atr":1.5,"down_atr":1.0,"time_bars":12}},
  "horizon": {"value":"5D","unit":"trading_days|bars","interval":"1D"},
  "prediction_time":"…UTC","data_as_of":"…UTC (last complete bar)",
  "classification": {"direction":"UP|DOWN|NEUTRAL|UNKNOWN","model_confidence":0.0,"probability_up":null,"probability_exceeds_threshold":null,"calibration_validated":false,"calibration":{"method":"platt|isotonic","brier":null,"ece":null,"n":0}},
  "expected_return": {"available":false,"value_pct":null,"interval_80":null,"note":"Shown only if a validated regression model exists"},
  "model": {"name":"…","version":"…","tier":"unvalidated|validated_val|validated_test","trained_on":"…","universe":"…","feature_set_version":"…","registry_id":"…"},
  "drivers":[], "risks":[], "uncertainties":[],
  "quality": {"data_quality_score":0.0,"freshness":"…","missing_feature_groups":["news"],"ood":{"flag":false,"score":0.0}},
  "components": {"technical":"bullish|bearish|neutral|unavailable","pattern":"…","news":"…","conflict":false,"disagreement_score":0.0},
  "disclaimer":"…" }
```
Rules: `probability_*` are `null` unless `calibration_validated`; classification probabilities and expected return are **separate fields**; no field returns a precise future price; `expected_return` appears only with a registered, validated regression model and an interval; the response never says "target price"; the forecast is explicitly "a model output, not a recommendation".

### 9.5 Point-in-time news and events
- **Historical/backtest** use: document eligible iff `published_at ≤ as_of` **and** `timestamp_quality = verified` (baseline §6.4/§7).
- **Live** use: eligible iff `published_at ≤ as_of` **and** `ingested_at ≤ as_of` (we cannot have known it earlier than we fetched it) – and both timestamps are stored and shown in evidence (`published_at`, `ingested_at`). For intraday models, news within the current bar's open→close is handled by the as_of definition (decision at bar close).
- Scheduled events (earnings dates) usable only if announced at/before `as_of`.
- Per prediction, store `FeatureSnapshot{snapshot_id, as_of, instrument_id, interval, series_id, features{name:value}, availability{group:bool}, source_ids[], timestamps{ohlcv_last_bar, news_latest_published, news_latest_ingested}, model_registry_id, config_hash, code_commit}` in `prediction_log` (immutable, append-only) so any shown number can be reproduced.

### 9.6 Model comparison and evaluation (extends baseline §22–25)
Models: **T** technical-only, **P** technical+patterns, **N** technical+news/RAG, **C** combined/stacked, plus trivial baselines (majority class, persistence, random, "previous bar direction", and for threshold targets the base rate). Protocol: purged/embargoed walk-forward (daily horizons: baseline §22; intraday: **day-blocked** walk-forward — all bars of a session stay in the same fold; embargo ≥ horizon bars across the session boundary), no tuning on the final untouched test, hyperparameters on validation only. Metrics: balanced accuracy, MCC, ROC-AUC, log-loss, **Brier**, ECE/reliability, accuracy-by-confidence-bucket, abstention coverage; paired block-bootstrap or McNemar for T vs P vs N vs C; 95% CIs everywhere; per-interval, per-market, per-regime reports (baseline §56); transaction-cost-aware simulated expectancy for any model-driven rule. A model is promoted to `validated_test` only if it beats the best trivial baseline on the untouched test with a CI that excludes zero improvement **and** is calibrated (or is labelled "confidence only"). Class imbalance: report base rates, use balanced metrics, never headline raw accuracy alone. Profitability is **never** inferred from accuracy.

### 9.7 LLM role boundary
The LLM may (a) narrate verified outputs, (b) summarise retrieved evidence, (c) structure extracted news sentiment (baseline §11). It may not create or alter numeric predictions, probabilities, levels or patterns. Enforcement: the narration prompt receives the forecast object as read-only JSON; a post-validator extracts every number in the narrative and asserts it exists in the object/evidence (tolerance for rounding) – mismatches ⇒ narrative discarded and replaced with a template rendering. Any future "LLM adjustment" requires a registered, tested mechanism and is out of scope.

### 9.8 Screenshot-based Chart Vision (separate, complementary) **[REQUIRED changes to existing feature]**
Keep baseline §17 and upload security (baseline §45): PNG/JPG/WEBP only, MIME + magic bytes + size + dimensions + re-encode, no execution, no retention by default.
Changes/clarifications:
1. Output sections are physically separated: **"Image observations"** (what is visibly drawn) vs **"Verified market-data calculations"** (only present if the user supplied/confirmed an instrument and clicked *Compare with data*, which calls E8).
2. `ticker` and `timeframe` appear in results only if (a) visibly legible in the image, with `source:"image_text"` and confidence, or (b) provided by the user with `source:"user_supplied"`. Otherwise `Unavailable`.
3. Fields the model cannot reliably read return the literal `"Unavailable"` or `"Unclear"`; **no exact support/resistance prices from pixels** – use qualitative positions ("near the upper part of the visible range") unless axis labels are clearly legible, in which case mark `approx` and `read_from_axis:true`.
4. Patterns are "visually apparent candidates" with uncertainty; never "detected"; the UI never implies the app has the OHLCV behind the image.
5. If the image is not a price chart or is unreadable: exactly "Insufficient visual evidence."
6. The agreement report with data (baseline §18.3) lists agree/conflict/not-comparable per item and always prefers the numerical data.
7. Regression tests: previously accepted uploads still pass; malicious files still rejected; hallucination test on blank/unrelated images yields zero pattern claims.

---

## 10. General-Purpose AI Research Assistant

### 10.1 Defect-hypothesis audit (Phase 1/10 — test each with recorded evidence)
| ID | Hypothesis | How to test |
|---|---|---|
| H1 | Frontend submits a fixed/default question or drops the typed text | Inspect form handler and the network payload for 10 distinct queries |
| H2 | Payload/field mismatch (e.g. `query` vs `question`) so the backend falls back to a default | Compare Pydantic model with the client; send each variant with `curl` |
| H3 | Keyword/intent routing sends many questions to one template | Trace router; feed unrelated queries; diff outputs |
| H4 | Endpoint is effectively ticker-only (query ignored in prompt) | Read prompt builder: is the user text interpolated? |
| H5 | Response cache keyed by ticker (not query) returns identical output | Inspect cache key; issue two queries for one ticker |
| H6 | Fenced/malformed JSON from the LLM triggers a generic fallback that masks the failure | Inject ` ```json ` fences, trailing commas, truncated output |
| H7 | Provider errors (503, quota, invalid model) are swallowed and replaced with canned text indistinguishable from success | Fake provider errors; inspect UI |
| H8 | Frontend renders only a subset of fields; markdown/tables/links not rendered | Component review with rich payloads |
| H9 | Company/ticker resolution defaults (e.g. blind `.NS`) or mixes entities across turns | Ambiguity tests; multi-turn tests |
Results go into `docs/audit/research_assistant_findings.md`; fixes in Phase 10 must each reference a hypothesis ID.

### 10.2 Target architecture **[REQUIRED]**
```
Question (raw) ─► sanitise (length ≤ 2000, strip control chars; keep meaning) ─► QueryPlanner
   QueryPlan{ entities[resolved|ambiguous|none], time_window?, intents[multi-label, open-ended],
              required_data[tools], answer_style, needs_clarification?, safety_flags }
 ─► ToolExecutor (parallel where independent; per-tool timeout; call budget ≤ N)
      tools: resolve_instrument · get_quote · get_ohlcv · compute_indicators · get_levels · get_patterns
             get_forecast · search_news(RAG) · get_fundamentals · get_filings_events · get_peers
             get_index_overview · get_calendar_events
 ─► EvidencePack{ items[id, tool, status, as_of, source, url?, published_at?, payload] }
 ─► AnswerComposer (LLM, JSON schema; sees raw question + plan + evidence + safe conversation context)
 ─► Validators (schema · citation · numeric-consistency · forbidden-phrase · query-echo · injection)
 ─► Report{ query_echo, answer_to_question, sections[], evidence[], unverified[], status, metadata }
```
- **Planner is not a keyword router.** Intents are open-ended labels produced from the question's meaning (LLM when available) and may be several at once; entity resolution and time-window extraction are explicit. If the LLM is down, a deterministic planner still extracts entities/dates and selects a *superset* of cheap tools; the composer (or a template) then answers *with the raw question echoed* and `status:"degraded"`. No path returns a canned answer detached from the question.
- Unknown/unsupported question types are allowed: the composer answers from whatever evidence exists and lists what it could not verify (`unverified[]`) rather than refusing or defaulting.
- Out-of-scope requests (e.g. "should I buy?", "guarantee me a price") get a direct, polite explanation plus the nearest research-style answer (signals, scenarios, risks).
- LLM calls per question ≤ 3 (plan, compose, optional repair); tool calls bounded; total deadline (default 45 s) with partial results returned on timeout.

### 10.3 Query preservation
`request.query` is stored verbatim (trimmed). The response contains `query_echo` equal to it; the UI displays it above the answer; logs store a hash and the text (redacted per privacy policy). No component may substitute, translate, summarise or default the query before the composer sees it. Test: for 20 random queries `response.query_echo == request.query.strip()`.

### 10.4 Partial reports and section status
Each section: `status ∈ {ok, degraded, unavailable}`, `reason`, `sources[]`. Examples: price section `ok` (OHLCV tool succeeded) while news section `unavailable (retrieval empty)` and explanation `degraded (LLM unavailable; template used)`. The top-level `status` is the worst severity among sections the question *requires*. The frontend shows per-section badges and never hides unavailability.

### 10.5 Contract (E11)
Request:
```json
{ "query":"How did TCS do versus INFY over the last 3 months and what are the main risks?",
  "session_id":null,
  "context":{"instrument_id":"IN.XNSE.TCS","interval":"1D","window":{"range":"3M"}},   
  "options":{"max_evidence":10,"language":"en","as_of":null} }
```
`context` is an optional *hint* from the UI (current chart), never an override of the entities in the query; if the query names other entities, they win and the response states which entities were analysed.
Response:
```json
{ "request_id":"…","query_echo":"…","session_id":"…","status":"ok|degraded|unavailable",
  "entities":[{"instrument_id":"…","resolved_from":"TCS","confidence":0.99}],
  "answer_to_question":"direct 2–5 sentence answer, hedged, grounded",
  "sections":[{"id":"…","title":"…","status":"ok","blocks":[
      {"type":"text|table|metric|list|chart_ref","content":"…","evidence_ids":["ev3"],"label":"observed_fact|computed_metric|model_output|ai_interpretation"}]}],
  "evidence":[{"id":"ev3","tool":"get_ohlcv","as_of":"…","source":"…","url":null,"published_at":null,"summary":"…"}],
  "unverified":["Q2 revenue growth could not be retrieved from a configured source"],
  "risks":[],"uncertainties":[],
  "disclosure":"This answer used only the listed tools and evidence; the model did not browse the internet.",
  "metadata":{"llm":{"provider":"…","model":"…","status":"ok","attempts":1},"prompt_version":"…","latency_ms":0,"tools_called":["resolve_instrument","get_ohlcv","search_news"]} }
```
Citations: every `evidence` entry is created by code from tool output; the composer may reference only IDs in the pack; URLs/timestamps come from metadata; invalid IDs ⇒ block removed + `unverified` entry. If a provider-side grounded-search feature is ever enabled, its returned source list must be captured as evidence items; without it, the disclosure line stays.

### 10.6 Follow-ups and context safety
`session_id` ties turns; server keeps (TTL e.g. 30 min, per-user, size-capped) the last K=4 turns' `query_echo`, `entities`, `answer_to_question`, and evidence *summaries*. A follow-up's own text is processed by the planner with: `active_entities` (those of the last turn) and `previous_turn_summary`. Rules: (1) pronouns ("it", "that company") resolve only if exactly one active entity exists, else ask a clarifying question; (2) if the follow-up names a different instrument, **switch entity context** – old company facts are not reused unless the question is a comparison, and each fact in the answer keeps its entity tag; (3) evidence is re-fetched or re-validated if older than its TTL; (4) context token budget enforced (truncate oldest); (5) user can "New topic" to clear; (6) no cross-session or cross-user memory leakage.

### 10.7 Frontend rendering requirements
Markdown via a sanitising renderer (GitHub-flavoured: headings, lists, tables, code, links) – **no `dangerouslySetInnerHTML` on model text**; allowed URL schemes http/https/mailto; external links `rel="noopener noreferrer"` + `target="_blank"`; responsive tables (horizontal scroll); block labels rendered visibly (Observed fact / Computed metric / Model output / AI interpretation); evidence drawer with source, timestamp, retrieval age; per-section status badges; copy/export (Markdown); loading skeleton with cancel; error panels showing `code` + actionable text; persistent disclaimer; focus management and `aria-live` for streaming/finished state.

### 10.8 Parsing and robustness
Strip fences; extract first balanced JSON object; strict parse → schema validation (Pydantic, `extra=forbid`) → on failure one repair prompt with the validation error → on second failure build a **degraded** report from tool outputs via templates (still echoing the question) and set `llm.status="degraded"`. Handle: empty response, truncated JSON, missing fields (field-level defaults only where semantically safe, otherwise mark section degraded), oversized output (cap), non-UTF8, provider timeout/quota/model-config errors (§3.7). Everything logged with request id, never with secrets.

### 10.9 Query-focused test suite **[REQUIRED]** (`tests/ai/research/`)
Each test asserts: correct entity resolved, `query_echo` preserved, expected tools called, answer contains tool-derived facts (or an `unverified` entry), no fabricated numbers/citations, and structurally different reports.

| # | Query (substantially different types) | Expected behaviour |
|---|---|---|
| 1 | "What was Infosys's revenue growth last quarter?" | `get_fundamentals`/filings tool; figure from structured data with period & source, or `unverified` |
| 2 | "How did TCS move between 1 March and 30 April 2026?" | OHLCV for that window; return computed in code equals independent calc |
| 3 | "Analyze RELIANCE technicals on the 15-minute chart" | indicators + levels + patterns on 15m; no news template |
| 4 | "Compare HDFC Bank and ICICI Bank on valuation and recent news" | two entities, fundamentals + news for each, side-by-side table |
| 5 | "What risks does Tata Motors face?" | news/fundamental risk evidence with citations; otherwise states limits |
| 6 | "Why is NIFTY falling today?" | index overview + contributors + news; correlation≠causation language |
| 7 | "Any earnings or corporate actions coming up for AAPL?" | calendar tool; `unverified` if unavailable |
| 8 | Follow-up: "And what about its debt?" after #1 | resolves to Infosys; fundamentals leverage block |
| 9 | Follow-up naming a new company mid-session | context switches; no mixing |
| 10 | "Tell me about Apple" (ambiguous: fruit/company/ticker) | resolves or asks a clarification; no silent guess |
| 11 | "What will Tesla's price be next Friday exactly?" | declines exact price; provides horizon-explicit probabilistic forecast if validated else explains |
| 12 | "Is silver in an uptrend?" | commodity instrument path |
| 13 | Prompt-injection text inside a retrieved news item | ignored; flagged |
| 14 | LLM provider down (503) | `degraded` deterministic report with echoed question |
| 15 | LLM model misconfigured (404 model) | `LLM_MODEL_INVALID`, actionable message, deterministic sections still returned |
| 16 | Malformed/fenced JSON from LLM | repaired or degraded path; no crash |
| 17 | Non-English / very short / very long query | handled; length cap error is explicit |
**Anti-canned check:** across tests 1–12, pairwise similarity of `answer_to_question` (token Jaccard and embedding cosine) must be below a configured threshold, and the set of `tools_called` must vary with the question.

---

## 11. Trader Toolkit (new modules missing from the baseline)

### 11.1 Daily workflow → modules

| Phase of the trading day | What the trader needs | Module |
|---|---|---|
| Pre-market (before 09:15 IST / 09:30 ET) | Global cues, gap candidates, event/earnings risk, key levels | Market Context (11.2), Scanner (11.4), Levels (6.3) |
| Open (first 15 min) | Opening range forming, volume surge, index direction | Chart workspace + ORB tools; no-signal period by default |
| Mid-session | Trend vs range day, VWAP behaviour, relative strength | Day-type context, scenario plan (11.5), alerts |
| Late session | Square-off timing, overtrading control | Session clock, risk meter, daily limit |
| After close | Review, journal, evidence | Journal/analytics (11.7), setup lab (11.9) |

### 11.2 Market context (index analytics) — E12 **[REQUIRED core; data-dependent parts flagged]**

| Component | Source / availability | Notes |
|---|---|---|
| Index OHLC (NIFTY 50, BANK NIFTY, SENSEX, NIFTY IT, S&P 500, Nasdaq, Dow, Russell 2000) | Market-data provider | Symbols via instrument master **[VERIFY]** |
| Volatility index (India VIX, VIX) | Provider **[VERIFY availability]** | Shown with percentile vs trailing 1y |
| Breadth (advancers/decliners, % above VWAP/50-DMA) | Computed from constituent quotes if constituents + quotes available; else `unavailable` | Do not estimate from the index alone |
| Index contribution (top movers by weight × return) | Official weights **[VERIFY]** | Approximate weights flagged |
| Sector/heat-map | Sector indices or constituent aggregation | |
| Global cues (US indices/futures, DXY, crude, gold, US 10y, USD/INR; GIFT Nifty) | Provider **[VERIFY each]** | Labelled with each source timestamp/time zone |
| FII/DII flows | Exchange-published daily data **[VERIFY terms]** | Previous-day, labelled; never intraday-live |
| Option-chain PCR / max pain | **[OPTIONAL]** only from a permitted source | No ToS-violating scraping |
| Event calendar (RBI/Fed, results, expiry days, holidays) | Reviewed calendar table + permitted feeds **[VERIFY]** | Only events announced at/before now |
Deterministic **day-type/regime labels** (not signals): gap type (up/down/flat, size vs ATR), opening-range status, VWAP relationship, ADX bucket, realised-vol percentile, trend-efficiency → e.g. "Trending up (ADX 28, price above VWAP, efficiency 0.62)". Each label shows the numbers behind it.

### 11.3 Fundamentals module — E13
**Purpose:** selection and risk flags (what to watch, what to avoid), not intraday timing.
Data model (all values carry `period_end`, `announced_at/filed_at`, `source`, `currency`, `units`, `basis ∈ {standalone, consolidated}`, `restated: bool`):
- Valuation: P/E, P/B, EV/EBITDA, dividend yield, market cap (and percentile vs sector peers).
- Growth: revenue, EBITDA, PAT YoY and QoQ, 3y/5y CAGR.
- Profitability: operating/net margin, ROE, ROCE.
- Balance sheet: debt/equity, net debt/EBITDA, interest coverage, current ratio.
- Cash quality: CFO/PAT, FCF, receivable days trend.
- Ownership: promoter holding and pledge (India), institutional holding, recent change.
- Calendar: next results/board-meeting date (if announced), dividend/split/bonus ex-dates.
- Peers: sector/industry peers from the instrument master; median and percentile ranks.
**Scoring (descriptive, transparent):** five pillars (Growth, Profitability, Balance sheet, Cash quality, Relative valuation), each 0–100 via published rule tables (thresholds in config, shown in UI with the underlying metrics). Missing inputs ⇒ pillar `unavailable`, not zero. UI label: "Descriptive summary — its relationship with future returns has not been validated." An optional factor study ([EXPERIMENTAL]) may test pillar scores vs forward returns with point-in-time data; until positive, no performance claim.
**Sources [VERIFY, Q7]:** US – SEC EDGAR filings/XBRL "company facts" (official, free); unofficial aggregators (e.g., Yahoo-based fields) only as clearly labelled low-reliability fallback. India – exchange-published results/XBRL filings and shareholding patterns where terms allow; commercial or ToS-restricted sites **must not** be scraped. Where no permitted source exists, the module reports `unavailable` for the field and says why.
**Point-in-time:** historical analysis uses `filed_at/announced_at ≤ as_of`; restated values kept as revisions. Currency/unit normalisation tested (e.g. crore vs million).
**LLM use:** may summarise management commentary or risk factors from filings with citations to the filing URL and publication time; all numbers come from structured data or are quoted ≤ 15 words with citation.

### 11.4 Scanner — E14
Named scans (parameterised, deterministic, evaluated on **completed** bars at `as_of`):
1. Pre-market/at-open **gap up/down** with abnormal volume (needs volume; at pre-open use previous-day data and quote).
2. **Opening-range breakout** candidates after the OR window completes (price relative to OR, volume ratio).
3. **RVOL-ToD leaders**.
4. **VWAP reclaim / rejection** (cross with close confirmation, ATR-distance filter).
5. **Near 52-week/N-day high or low** with volume.
6. **Compression** (inside bar, NR7, Bollinger bandwidth percentile) → "watch for expansion".
7. **Relative strength/weakness vs index** over chosen window.
8. **Sector leaders/laggards**.
Universe: user watchlist, index constituents, or "supported liquid list" (coverage honest, §3.1). **Liquidity & safety filters** (configurable; applied before ranking): minimum average daily traded value, minimum price, minimum bars available; exclusion/flag lists when data is available — exchange surveillance categories, F&O ban list, circuit-limit-hit, results-today/ex-date-today (otherwise flag "not checked"). Budget: ≤ N symbols per run (set from provider limits), batched, cached, cancellable; partial results returned with `completed/total`.
Output row: `instrument_id, scan_id, as_of, data_class, metrics{…}, conditions[{rule, passed, value, threshold}], flags[], evidence_level` (from setup lab if available), `chart_link`. Sorting by a stated metric; **never** a "top picks to buy" ranking. Each result card says "Candidate for review – conditions met, not a recommendation."

### 11.5 Scenario trade plan — E15 **[REQUIRED]**
Purpose: turn analysis into a *testable, risk-defined scenario*, and make "no trade" an explicit, respectable outcome.
Input: `instrument_id, interval, scenario ∈ {long, short}, capital, risk_pct, setup_id?, as_of?, cost_profile`.
Computation (deterministic; AI forecast shown only as context):
1. Trigger: from the chosen setup rule (e.g. close above OR high; VWAP reclaim; resistance break) with the exact bar condition.
2. Invalidation/stop: structure-based (beyond swing low/OR low/VWAP/level) **and** not tighter than `k·ATR` (default k=0.5–1.0) to avoid noise stops; if structure stop would exceed max allowed risk, plan fails the sizing check rather than silently tightening.
3. Targets: at 1R/2R/3R and at the next computed levels (pivots, S/R, day extremes); partial-exit suggestions are labelled optional.
4. Time stop: exit if no progress after N bars or by a configured clock time (before the user's square-off reminder).
5. Costs: §11.6 → `c` and breakeven probability `p*` (§2.5); net R:R.
6. Sizing: `qty` per §2.5 with lot size and liquidity cap.
7. **Plan-quality checklist** (pass/warn/fail): data fresh & not delayed beyond tolerance; liquidity; R:R net ≥ minimum (default 1.5); `c` ≤ cap (default 0.25R); distance to adjacent opposing level ≥ 1R; event risk (results/major macro within window); signal conflict (§7.5, baseline §28); market-context alignment (index regime); setup evidence level (11.9); volatility regime sane; daily risk budget remaining; trades-today under cap.
8. **Verdict states**: `scenario_ready` (all pass/warn), `scenario_weak` (warnings), `no_trade_conditions_not_met` (any fail). Language: "Scenario: IF price closes above X on 15m with volume ≥ …, THEN reference stop Y, targets Z. Historical evidence for this setup: …".
Response includes everything needed to reproduce the numbers (inputs, series_id, parameters hash). No "buy/sell now". Refused (with reason) when data is stale/unavailable or invalidation cannot be defined.

### 11.6 Cost and risk calculators — E16
Cost model is **configuration**, not code constants: `configs/costs/{market}.yaml` with each component's rate, basis (turnover, brokerage, buy/sell side), min/max caps, `source_url`, `verified_on`. Components (India equity intraday): brokerage (flat/percent/capped per order), securities transaction tax (sell side), exchange transaction charges (NSE/BSE rates differ), SEBI turnover fee, stamp duty (buy side), GST (on brokerage + transaction charges + SEBI fees), plus modelled slippage (ticks or bps, ATR-scaled option). US: commissions (often zero), regulatory sell-side fees, slippage **[VERIFY all rates; rates change]**. Output is labelled "Estimate – confirm with your broker's contract note". F&O/options costs [OPTIONAL]. Tests: component arithmetic with fixtures derived from an official published worked example **[VERIFY]**; rounding rules; side-dependent charges; min/max caps; zero-qty; extreme prices.
Risk tools: position-size (§2.5), risk-per-trade meter, daily loss limit and max-trades-per-day (advisory), risk-of-ruin illustration table (clearly "illustrative, assumes independent trades"), breakeven calculator (`p*`).

### 11.7 Paper trading and trade journal — E17
**Paper engine (simulation, conservative fills):**
- Market order fills at the **next bar's open** + slippage (never the signal bar's close).
- Limit order fills only if the bar trades *through* the limit by ≥ 1 tick (price merely touching is not a guaranteed fill).
- Stop order triggers on touch; fill = stop ± slippage, or the bar's open if it gaps through.
- If stop and target are both within one bar → assume **stop first** unless a finer interval resolves the order; counter in diagnostics.
- Intraday (MIS-style) positions auto-flat at a configurable time; costs applied per §11.6; liquidity cap enforced; no leverage beyond a configured margin multiple.
- Data class `DELAYED_UNVERIFIED` ⇒ paper fills flagged "approximate".
**Journal:** `trade_id, instrument_id, side, qty, planned{entry, stop, targets, setup_id, plan_id}, executed{entry_time, entry_price, exit_time, exit_price}, fees_est, fees_actual?, notes, tags (setup, mistake, emotion), attachments (images via upload security), R_result, MAE/MFE (computed from stored OHLCV between entry and exit), created_at`. Entries keep an **append-only revision history** (edits create revisions; the original plan values remain visible) so reviews cannot be rewritten after the fact.
**Analytics (deterministic):** n trades, win rate with Wilson CI, average R, expectancy (net), payoff ratio, profit factor, equity curve, max drawdown, costs as % of gross, performance by setup / time-of-day / weekday / instrument / regime, MAE/MFE distributions (stop-placement insights), and **discipline metrics**: % trades with predefined stop, average risk vs cap, oversize flags, trades-after-loss within N minutes, size-up-after-loss, trades outside plan window, daily trade/loss limit breaches, plan adherence (exit as planned vs discretionary). Minimum-sample guard (e.g. n<30 ⇒ show numbers but label "insufficient sample"). An LLM may *describe* the computed stats but cannot invent them. Storage: local-first or per-user server store (Q3); export/delete-all; no sharing by default.

### 11.8 Watchlists and alerts — E18
Alert types: price crosses level, touches a user/auto level, crosses VWAP, RSI threshold, ORB break, pattern completed (confirmed), session events. Evaluated on **completed bars** (or provider ticks only if `LIVE`); each alert stores condition, instrument, interval, created_at, cooldown, one-shot/recurring, max active (e.g. 25). Delivery: in-app + Browser Notification API (permission-gated) [email OPTIONAL]. UI states delay honestly ("Evaluated on delayed data"). Deduplicate and rate-limit. Alerts never trigger orders.

### 11.9 Setup lab — evidence before conviction (E19) **[REQUIRED for any "historical evidence" claim]**
**Setup DSL** (JSON/YAML, versioned, hashed): `entry` (boolean expression over indicators/levels/patterns on completed bars; trigger bar; direction), `filters` (time window, day-type, index regime, liquidity), `stop`, `targets`, `time_stop`, `sizing` (fixed risk), `params` with small pre-declared grids.
Initial catalogue **[PLANNED]**: (1) Opening-range breakout (5/15/30 min) with volume filter; (2) VWAP pullback in an established trend; (3) VWAP reclaim/rejection; (4) support/resistance rejection (computed levels); (5) gap-and-go / gap-fill; (6) inside-bar/NR7 expansion; (7) EMA 9/21 pullback; (8) Supertrend flip with ADX filter. Parameters and universe are **pre-registered** (config committed before evaluation).
**Engine:** event-driven, bar-by-bar, decisions on completed bars only; fills per §11.7; costs/slippage per §11.6; day-blocked walk-forward (anchored or rolling); parameters (if any) chosen on training days only; untouched final test period.
**Reported per setup × instrument group × interval × period:** trades (n), win rate (Wilson CI), average R net, expectancy with **day-block bootstrap CI**, profit factor, max drawdown, MAE/MFE, time-of-day and regime breakdowns, cost drag, sensitivity to cost ×0.5/×1/×2/×3, comparison with a **random-entry control** (same stop/target/time stop, random entries during allowed windows), number of variants tested and multiple-testing adjustment (BH or deflated Sharpe-style reasoning).
**Evidence tiers:** `cannot_evaluate` (insufficient data/lookback), `insufficient_sample` (n < 30 or < 20 independent days), `negative`, `positive_not_robust`, `positive_robust` (net expectancy CI > 0 on the untouched test, survives ×2 costs, beats random control, positive in a majority of walk-forward folds). The scorecard is shown beside any scenario plan or scan using that setup, with the banner **"HISTORICAL SIMULATION — NOT FUTURE PERFORMANCE."** Honest negative results are first-class output and stay visible. Data-limit statement: the period/lookback covered, provider, and survivorship caveats are printed on every scorecard.

### 11.10 Prospective intraday signal ledger **[PLANNED]**
Separate from, and never modifying, the existing prospective ledger/model `1.0.0` records.
- **Append-only** store (`prospective_intraday_ledger`): each record has `signal_id`, `created_at` (server UTC), `as_of_bar`, `instrument_id`, `interval`, `source` (model version or setup id), `signal` (forecast or scenario trigger), `feature_snapshot_hash`, `config_hash`, `code_commit`, `prev_hash`, `hash` (hash chain). Outcomes are separate `outcome` records referencing `signal_id`, written by a scheduled job after the horizon ends. No update/delete paths exist in code; a nightly verifier recomputes the chain and alerts on mismatch.
- **Automated, pre-declared issuance** on a fixed universe/schedule (prevents cherry-picking); user-triggered analyses are stored as `exploratory` and excluded from official statistics.
- Metrics (hit rate with CI vs base rate, Brier/ECE, expectancy after costs for rule-based signals) are computed only from matured outcomes and published with sample size; below the minimum sample the dashboard says "insufficient prospective sample".
- **Never manufacture, backfill or edit** prospective observations to satisfy a review gate; backfilled research results live in `experiments/` and are labelled retrospective.

---

## 12. Verification Plan (Testing, Scientific Validation)

### 12.1 Frontend tests (Vitest/Jest + Testing Library; Playwright for e2e)
| Area | Tests |
|---|---|
| Range selector | Each preset triggers exactly one new `GET /ohlcv` with the resolved params (mock server asserts); displayed first/last timestamps change; active state follows data, not just click; rapid clicks cancel earlier requests; stale responses ignored (`requestSeq`) |
| Interval selector | Unsupported combos disabled with tooltip; selecting an allowed interval refetches; persisted invalid preference shows a notice and is not silently swapped |
| Custom range | Validation messages (start≥end, future, over-span); holiday-snapping notice; datetime for intraday |
| Prev/next/latest | Window shifts by its length; disabled at bounds; Latest re-enables refresh |
| Pan/zoom + pagination | Reaching the left edge requests `before=…`; merge de-duplicates; memory cap |
| Chart types | Line/Area/OHLC/Candles/HA switch without refetch; candle tooltip shows real OHLC; HA transform unit-tested; volume pane colouring |
| Indicators | Add/configure/remove multiple; parameter validation; pane creation for oscillators; overlay legend; readability limits message; persistence & corrupted-storage recovery; recompute on interval change |
| Drawings | Create/move/delete per tool; scoping by interval; undo/redo; clear with confirm; localStorage failure handling; text sanitised |
| States | Loading skeleton, empty (each reason code), provider error with retry, stale banner, partial; no uncaught exception (error boundary test) |
| Symbol switching | Ambiguity dialog; state reset (indicators kept, drawings swapped); no data leakage between symbols |
| Analysis panel | Renders forecast, drivers, risks, uncertainty, `unavailable` reasons, conflict banner, data-class badge |
| Research UI | 17-query matrix (§10.9) against a mock backend: query echo shown; markdown/table/link rendering; no `dangerouslySetInnerHTML`; section badges; degraded/unavailable displays |
| Trader UI | Plan view with verdict states; cost/breakeven display; scanner results; journal/paper flows; discipline warnings |
| Responsive | Playwright viewports 375, 768, 1024, 1440 – no horizontal page scroll, touch targets ≥44px, bottom-sheet pickers |
| Accessibility | `axe` automated checks (0 serious/critical violations), keyboard-only walkthrough scripts, focus order, aria-live announcements, reduced-motion, "view as table" |
| Visual regression | Snapshot key states (dark theme) |

### 12.2 Backend tests (pytest)
Ticker resolution (exact, alias, ambiguous 409, unknown, never blind suffix); provider adapters with recorded fixtures (200/404/429/5xx/timeout/empty/schema-change); retry/timeout bounds (assert max attempts and max elapsed with fake clocks); circuit breaker; capability and range/interval validation matrix; calendar (holidays, special sessions, DST); **aggregation** (bucket anchoring NSE/NYSE, partial buckets, missing constituents, session boundaries, weekly/monthly, derived-vs-native daily reconciliation); indicator golden fixtures + truncation invariance + parameter grids; level tools (pivots/CPR/ORB availability/RVOL-ToD); candlestick and chart-pattern unit tests (§7.4/7.6); data-driven analysis (symbol/interval honoured; no silent fallback; section statuses); forecast schema & eligibility gate (no model ⇒ `unavailable`); OOD flag; probability exposure rule; LLM provider error classification (503 transient, 429 quota, 404 model invalid permanent); JSON parsing/repair; research (query preservation, tool selection, citation/timestamp integrity, numeric consistency, follow-up entity switching, injection); cost model; position sizing; paper-engine fills (next-bar, stop-first, gap-through); journal revision history; ledger hash-chain (tamper ⇒ verifier fails); upload security matrix (baseline §45); API contract tests for every endpoint and error code; OpenAPI diff; fixture-import ban.

### 12.3 Leakage and point-in-time suite (extends baseline §7.5) **[CI gate]**
Future-perturbation (all bars after *t* randomised ⇒ features/patterns/forecast at *t* unchanged) for each interval; derived-interval check (aggregated bar at *t* cannot include constituents after its close); ORB/pivot level availability; pivot `confirmed_at` enforcement; news `published_at`/`ingested_at` rules (§9.5) with boundary cases; scaler fit isolation; day-block fold disjointness; label-window embargo; shuffled-label sanity (≈ chance); too-good-to-be-true alarm (daily direction ceiling 65%, intraday ceiling configurable; exceeding ⇒ mandatory audit report before any result is published); setup-lab engine uses only completed bars (lookahead injector test: a rule peeking at the next bar must make the test fail).

### 12.4 Quantitative evaluation protocol
1. **Pre-registration**: universe, periods, intervals, horizons, targets, feature groups, models, hyperparameter grids, setup definitions and cost profiles are committed in `experiments/configs/` *before* seeing validation/test results.
2. **Splits**: chronological train/validation/untouched-test; walk-forward (expanding and rolling) with purge/embargo; intraday day-blocked folds. Report the actual periods available (never fabricate coverage).
3. **Baselines**: majority, persistence, random, previous-bar, base-rate (threshold targets), buy-and-hold for the instrument/index where relevant.
4. **Metrics**: classification (balanced accuracy, MCC, AUC, log-loss), probabilistic (Brier, ECE, reliability), selective (accuracy vs confidence bucket, coverage vs abstention), *economic* (net-of-cost expectancy in R, profit factor, max DD, turnover) – economic metrics never inferred from accuracy.
5. **Uncertainty**: block/stationary bootstrap CIs; paired tests between models on identical samples; report n and effective sample size.
6. **Ablations**: T / P / N / C (+ no-rerank, no-recency, masked-entity news, shuffled-news control, feature-group dropout); random-entry control for setups.
7. **Selection discipline**: model/hyperparameter/threshold choices on validation only; the final test is evaluated once per registered candidate; every run is logged (count of trials reported; multiple-testing adjustment applied).
8. **Regime-aware**: bull/bear/high-vol/low-vol/major-news (baseline §56) plus intraday day-types (trend/range/gap), each with sample counts and CIs.
9. **Costs & slippage**: applied per §11.6; sensitivity ×0.5–×3.
10. **Reporting**: auto-generated `experiments/reports/<run_id>/report.md` with limitations (non-empty), exact configs, dataset snapshot IDs, commit hash.
11. **Claims policy**: no statement that a model/setup "works", "is profitable" or "beats the market" unless the corresponding report meets the evidence tier; the benchmark claim in baseline §24 stays "reported/unverified" until reproduced.

---

## 13. Implementation Phases

**Phase map vs the brief's required list** (the brief's 13 areas are all present; order adjusted so provider resilience precedes features that depend on it, and trader modules are added):

| Brief item | This spec |
|---|---|
| 1 Baseline audit | Phase 1 |
| 2 Market-data & ticker correctness | Phase 2 |
| 10 Provider resilience | **Phase 3** (moved earlier) |
| 3 Range & interval | Phase 4 |
| 4 Charting engine | Phase 5 |
| 5 Indicators | Phase 6 |
| 6 Candle & chart patterns | Phase 7 |
| 7 Data-driven chart analysis | Phase 8 |
| 8 Forecasting & fusion | Phase 9 |
| 9 Research Assistant | Phase 10 |
| *(new)* trader toolkit | Phases 11, 12, 13 |
| 11 UI polish/a11y | Phase 14 |
| 12 Regression/quant/security | Phase 15 |
| 13 Docs/deploy/acceptance | Phase 16 |

Dependency graph: `1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9`; `3 → 10`; `(2,3,6) → 11`; `(6,7,11) → 12`; `(6,7,12) → 13`; `(5..13) → 14 → 15 → 16`. **Parallel allowed** only when interfaces are frozen: Phase 5 (frontend engine spike/adapter) may run beside Phase 4 backend work once the `OHLCV` response schema (§8.4) is merged; Phase 7 pattern unit work may start beside Phase 6 after the candle schema is frozen; Phase 10 planner/tool work may begin after Phase 3 (LLM resilience) and the tool schemas, independent of Phases 8–9 (tools degrade gracefully when forecast/patterns are unavailable).

**Global rules for every phase:** write tests with the code; update OpenAPI + regression snapshots; evidence file `docs/evidence/phase-NN.md`; feature flags for risky UI (`chart_workspace_v2`, `research_v2`, `trader_toolkit`); no changes to frozen `1.0.0` artefacts, historical metrics, snapshots or the existing prospective ledger (integrity test in CI from Phase 1 onward); mock data only in test dirs; commit per task with conventional messages; stop and report if a Definition of Done item cannot be met rather than weakening the criterion.

---

### Phase 1 — Baseline audit and acceptance mapping
**Objective:** establish the true current state from code, not documents; fix the acceptance baseline; freeze integrity references.
**Exact expected behaviour:** `docs/audit/BASELINE_AUDIT_2.md` + `baseline_audit.json` classify every feature in §1.3 and §7.1 as `IMPLEMENTED_VERIFIED/…/MISSING`; `integrity_manifest.json` lists SHA-256 of model `1.0.0` artefacts, model cards, historical metric files, snapshots, ledger files; a CI job fails if any hash changes.
**Inspect:** everything in §1.6; `AIplannedcld.md`; `docs/FINAL_ACCEPTANCE_AUDIT.md`; OpenAPI; test/lint/build configs.
**Expected to change:** only `docs/audit/*`, `docs/evidence/phase-01.md`, CI config (integrity job), possibly this spec's *Files* lists.
**Dependencies:** none.
**Tasks:** run §1.6 steps 1–12; record failing tests/builds; test H1–H9 (§10.1) and capture payloads; list unsupported claims; produce the requirements→current-status table; resolve Q1–Q4, Q6; update traceability (§15) with real paths; decide chart-engine path (keep vs spike).
**API/schema changes:** none (dump `openapi_before.json`).
**Tests:** integrity-manifest verifier; baseline suite runs recorded.
**Edge cases:** missing tests/builds failing (record, don't hide); repo lacks `1.0.0` (record as "not found", do not create or invent it); secrets found (rotate and report, don't print).
**Definition of Done:** audit docs committed; every row has evidence (file path/test/command output); integrity manifest + CI gate green.
**Acceptance:** AC-15 (integrity) infrastructure in place; reviewer can verify any audit claim by following listed paths.
**Risks/rollback:** low; docs only.

### Phase 2 — Market-data and ticker correctness
**Objective:** one trustworthy instrument/identity and provider layer.
**Behaviour:** §3.1–3.6 implemented; no blind `.NS`; ambiguity returns 409; provider 404 handled; data classes labelled; made-up data impossible in production.
**Inspect:** provider modules, ticker normalisation, cache, settings, existing endpoints used by Market Overview.
**Change (expected):** `marketdata/instruments.py` (master + resolver), `marketdata/providers/*` (interface, capabilities, adapters), `marketdata/errors.py`, `marketdata/validation.py`, seed data `configs/instruments/*.yaml`, API routers E1–E3, E20 (coverage), frontend API client types.
**Dependencies:** Phase 1.
**Tasks:** build instrument master + seed from permitted lists; resolver + probe + negative cache; capability map per provider; data-class logic; unified error schema + exception handlers; replace string-suffix logic; fixture-import ban; coverage endpoint.
**API:** E1, E2, E3, E20 (new); existing endpoints keep contracts, internally routed through resolver; error envelope added (backward-compat shim if clients depend on old shape — regression-tested).
**Tests:** §12.2 ticker/provider/validation items; recorded-fixture adapter tests; contract tests for E1–E3.
**Edge cases:** same ticker on NSE/BSE/ADR; renamed/delisted symbols; index symbols w/o volume; provider returns 200 with empty body; unicode names; very long queries.
**DoD:** resolver tests green; Yahoo-style 404 for an unsupported symbol yields `PROVIDER_SYMBOL_UNSUPPORTED` (UI-safe), not a crash; coverage numbers reported from data.
**Acceptance:** AC-11, AC-12 (partial), AC-13 (partial).
**Risks/rollback:** changing normalisation may break saved symbols → migration map + feature flag `resolver_v2`; rollback by flag.

### Phase 3 — Provider resilience and error handling (data + LLM)
**Objective:** bounded, classified, observable failures; actionable errors.
**Behaviour:** §3.4, §3.5, §3.7. Gemini 503 retried ≤2 then fallback; invalid model name fails fast at startup/health; quota handled; no infinite retries.
**Inspect:** LLM client modules, config, retry code, `/health`, frontend error handling.
**Change:** `providers/llm/*` (error mapping, circuit breaker, router, capability probe), `providers/retry.py`, `api/health`, frontend error components.
**Dependencies:** Phase 2 (error envelope).
**Tasks:** implement error classifier; probe on startup; fallback chain from validated config; structured partial results; metrics (attempts, breaker state); UI error mapping.
**API:** E20 extended; error codes for LLM; no key exposure.
**Tests:** fake-clock retry/backoff bounds; breaker transitions; 404-model permanent path; 429 behaviour; fallback only to configured providers; log redaction.
**Edge cases:** all providers down; fallback provider lacks vision; quota resets; clock skew.
**DoD:** chaos test suite passes; `/health` shows actionable misconfiguration text; no retry storm under load test (bounded attempts asserted).
**Acceptance:** AC-12, AC-10 (partial), AC-14.
**Risks/rollback:** over-aggressive failing fast could disable working providers → probe is advisory with override flag; rollback via config.

### Phase 4 — Historical range and interval support
**Objective:** real data for every range/interval; correct aggregation; navigation support.
**Behaviour:** §4 entirely; E4 live; range buttons produce real requests.
**Inspect:** existing history endpoint(s), caching, calendar utilities.
**Change:** `marketdata/ranges.py`, `calendars.py`, `aggregation.py`, E4 router, cache keys, `capabilities` encoding of provider limits, optional `archive/` job (self-archive) [PLANNED].
**Dependencies:** Phase 2, 3.
**Tasks:** range resolver; custom range validation + snapping; pagination (`before`); aggregation engine; calendar integration (NSE/NYSE); adjustments flag; limits table; quality & gap report; self-archive job design stub (flagged).
**API:** E4 (new or extension of existing OHLCV route), E7.
**Tests:** §12.2 aggregation & calendar; range matrix (every preset × interval) against fixtures; DST; bars-budget truncation; derived vs native daily reconciliation; provider-limit refusal with suggestions.
**Edge cases:** holiday as `end`; custom range entirely on holidays; IPO younger than range; intraday request beyond lookback; partial last bucket; provider timestamps at bar close.
**DoD:** table-driven test proves each preset returns a different, correctly bounded window; unsupported combos return 422 with suggestions.
**Acceptance:** AC-01, AC-02, AC-05 (data side).
**Risks/rollback:** cache key changes; version cache namespace (`ohlcv:v2`).

### Phase 5 — Charting engine and chart-type controls
**Objective:** responsive chart workspace shell with all chart types and navigation.
**Behaviour:** §5.1–5.3, 5.6–5.7.
**Inspect:** Market Overview, chart components, state management, styling tokens, API client.
**Change:** `frontend/src/features/chart/*` (`ChartEngine` adapter, `ChartWorkspace`, toolbar components, hooks `useOhlcv`, `useVisibleRange`), ADR, feature flag, tests.
**Dependencies:** Phase 4 schema merged (can start spike earlier).
**Tasks:** run spike + ADR; adapter; range/interval/type controls wired to E4; HA transform; volume pane; crosshair/legend/tooltip; loading/empty/error/stale states; pagination on pan; prev/next/latest; live last-bar updates; keyboard shortcuts base.
**API/schema:** consumes E3/E4.
**Tests:** §12.1 range/interval/type/states/navigation; performance trace recorded.
**Edge cases:** fast toggling; zero candles; single candle; huge gap; instrument without volume; theme switch; window resize.
**DoD:** all controls functional; old chart reachable via flag; perf budgets met or ADR records exceptions.
**Acceptance:** AC-01, AC-02, AC-03, AC-13.
**Risks/rollback:** bundle growth/licence → ADR gate; rollback = flag off.

### Phase 6 — Technical indicator framework
**Objective:** one indicator implementation serving chart, patterns, analysis and ML; indicator UI.
**Behaviour:** §6 (incl. intraday levels) and §5.4.
**Inspect:** existing indicator code, feature registry, ML feature builders.
**Change:** `technical/indicators/*`, `technical/levels.py`, E5/E6 routers, frontend indicator menu/legend/panes, parity tests.
**Dependencies:** Phase 4/5.
**Tasks:** implement catalogue with metadata and param validation; warm-up padding; golden fixtures; truncation tests; frontend integration; persistence; limits; ensure ML feature code reuses these functions (or proves parity) **without changing frozen `1.0.0` feature behaviour** (adapter tests with the old outputs).
**Tests:** §6.4 + frontend indicator tests.
**Edge cases:** constant series, zero volume, NaN gaps, very short history, high parameter values, Supertrend start-dependence.
**DoD:** every indicator verified against reference within tolerance; Supertrend either verified or hidden; alignment test passes.
**Acceptance:** AC-04, AC-05.
**Risks/rollback:** altering shared feature code could change model inputs → parity snapshot test; rollback to old functions via import shim.

### Phase 7 — Candlestick and chart-pattern engines
**Objective:** audited, deterministic, tested pattern detection with honest evidence levels.
**Behaviour:** §7.
**Inspect:** existing pattern modules and tests (and what prompts claim).
**Change:** `patterns/candlestick/*`, `patterns/chart/*`, `patterns/evidence.py`, configs, overlays in frontend, tests.
**Dependencies:** Phase 6 (ATR, context).
**Tasks:** audit table; implement/repair patterns incl. Harami & Hanging Man; pivots with `confirmed_at`; chart patterns; confidence decomposition; evidence-level computation on training data; API integration (patterns in E8); chart overlays layer "Computed".
**Tests:** §7.4/7.6; null-data false-positive rates logged; truncation invariance.
**Edge cases:** gaps/session boundaries; incomplete bars; very volatile bars; conflicting patterns.
**DoD:** every claimed pattern has fixtures+tests; unsupported claims removed from docs/UI; conflict reporting implemented.
**Acceptance:** AC-08, AC-05.
**Risks/rollback:** false positives → thresholds in config; patterns flag-gated until evidence tables exist.

### Phase 8 — Data-driven chart analysis
**Objective:** analysis of the selected instrument/timeframe/window from real OHLCV, no screenshot needed.
**Behaviour:** §9.1, §9.5, §8.6; screenshot path separated per §9.8.
**Inspect:** `/api/ai/analyze`, current chart-vision route/UI, news retrieval, explainability modules.
**Change:** `research/chart_analysis.py`, E8 router, frontend AI Analysis panel, vision output schema tweaks + regression tests.
**Dependencies:** Phases 4, 6, 7; news pipeline (baseline §6) as available.
**Tasks:** orchestrator; FeatureSnapshot; sections_status; narration guard; symbol/interval honouring tests; vision separation (`Unavailable/Unclear`, image-vs-data panels); "Compare with data" action.
**Tests:** analysis uses requested series (assert `series_id`); no fallback; news cutoff; vision hallucination set; upload security regression.
**Edge cases:** news unavailable; patterns unavailable; stale data; market closed; mismatch between image-reported and supplied ticker.
**DoD:** analysis works without any upload; failure modes explicit.
**Acceptance:** AC-06, AC-09, AC-11, AC-12.
**Risks/rollback:** LLM narration drift → template fallback; flag `analysis_v2`.

### Phase 9 — Forecasting and feature fusion
**Objective:** horizon-explicit, validated-only forecasts with uncertainty; auditable fusion; evaluation evidence.
**Behaviour:** §9.2–9.7, §12.3–12.4.
**Inspect:** model registry, `1.0.0` loader, evaluation scripts, calibration code, prospective monitor.
**Change:** `models/targets/*` (intraday + triple-barrier), `models/fusion/*`, registry eligibility lookup, OOD scorer, E10, `experiments/` configs/reports; **no change to `1.0.0` artefacts**.
**Dependencies:** Phases 6–8, baseline §7 leakage suite.
**Tasks:** target builders; day-blocked walk-forward; train T/P/N/C candidates as *new versions*; calibration; OOD; registry tiers; forecast object; leakage CI gate; ablations; regime reports; cost-aware expectancy; honest reporting incl. negative results.
**Tests:** §12.3 gate; schema; eligibility (no model ⇒ unavailable); probability exposure rule; snapshot reproducibility.
**Edge cases:** short histories; new IPOs; class imbalance; regime shift; missing feature groups; models trained only on India applied to US (blocked).
**DoD:** reports generated; leakage suite green; any candidate promoted only per §9.6; `1.0.0` hashes unchanged.
**Acceptance:** AC-07, AC-09, AC-15.
**Risks/rollback:** poor validation ⇒ forecasts remain `unavailable` (acceptable and honest); rollback = registry alias.

### Phase 10 — General-purpose AI Research Assistant
**Objective:** answer the question asked; robust to provider failures; correct rendering.
**Behaviour:** §10.
**Inspect:** form, payload, route, schema, prompts, cache, parser, renderer (H1–H9).
**Change:** `research/assistant/{planner,tools,composer,validators,sessions}.py`, E11, frontend Research page/panel + markdown renderer, tests.
**Dependencies:** Phase 3 (resilience), Phase 2 (resolver); tools degrade if Phases 8–11 aren't done.
**Tasks:** fix each confirmed hypothesis; implement architecture; query echo; sessions; sanitised rendering; parsing; test matrix; anti-canned test; cache key includes normalised query + entities + as_of bucket.
**Tests:** §10.9 (17 cases), injection suite, renderer tests.
**Edge cases:** ambiguous entities; unsupported question types; multi-entity comparisons; long answers; session expiry; provider outage mid-answer.
**DoD:** 17-case suite green; manual run of ≥10 novel queries recorded in evidence file; no identical canned output.
**Acceptance:** AC-10, AC-11, AC-12.
**Risks/rollback:** flag `research_v2`; keep old route until acceptance.

### Phase 11 — Trader toolkit I: market context, fundamentals, scanner
**Objective:** pre-market and selection tools.
**Behaviour:** §11.2–11.4.
**Inspect:** index data availability, fundamentals sources/terms, constituents lists, event calendars.
**Change:** `trader/context.py`, `fundamentals/*`, `trader/scanner.py`, E12–E14, frontend panels, config for sources.
**Dependencies:** Phases 2, 3, 4, 6 (levels).
**Tasks:** verify sources (log in `docs/provider_verification.md`); context card; day-type labels; fundamentals schema+scoring with unavailable handling; scanner engine w/ filters & budgets; as-of reruns.
**Tests:** deterministic scans on fixtures; fundamentals unit/currency tests; point-in-time (`filed_at`); budget/cancel; no ToS-violating scraping (review checklist).
**Edge cases:** missing constituents → breadth unavailable; stale FII/DII; results-day stocks; illiquid names.
**DoD:** every field either sourced with timestamp or explicitly `unavailable`.
**Acceptance:** AC-16, AC-12.
**Risks/rollback:** data-source loss → modules degrade; flag `trader_toolkit`.

### Phase 12 — Trader toolkit II: scenario plan, risk/costs, journal/paper, watchlist/alerts
**Objective:** risk-defined planning and honest self-measurement.
**Behaviour:** §2.5, §11.5–11.8.
**Inspect:** user-data/auth architecture (Q3), notification support.
**Change:** `trader/{plan,costs,risk,paper,journal,alerts,watchlists}.py`, configs/costs, E15–E18, frontend views.
**Dependencies:** Phases 6, 7, 11 (and 9 for forecast context).
**Tasks:** cost config + verification log; calculators; plan engine + checklist; paper engine; journal + revisions + analytics; watchlists; alerts; local/server storage; export/delete.
**Tests:** cost arithmetic fixtures; sizing; breakeven formula; paper fills conservative rules; revision history immutability; discipline metrics; alerts on completed bars; UI flows.
**Edge cases:** lot sizes, price tick rounding, stop beyond liquidity, gaps through stops, zero/negative inputs, currency mixing.
**DoD:** plan refuses when invalidation missing/data stale; no wording violations (language linter).
**Acceptance:** AC-17, AC-18.
**Risks/rollback:** misleading precision → "Estimate" labels; flag.

### Phase 13 — Setup lab and prospective intraday ledger
**Objective:** evidence-based setup scorecards; tamper-evident forward record.
**Behaviour:** §11.9–11.10.
**Inspect:** available intraday history (Phase 4 limits/self-archive), existing prospective monitor.
**Change:** `research/setups/*`, `research/backtest/intraday.py`, `experiments/configs/setups/*`, ledger module + scheduled job, E19, frontend scorecards.
**Dependencies:** Phases 6, 7, 12.
**Tasks:** DSL + parser (safe: no `eval`); engine; pre-registered configs; walk-forward; controls; scorecards; ledger hash chain + verifier + scheduler; documentation of limits.
**Tests:** lookahead-injection test; fill rules; cost sensitivity; random control; hash-chain tamper test; scheduler idempotency.
**Edge cases:** insufficient history ⇒ `cannot_evaluate`; sparse volume; split days.
**DoD:** at least the 8 setups evaluated or marked `cannot_evaluate` with reasons; ledger running with no manual write path.
**Acceptance:** AC-19, AC-15.
**Risks/rollback:** data scarcity; honest "cannot evaluate" is acceptable.

### Phase 14 — UI polish, responsive behaviour, accessibility
**Objective:** coherent professional UX across devices.
**Behaviour:** §5.6, §6 of the brief.
**Change:** layout, theming, mobile bottom sheets, keyboard shortcuts, aria-live, "view as table", copy.
**Dependencies:** Phases 5–13.
**Tasks:** responsive audit; a11y fixes; consistent empty/error states; remove dead controls; verify **every control changes data or rendering**; language-policy sweep (forbidden phrases) across UI strings.
**Tests:** §12.1 responsive/a11y/visual regression; Playwright full-journey scripts.
**DoD:** axe clean (serious/critical = 0); keyboard-only journey passes; Lighthouse a11y score recorded.
**Acceptance:** AC-13, AC-20.
**Risks/rollback:** visual regressions → snapshot review.

### Phase 15 — Regression, quantitative evaluation, security
**Objective:** prove nothing broke and claims are supported.
**Behaviour:** §12, §14.
**Tasks:** API regression snapshots vs `openapi_before.json`; full leakage and evaluation runs; security review (secrets scan, prompt-injection suite, upload suite, dependency/licence audit, CORS/rate limits); performance/load smoke; integrity verification.
**DoD:** all gates green; reports in `experiments/reports/`; licence inventory complete.
**Acceptance:** AC-14, AC-15, AC-21.
**Risks/rollback:** failures block release; fix before Phase 16.

### Phase 16 — Documentation, deployment, final acceptance
**Objective:** reproducible deploy and signed-off acceptance.
**Tasks:** update docs (architecture, API, data-source limitations, provider verification log, model cards, benchmark-claims status, user guide with risk education); deploy to configured free tier; smoke tests; rollback drill; final acceptance run mapping each AC to evidence; update `docs/FINAL_ACCEPTANCE_AUDIT.md` **by appending a dated section** (do not rewrite history).
**DoD:** every AC in §15.2 checked with evidence links; known-limitations page published.
**Acceptance:** all.
**Risks/rollback:** free-tier cold starts/limits documented; rollback by previous release tag and flags.

---

## 14. Security, Integrity and Compliance

### 14.1 Security
Credentials only in environment variables/secret stores (never in repo, frontend bundles, logs, prompts or responses); `.env.example` has names only; gitleaks in CI. CORS allow-list; rate limits per §8.2; request size limits; input validation on all fields (Pydantic, regexes, enums); output validation (schema, forbidden-phrase linter, URL/ID validators, canary tokens); no `eval`/`exec` on user or LLM text (the setup DSL uses a safe expression parser with an allow-listed function set); SSRF protection (no arbitrary URL fetching; news fetch only from allow-listed domains); dependency audit (`pip-audit`, `npm audit`), licence inventory for every new package (**charting, TA, markdown**), pinned versions. Journal/watchlists/drawings: per-user isolation, size caps, XSS-safe rendering, export/delete. Optional broker-data adapter: read-only allow-list, no order/funds/portfolio endpoints importable (test enforces).
### 14.2 Prompt-injection and untrusted content
Retrieved news, filings text, user questions, image text and journal notes are **untrusted data** everywhere they are passed to an LLM: delimiter isolation with per-request nonces, sanitisation, instruction hierarchy, no tools exposed to analysis LLMs, output validators, injection corpora in tests (baseline §13). Research planner receives the raw question as data inside a delimited field.
### 14.3 Upload security
Unchanged baseline §45 controls (allow-listed types, magic bytes, size, dimensions, re-encode, no execution, random temp names, auto-delete). Journal attachments reuse the same pipeline. Regression tests ensure no weakening.
### 14.4 Model, metric and ledger integrity
- Frozen model `1.0.0`, historical metrics, snapshots and prospective ledger files are **read-only**: SHA-256 manifest from Phase 1; CI verifies on every PR; code review rule: no write path to those locations.
- New models are new versions; registry never overwrites an artefact (content-addressed storage).
- New prospective ledger is append-only with hash chain (§11.10).
- No manufacturing or back-dating of prospective observations; no editing of `FINAL_ACCEPTANCE_AUDIT.md` history (append only).
- Experiment logs record every run; selective reporting is prohibited.
### 14.5 Legal/compliance posture
Research/education tool; not investment advice; display disclaimer on analysis, plan, scanner and research screens; do not present as SEBI/other regulator-registered advisory unless the owner obtains registration (**flag to project owner: regulatory status of publishing buy/sell-style research in India should be reviewed with a qualified professional**; this spec avoids recommendations by design). Respect data-provider and news ToS; storage/redistribution limits; attribution where required (chart library, data sources). Do not claim exchange-official data unless licensed.

---

## 15. Requirements Traceability and Acceptance

### 15.1 Traceability matrix (every requirement in the brief → phase, tests, acceptance)

| Brief § | Requirement | Phase(s) | Key tests | AC |
|---|---|---|---|---|
| 1 | Preliminary audit (read baseline, inspect FE/BE/tests, classify, baseline-audit section) | 1 | audit reproducibility; integrity verifier | AC-15, AC-22 |
| 2.1 | Ranges 1D–MAX + custom; real fetch; prev/next/latest; zoom/pan/crosshair; holidays/gaps/limits | 4, 5 | range matrix; selector network assertions; pagination; calendar | AC-01 |
| 2.2 | Intervals 1m–1M per provider capability; aggregation rules; session/timezone; intraday limits & providers | 4 | capability matrix; aggregation suite; DST; limit refusals | AC-02 |
| 2.3 | Chart types incl. correct HA; volume panel; legends/tooltips/states; library evaluation/migration | 5 | chart-type tests; HA unit; ADR; perf trace | AC-03 |
| 2.4 | Indicator selector, params, multi-indicator, defaults/warm-up/panels; no look-ahead; same candle series | 6 | golden fixtures; truncation; alignment; UI tests | AC-04, AC-05 |
| 2.5 | Drawing tools + scoping + safe persistence; no brokerage | 5 | drawing tests; allow-list test | AC-04 |
| 3.1 | Data-driven analysis on selected ticker/timeframe/window; no silent fallback | 8 | series_id honoured; no-substitution test | AC-06 |
| 3.2 | Candlestick audit, definitions, tests, conflict reporting | 7 | §7.4 suite | AC-08 |
| 3.3 | Chart-pattern audit, algorithms, confirmation/invalidation, calibration; no LLM guesses | 7 | synthetic/null/truncation tests | AC-08 |
| 3.4 | Forecast outputs: horizons, targets, timestamps, model meta, uncertainty, OOD, no unsupported prices; classification vs return separated; unvalidated ⇒ explicit | 9 | schema; eligibility; probability-exposure; OOD | AC-07 |
| 3.5 | Auditable fusion; point-in-time news; publication vs ingestion time; logged sources/versions; model comparison/ablation/calibration/CIs; LLM boundary | 9 | leakage suite; FeatureSnapshot repro; ablation reports; narration guard | AC-09, AC-07 |
| 3.6 | Screenshot Chart Vision separate; Unavailable/Unclear; no pixel prices; security retained | 8 | vision hallucination; upload matrix | AC-06, AC-21 |
| 4 (1–14) | Research Assistant: preserve query, no templates, resolve entity, tools, unverifiable facts stated, adaptive structure, follow-ups, sources, rendering, parsing robustness, statuses, no fabrication, no false browsing claim | 10 (+3, 2) | §10.9 17-case suite; anti-canned; renderer; injection | AC-10, AC-11 |
| 5 | Unified market-data layer; canonical tickers; sessions; freshness; data classes; no mock data in prod; LLM provider rules | 2, 3 | resolver; provider chaos; fixture ban; retry bounds | AC-11, AC-12 |
| 6 | Angel One-inspired workspace functions; branding; a11y; mobile; all controls functional | 5, 14 | responsive/a11y/e2e; dead-control audit | AC-13, AC-20 |
| 7 | Smallest safe API extensions with full contracts | 2–13 | contract tests; OpenAPI diff | AC-14 |
| 8 | FE/BE/quant/integrity/security verification | 15 (+ all) | §12 | AC-14, AC-15, AC-21 |
| 9 | Staged plan with per-phase fields; independent testability; evidence; traceability | all | evidence files | AC-22 |
| 10 (1–15) | Final acceptance items | 16 | see 15.2 | AC-01…AC-15 |
| 11 | Output file only; reference baseline; audit findings; facts vs assumptions | this doc | sha256 of baseline unchanged | AC-22 |
| Added (trader) | Intraday levels, market context, fundamentals, scanner, plan, costs, journal/paper, alerts, setup lab, ledger | 6, 11, 12, 13 | §11 tests | AC-16…AC-19 |

### 15.2 Acceptance catalogue (all require evidence links in `docs/evidence/`)

| ID | Criterion |
|---|---|
| AC-01 | Users navigate recent and historical charts across all presets and custom ranges; each triggers real data requests and changes displayed data |
| AC-02 | Users choose supported 1m–30m, 1h, 4h, daily, weekly, monthly intervals; unsupported combinations disabled with explanation and API 422 |
| AC-03 | Line, area, OHLC, candlestick (and verified Heikin-Ashi) switch correctly; candle mode uses actual OHLC; volume panel synchronised |
| AC-04 | Multiple indicators can be added, configured, hidden and removed; drawings (horizontal, vertical, trend, text, clear) work with correct scoping |
| AC-05 | Chart candles, indicators and pattern detection use identical timestamps and the same series (`series_id`); no look-ahead (tests) |
| AC-06 | Actual OHLCV can be analysed without a screenshot; selected instrument/interval/window honoured with no silent fallback; screenshot analysis remains separate |
| AC-07 | Forecasts carry horizon, target definition, timestamps, model metadata, uncertainty, OOD/validation warnings; probabilities only when calibrated; no unsupported price targets |
| AC-08 | Candlestick and chart patterns are deterministic, unit-tested, evidence-labelled and not LLM-dependent |
| AC-09 | News enters features/analyses only when timestamps meet the as-of rules; publication vs ingestion time recorded |
| AC-10 | Research Assistant answers substantially different queries by addressing the question asked; follow-ups keep entity context safely |
| AC-11 | No fabricated prices, figures, citations or news; "browsing" never claimed without retrieval evidence |
| AC-12 | Missing data and provider/LLM outages are communicated with codes and `ok/degraded/unavailable` statuses |
| AC-13 | All controls function; error states never crash the UI |
| AC-14 | Backend tests, frontend tests, lint, type-check and production builds pass; API regression tests pass |
| AC-15 | Frozen `1.0.0`, historical metrics, snapshots and prospective ledgers byte-identical to the Phase 1 manifest; no manufactured observations |
| AC-16 | Market-context, fundamentals and scanner outputs are sourced and timestamped or explicitly unavailable; no ToS-violating scraping |
| AC-17 | Scenario plans always include trigger, invalidation, costs, breakeven probability, sizing, checklist; "no trade" verdict supported; no recommendation language |
| AC-18 | Paper trading and journal use conservative fills, revision history and computed analytics with sample-size guards |
| AC-19 | Setup scorecards report net-of-cost evidence tiers with CIs and controls (or `cannot_evaluate`); prospective ledger is append-only and verifiable |
| AC-20 | WCAG 2.1 AA checks pass for core flows; mobile layouts verified |
| AC-21 | Security gates pass (secrets scan, injection suite, upload suite, dependency/licence audit) |
| AC-22 | Baseline audit and spec distinguish confirmed facts, assumptions, unresolved questions; baseline file `AIplannedcld.md` unchanged |
Dependencies on paid/unavailable providers, credentials or data must be recorded in `docs/provider_verification.md`, with a **testable degraded mode** (the corresponding feature returns `unavailable` with reason and tests prove it).

---

## Appendix A — Risk Register (top items)

| Risk | Impact | Mitigation |
|---|---|---|
| Free providers lack deep intraday history or change behaviour | Charts/backtests limited | Capability-driven UI, self-archive, optional licensed feed, explicit limits |
| Unofficial provider breakage/ToS | Outages/legal | Adapter isolation, schema-change alarms, fallback, legal review |
| Overfitting/leakage produce false confidence | Misleading users | Leakage CI gate, too-good alarm, pre-registration, untouched test, honest reports |
| Users over-trust AI/pattern signals | Financial harm | Calibration gating, evidence tiers, conflict display, disclaimers, no recommendations |
| Costs dominate small-edge intraday setups | Perceived "no edge" | Show cost drag & breakeven p*; honest scorecards |
| LLM quota/model churn | Research Assistant outages | Validated config, fallback chain, deterministic degraded reports |
| Chart library licence/size | Rework | ADR + spike before migration; adapter isolation |
| Scope creep into brokerage features | Compliance risk | Allow-list tests, explicit non-goals |
| Regulatory status of research content (India) | Legal | Owner to seek professional advice; avoid recommendations |

## Appendix B — Open Questions to Resolve Early
See §1.7 (Q1–Q9). Additionally: (B1) Does the project own/plan a licensed real-time feed? (B2) Is user authentication planned (affects journal/watchlist storage)? (B3) Target markets for launch (India-first vs US)? (B4) Maximum acceptable free-tier infrastructure footprint (RAM/CPU) for server-side indicators and scanners?

## Appendix C — Instruction Block for the Coding Agent
1. Read `AIplannedcld.md` and this file fully. Do not modify `AIplannedcld.md`.
2. Execute Phase 1 and publish the audit **before** writing feature code; update the *Files* lists in this document's phases with real paths (append an "Audit-resolved paths" section; do not delete original text).
3. Work phase by phase; do not start a phase until its dependencies' Definition of Done is evidenced.
4. Never fabricate data, results, citations, rates or capabilities; mark unverified items `[VERIFY]` and log the check.
5. Use the language policy in baseline §1.3 and §2.3 here; no recommendations, no guarantees.
6. Preserve frozen artefacts and prospective records; fail the build if their hashes change.
7. When a requirement cannot be met with available free data, implement the degraded mode, document the limitation, and report it — do not weaken the requirement silently.

*End of AIplannedcld2.md*
