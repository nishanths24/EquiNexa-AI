# V2 Data Stack & Provider Matrix

## Recommended V2 Architecture & Data Stack

| Requirement | V2 Choice | Role |
| :--- | :--- | :--- |
| **Market data** | **Twelve Data** | Primary provider where its actual plan/display rights permit |
| **Market/fundamental/news fallback** | **Finnhub** | Secondary provider |
| **Historical/technical fallback** | **Alpha Vantage** | Secondary |
| **Research/backfill** | **yfinance** | Development/research only, not core public feed |
| **Global news** | **GDELT / permitted feeds** | Broad news ingestion |
| **News development** | **NewsAPI** | Secondary; free tier is delayed/limited |
| **Macro** | **FRED** | US economic data |
| **FX reference** | **Frankfurter** | Free reference FX data |
| **Database** | **Supabase Postgres** | Users, fundamentals, candles, news, predictions |
| **Cache** | **Upstash Redis** | Quotes, candles, news, AI/cache/rate limiting |
| **Backend** | **FastAPI async** | V2 API |
| **Frontend** | **React + TypeScript** | Trading terminal |
| **Charts** | **Lightweight Charts** | Candlestick/line/technical visualization |
| **AI** | **Gemini abstraction** | Reasoning/explanation layer |
| **Future streaming** | **Kafka/Redpanda** | Only when scale justifies it (Interfaces built now) |
| **Future stream analytics**| **Flink** | Later |
| **Future analytics DB** | **ClickHouse/TimescaleDB** | Later |
| **Future low latency** | **Go/Rust** | Later, selected hot paths |

---

## Architectural Directives & Compliance

1. **Defer Complex Streaming**: Kafka, Flink, TimescaleDB, ClickHouse, and Go/Rust have **NOT** been deployed. Deploying them on a free-tier project makes it harder to operate without bringing immediate latency benefits. The V2 production path is strictly executed via **FastAPI + async workers + Upstash Redis + Supabase Postgres**. The interfaces (e.g. `EventBus`) have been designed so they can be seamlessly swapped to Kafka later when scale justifies it.
2. **NSE/BSE Scraping Restriction**: EquiNexa AI honors the NSE data-sharing policy. NSE/BSE scraping is strictly avoided. Real-time Indian exchange data is only queried if an authorized provider tier is active; otherwise, it gracefully falls back to authorized delayed/EOD data.
3. **Database Boundaries**: Supabase is configured as the V2 core database (within the 500MB / 50,000 MAU free tier), tracking users, fundamentals, and V2 predictions.
4. **Cache & Rate Limiting**: Upstash Redis acts as the primary buffer, adhering strictly to the 256MB free allowance, coalescing concurrent requests so upstream providers (Twelve Data, Finnhub, FRED) are not flooded past their free quotas.
