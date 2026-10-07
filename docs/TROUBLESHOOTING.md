# Troubleshooting Guide

## Missing Market Data
- Check `ProviderManager` circuit breaker logs. If a provider is in `OPEN` state, rate limits or 500 errors were exceeded. The system will auto-fallback.
- Ensure API keys in `.env` (derived from `.env.example`) are valid.

## UI Data says "UNAVAILABLE"
- This is an intentional feature of Phase 4 and Part D capabilities. If a timeframe or region is not supported by the current active provider (e.g. NSE realtime on a free tier), it gracefully returns an unavailable state rather than fabricating data.

## Missing Charts
- Verify `FRONTEND_ORIGIN` in `.env` matches the port your Vite server is running on (e.g. `:5173`). Strict CORS prevents rendering on mismatched origins.
