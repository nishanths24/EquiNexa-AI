-- Phase 3 Base Schema (Postgres / Supabase)

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS exchanges (
    id SMALLSERIAL PRIMARY KEY,
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    timezone TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS instruments (
    id BIGSERIAL PRIMARY KEY,
    symbol TEXT NOT NULL,
    exchange_id SMALLINT REFERENCES exchanges(id),
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    UNIQUE(symbol, exchange_id)
);

CREATE TABLE IF NOT EXISTS ohlcv (
  instrument_id  BIGINT      NOT NULL REFERENCES instruments(id),
  exchange_id    SMALLINT    NOT NULL REFERENCES exchanges(id),
  timeframe      TEXT        NOT NULL CHECK (timeframe IN ('1m','3m','5m','15m','30m','1h','2h','4h','1D','1W','1M')),
  ts             TIMESTAMPTZ NOT NULL,
  open  NUMERIC(20,8) NOT NULL CHECK (open  > 0),
  high  NUMERIC(20,8) NOT NULL,
  low   NUMERIC(20,8) NOT NULL,
  close NUMERIC(20,8) NOT NULL CHECK (close > 0),
  volume NUMERIC(24,4) CHECK (volume >= 0),
  source   TEXT NOT NULL,
  quality  TEXT NOT NULL DEFAULT 'OK',
  ingested_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CHECK (high >= GREATEST(open, close) AND low <= LEAST(open, close)),
  UNIQUE (instrument_id, timeframe, ts, source)
);

CREATE INDEX IF NOT EXISTS idx_ohlcv_time ON ohlcv (instrument_id, timeframe, ts DESC);
