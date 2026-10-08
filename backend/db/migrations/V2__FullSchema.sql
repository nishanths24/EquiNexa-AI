-- Phase 4 (Out-of-order execution) / Part F Full Schema Implementation
-- Ground Rules applied: Foreign Keys, Constraints, RLS, Versioned.

-- 1. AUTH / PROFILES
CREATE TABLE IF NOT EXISTS user_profiles (
    id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    display_name TEXT,
    timezone TEXT DEFAULT 'UTC',
    currency TEXT DEFAULT 'USD',
    preferred_market TEXT DEFAULT 'US',
    default_timeframe TEXT DEFAULT '1D',
    theme TEXT DEFAULT 'system',
    risk_preference TEXT DEFAULT 'moderate',
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Enable RLS on user_profiles
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can manage their own profile" 
ON user_profiles FOR ALL USING (auth.uid() = id);

-- 2. WATCHLISTS & ALERTS
CREATE TABLE IF NOT EXISTS watchlists (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE(user_id, name)
);
ALTER TABLE watchlists ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS watchlist_items (
    id BIGSERIAL PRIMARY KEY,
    watchlist_id BIGINT NOT NULL REFERENCES watchlists(id) ON DELETE CASCADE,
    instrument_id BIGINT NOT NULL REFERENCES instruments(id),
    added_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE(watchlist_id, instrument_id)
);
ALTER TABLE watchlist_items ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS saved_charts (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    instrument_id BIGINT NOT NULL REFERENCES instruments(id),
    layout_json JSONB NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT now()
);
ALTER TABLE saved_charts ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS alerts (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    instrument_id BIGINT NOT NULL REFERENCES instruments(id),
    condition_type TEXT NOT NULL,
    threshold_value NUMERIC(20,8),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT now()
);
ALTER TABLE alerts ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS alert_events (
    id BIGSERIAL PRIMARY KEY,
    alert_id BIGINT NOT NULL REFERENCES alerts(id) ON DELETE CASCADE,
    triggered_at TIMESTAMPTZ DEFAULT now(),
    trigger_value NUMERIC(20,8),
    resolved BOOLEAN DEFAULT false
);

-- 3. MARKET DATA EXTENSIONS
CREATE TABLE IF NOT EXISTS markets (
    id SMALLSERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    region TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS quotes (
    instrument_id BIGINT PRIMARY KEY REFERENCES instruments(id),
    price NUMERIC(20,8) NOT NULL,
    change NUMERIC(20,8),
    change_percent NUMERIC(10,4),
    updated_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS fundamentals (
    instrument_id BIGINT PRIMARY KEY REFERENCES instruments(id),
    market_cap NUMERIC(30,4),
    pe_ratio NUMERIC(10,4),
    pb_ratio NUMERIC(10,4),
    div_yield NUMERIC(10,4),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS financial_statements (
    id BIGSERIAL PRIMARY KEY,
    instrument_id BIGINT NOT NULL REFERENCES instruments(id),
    period_end TIMESTAMPTZ NOT NULL,
    statement_type TEXT NOT NULL,
    metrics JSONB NOT NULL,
    UNIQUE(instrument_id, period_end, statement_type)
);

CREATE TABLE IF NOT EXISTS corporate_events (
    id BIGSERIAL PRIMARY KEY,
    instrument_id BIGINT NOT NULL REFERENCES instruments(id),
    event_type TEXT NOT NULL,
    event_date TIMESTAMPTZ NOT NULL,
    details JSONB
);

-- 4. NEWS & MACRO
CREATE TABLE IF NOT EXISTS news_sources (
    id SMALLSERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    reliability_score INT DEFAULT 50
);

CREATE TABLE IF NOT EXISTS news_articles (
    id BIGSERIAL PRIMARY KEY,
    source_id SMALLINT REFERENCES news_sources(id),
    title TEXT NOT NULL,
    url TEXT NOT NULL UNIQUE,
    published_at TIMESTAMPTZ NOT NULL,
    content_hash TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS news_sentiment (
    article_id BIGINT PRIMARY KEY REFERENCES news_articles(id),
    instrument_id BIGINT REFERENCES instruments(id),
    sentiment_score NUMERIC(5,4),
    importance INT
);

CREATE TABLE IF NOT EXISTS macro_series (
    code TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    value NUMERIC(20,8),
    updated_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS forex_rates (
    pair TEXT PRIMARY KEY,
    rate NUMERIC(20,8),
    updated_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS index_members (
    index_id BIGINT REFERENCES instruments(id),
    member_id BIGINT REFERENCES instruments(id),
    weight NUMERIC(10,6),
    PRIMARY KEY(index_id, member_id)
);

-- 5. SYSTEM LOGGING & PLATFORM HEALTH
CREATE TABLE IF NOT EXISTS provider_health (
    provider_name TEXT PRIMARY KEY,
    status TEXT NOT NULL,
    latency_ms INT,
    last_checked TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS provider_requests (
    id BIGSERIAL PRIMARY KEY,
    provider_name TEXT NOT NULL,
    endpoint TEXT NOT NULL,
    status_code INT NOT NULL,
    timestamp TIMESTAMPTZ DEFAULT now()
);

-- 6. AI ANALYSIS (V2 LEDGER)
CREATE TABLE IF NOT EXISTS ai_analysis (
    id BIGSERIAL PRIMARY KEY,
    instrument_id BIGINT NOT NULL REFERENCES instruments(id),
    generated_at TIMESTAMPTZ NOT NULL,
    bias TEXT NOT NULL,
    scenarios JSONB NOT NULL,
    risk_warning TEXT
);

CREATE TABLE IF NOT EXISTS ai_analysis_features (
    analysis_id BIGINT PRIMARY KEY REFERENCES ai_analysis(id) ON DELETE CASCADE,
    feature_vector JSONB NOT NULL
);

CREATE TABLE IF NOT EXISTS ai_predictions_v2 (
    id BIGSERIAL PRIMARY KEY,
    instrument_id BIGINT NOT NULL REFERENCES instruments(id),
    model_version TEXT NOT NULL,
    predicted_at TIMESTAMPTZ NOT NULL,
    target_date TIMESTAMPTZ NOT NULL,
    prediction_value NUMERIC(20,8)
);

CREATE TABLE IF NOT EXISTS ai_prediction_outcomes (
    prediction_id BIGINT PRIMARY KEY REFERENCES ai_predictions_v2(id),
    actual_value NUMERIC(20,8),
    resolved_at TIMESTAMPTZ NOT NULL,
    error_margin NUMERIC(20,8)
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    action TEXT NOT NULL,
    details JSONB,
    timestamp TIMESTAMPTZ DEFAULT now()
);
