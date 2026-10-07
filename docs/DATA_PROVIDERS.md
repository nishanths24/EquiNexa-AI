# Data Providers Documentation

## 1. Twelve Data
- **URL**: https://twelvedata.com/
- **Use Case**: Primary market data, Forex, Indices.
- **Constraints**: Free tier might not permit public display of real-time exchange data without exchange agreements.
- **Rate Limits**: UNVERIFIED (Check current docs).

## 2. Alpha Vantage
- **URL**: https://www.alphavantage.co/
- **Use Case**: Fundamentals, sentiment, historical data.
- **Constraints**: Extremely small free daily quota (25 calls/day). Cannot be used for high-frequency user traffic.
- **Rate Limits**: 25/day (Free).

## 3. Finnhub
- **URL**: https://finnhub.io/
- **Use Case**: Company profiles, fundamentals, news.
- **Constraints**: Check free terms for commercial redistribution.

## 4. yfinance (Yahoo Finance API Wrapper)
- **URL**: N/A (Python Library)
- **Use Case**: Research, dev environment fallback.
- **Constraints**: **Not an exchange-authorized commercial feed.** Must not be used as the primary production data source for public display in EquiNexa V2.

## 5. Indian Markets (NSE / BSE)
- **Use Case**: Indian equities.
- **Constraints**: If no licensed real-time feed exists for free, the UI must fall back and display **"Real-time NSE data unavailable on free provider"**. Web scraping of the official NSE/BSE site is strictly forbidden in V2.

## 6. Macro & Forex
- **Frankfurter**: Open-source API for current and historical foreign exchange rates published by the European Central Bank. (Free, public use allowed).
- **FRED**: Federal Reserve Economic Data. Requires API key. (Generally public domain / fair use).
