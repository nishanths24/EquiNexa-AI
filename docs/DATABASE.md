# Database Architecture

## Technology
- **Supabase (PostgreSQL)**
- Designed for TimescaleDB migration (hypertable-ready) via time-partitioning on the `ohlcv` table.

## V1 Isolation
- V2 writes to entirely separate tables (e.g., `ai_predictions_v2`) to ensure V1 processes and analytical baselines remain unaffected.

## Key Constraints
- Strict `CHECK` constraints on `ohlcv` (e.g., `high >= GREATEST(open, close)`).
- Row Level Security (RLS) is explicitly enabled on all user-linked assets.
- Schema migrations are handled via strict `.sql` files (`V1__BaseSchema.sql`, `V2__FullSchema.sql`).
