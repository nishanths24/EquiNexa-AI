# Data Provider Matrix

| Provider | Asset | Market | Realtime | Delayed | Historical | Fundamentals | News | WebSocket | Free Limit | Public Display | Commercial Use | Fallback | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Twelve Data** | Equities/FX/Crypto | Global | Yes (FX/Crypto) | Yes (Equities) | Yes | No | No | Yes | 800/day | No (check terms) | Paid | Alpha Vantage | Primary data provider |
| **Alpha Vantage** | Equities/FX | US/Global | No | Yes | Yes | Yes | Yes | No | 25/day | No (check terms) | Paid | Finnhub | Small free quota |
| **Finnhub** | Equities | US | Yes | Yes | Yes | Yes | Yes | Yes | 60/min | No (check terms) | Paid | None | Good for company profiles |
| **yfinance** | Equities | Global | No | Yes | Yes | Basic | No | No | N/A | No | No | Yes | Dev/Fallback only |
| **NSE** | Equities | India | No | Yes (EOD) | No | No | No | No | N/A | No | No | No | No scraping allowed |
| **BSE** | Equities | India | No | Yes (EOD) | No | No | No | No | N/A | No | No | No | No scraping allowed |
| **Supabase** | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Yes | 50k MAU | Yes | Yes | N/A | Auth / Postgres backend |
| **Upstash** | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | 10k/day | Yes | Yes | N/A | Redis caching layer |
| **NewsData** | News | Global | No | Yes | Yes | No | Yes | No | 200/day | Yes (with attrib) | Paid | Yes | Global news fallback |
| **Currents** | News | Global | No | Yes | Yes | No | Yes | No | 600/day | Yes (with attrib) | Paid | Yes | High-frequency news |
| **GNews** | News | Global | No | Yes | Yes | No | Yes | No | 100/day | Yes (with attrib) | Paid | Yes | Broad tech/market news |
| **FRED** | Macro | US | No | Yes | Yes | No | No | No | 120/min | Yes | Yes | Yes | US Economic yields |
| **Frankfurter** | FX | Global | No | Yes | Yes | No | No | No | Unlimited | Yes | Yes | Yes | ECB daily reference rates |

*Verified On: 2026-10-08*
