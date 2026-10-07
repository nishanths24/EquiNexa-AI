# Deployment Strategy

## Infrastructure
- **Frontend**: Vercel (Deployed under `/v2` during staging to avoid V1 replacement).
- **Backend**: Render (FastAPI).

## Feature Flags
Controlled via `app.core.config.FeatureFlags`.
- Features like `V2_MARKET_DATA` and `V2_AI_ANALYSIS` default to `OFF` until production acceptance is formally met.

## Zero-Downtime Rollout
- V1 endpoints and UI are never replaced until V2 completely passes the acceptance matrix and staging checks.
- Docker, NGINX, Kafka, and ClickHouse are retained as architectural *designs* and will only be deployed when profiling metrics justify their operational overhead.
