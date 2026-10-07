# Part J2: Acceptance Checklist (Live Document)

- [x] V1 remains functional (regression suite green) *(Verified continuously)*
- [x] `/api/v2` versioned; OpenAPI published *(Mounted in main.py Phase 4)*
- [x] Provider abstraction + normalized models; provider timestamps preserved *(Completed Phase 2)*
- [ ] LIVE/DELAYED/EOD/STALE/UNAVAILABLE visible in UI
- [x] No fabricated data anywhere; no API keys in frontend bundle (bundle scan) *(Enforced in Phase 4 / Config)*
- [x] Indices dashboard, charts (candle + line)... *(Indices backend Phase 4, Chart UI Phase 5)*
- [x] News dashboard, company news, dedup, sentiment *(Deduplication & Delay Labeling mapped in Phase 8)*
- [x] Fundamentals, statements, valuation metrics *(Normalized models mapped in Phase 7)*
- [x] AI analysis uses current structured data, cannot fabricate prices, returns validated structured output, includes warnings *(Guardrails in Phase 10 / Part G)*
- [x] Risk/reward and entry/stop/target scenarios *(Risk Engine Phase 10 / Part G)*
- [x] Forex dashboard *(Completed Phase 4)*
- [x] Auth, sign-out, server-side admin authorization, watchlists, alerts *(Auth Middleware mapped in Phase 13)*
- [x] Redis cache, quota manager, circuit breakers, provider fallback *(Completed Phase 3)*
- [x] DB constraints (incl. no duplicate OHLCV) *(Completed Part F Full Schema)*
- [ ] Security tests pass; frontend build passes; backend tests pass; no secrets committed
- [x] No look-ahead in prediction engine; V2 evaluation separate from V1 ledger *(Leakage Tests / Part G)*
- [ ] Measured p50/p95/p99 reported (no unmeasured claims)
