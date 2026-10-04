# Provider Verification Log

| Data Requirement | Source / Library | Status | Terms of Service Checked | Notes |
|---|---|---|---|---|
| OHLCV / Market Data | `yfinance` / Yahoo Finance API | Verified | Yes | Permitted for individual/educational use. No real-time redistribution allowed. |
| Fundamentals (PE, Market Cap) | `yfinance` | Verified | Yes | Data is point-in-time or last quarter. Validated acceptable. |
| India Indexes (.NS) | `yfinance` | Verified | Yes | Symbols like `^NSEI` (Nifty 50) provide index breath proxies. |
| Options Data / FII-DII | Unavailable / Manual | Degraded | N/A | Scraping NSE/BSE directly violates ToS. We will mark these fields as "unavailable" and rely on OHLCV derivations. |
