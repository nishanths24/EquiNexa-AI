# EquiNexa AI - Known Limitations

## Data Sourcing
1. **Intraday Data Scarcity**: Access to historical 1-minute or 5-minute data is severely limited on the free tier (`yfinance`). Most tools degrade gracefully to End-of-Day (EOD) metrics if intraday data is unfetchable.
2. **Options and Derivatives**: Scraping direct FII/DII data or live option chains from exchange servers violates standard ToS. These datasets are currently unavailable; users must rely on price-action and OHLC derivations.
3. **Time Delays**: Market data is delayed up to 15 minutes unless an institutional API key is provided in the `.env`.

## Analytics and Forecasting
1. **OOD (Out-of-Distribution) Bounds**: The AI forecasting engines will strictly refuse to issue probability metrics on tickers outside of the Indian equity indices (.NS, .BO) to prevent systemic hallucinations.
2. **Setup Scanner Budget**: Scanner queries are intentionally hard-capped at 5 symbols per request. Do not attempt to run a full index scan on a single API call, as upstream rate-limiting will trigger.

## Deployment Limits
1. **Free-tier Cold Starts**: On free hosting tiers, the first API request of the day may take up to 30 seconds due to container cold starts.
2. **Memory Constraint**: Intensive candlestick pattern analysis limits history lookup to 3 months.
