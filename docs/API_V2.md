# API V2 Specification

## Core Endpoints
All endpoints return strict, Pydantic-validated JSON shapes.
`GET /api/v2/markets/overview` - Returns grouped quotes for global indices.
`GET /api/v2/markets/forex` - Returns major currency pairs.
`GET /api/v2/markets/macro` - Returns treasury yields and commodities.

*(Further endpoints to be mounted in subsequent phases)*:
- `/api/v2/quotes/{symbol}`
- `/api/v2/history/{symbol}`
- `/api/v2/fundamentals/{symbol}`
- `/api/v2/news`
- `/api/v2/analysis/{symbol}`

## Structured Error Handling
All API V2 errors return a standardized JSON schema mapped directly by the frontend to prevent bare "Failed to fetch" errors.
```json
{
  "status": "ERROR",
  "code": "PROVIDER_RATE_LIMIT",
  "message": "Market data provider rate limit reached.",
  "request_id": "req-12345"
}
```
