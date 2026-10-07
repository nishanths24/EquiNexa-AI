# Observability & Logging

## Structured Logging
All backend logs output as strict JSON lines. This ensures parsability by Datadog, AWS CloudWatch, or Grafana Loki.

Fields logged include:
- `timestamp` (ISO-8601 UTC)
- `level`
- `message`
- `request_id`
- `endpoint`
- `provider`
- `error_code`
- `latency_ms`

## Metrics Tracking
- **Latency**: Provider latency, AI generation latency, and backend API latency are tracked to report true p50/p95/p99 values.
- **Cache Hit Ratio**: Redis metrics are exposed for admin dashboards.
