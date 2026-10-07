# V2 Architecture Overview

## Layering & Stack
- **Frontend:** React (Vite/TS/Tailwind), Lightweight Charts for rendering, Web Workers for heavy client-side computation.
- **Backend:** FastAPI (async Python).
- **Service Layer:** Modules mapped directly to business domains (Market, News, Fundamentals, Macro, Forex, Analysis, Alerts, Prediction, Risk).
- **Provider Layer:** Deterministic `ProviderManager` wrapping multiple adapters (TwelveData, Alpha Vantage, etc.) via Circuit Breakers and Quota Managers.
- **Caching & Event Bus:** Upstash Redis (Phase 3 in-memory coalescing).
- **Persistence:** PostgreSQL / Supabase, specifically designed for TimescaleDB migration (hypertable-ready).

## Core Principles
1. **Never mutate V1:** The V1 endpoints, UI, and ledger are strictly frozen. V2 is an additive evolution.
2. **Deterministic Failover:** When a primary provider rate-limits or fails, the `ProviderManager` strictly falls back down the chain before gracefully rejecting the request as `UNAVAILABLE`.
3. **Data Integrity First:** No synthetic data is generated. All responses contain a strict `meta` block describing provenance, latency, and cache age.
