# Data Provider Matrix (Part K Specification)

| Provider | Asset | Market | Realtime | Delayed | Historical | Fundamentals | News | WebSocket | Free Limit | Public Display | Commercial Use | Fallback | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Twelve Data** | Equities/FX/Crypto | Global | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | Yes | Primary data provider |
| **Alpha Vantage** | Equities/FX | US/Global | No | Yes | Yes | Yes | Yes | No | 25/day | UNVERIFIED | UNVERIFIED | Yes | Small free quota |
| **Finnhub** | Equities | US | UNVERIFIED | UNVERIFIED | Yes | Yes | Yes | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | Yes | Good for company profiles |
| **yfinance** | Equities | Global | No | Yes | Yes | Basic | No | No | None | No | No | Yes | Dev/Fallback only |
| **NSE** | Equities | India | No | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | No | None | No | No | No | No scraping allowed |
| **BSE** | Equities | India | No | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | No | None | No | No | No | No scraping allowed |
| **Supabase** | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Yes | 50k MAU | Yes | Yes | N/A | Auth / Postgres backend |
| **Upstash** | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | 10k/day | Yes | Yes | N/A | Redis caching layer |
| **NewsData** | News | Global | No | Yes | Yes | No | Yes | No | UNVERIFIED | UNVERIFIED | UNVERIFIED | Yes | Global news fallback |
| **Currents** | News | Global | No | Yes | Yes | No | Yes | No | UNVERIFIED | UNVERIFIED | UNVERIFIED | Yes | High-frequency news |
| **GNews** | News | Global | No | Yes | Yes | No | Yes | No | UNVERIFIED | UNVERIFIED | UNVERIFIED | Yes | Broad tech/market news |
| **FRED** | Macro | US | No | Yes | Yes | No | No | No | UNVERIFIED | Yes | Yes | Yes | US Economic yields |
| **Frankfurter** | FX | Global | No | Yes | Yes | No | No | No | None | Yes | Yes | Yes | ECB daily reference rates |

*Verified On: 2026-10-07*
