import uuid
import hashlib
import json
from datetime import datetime, timezone
import pandas as pd

from backend.app.ai.schemas.prediction import PredictionSnapshot
from backend.app.ai.patterns.candlestick.engine import CandlestickEngine
from backend.app.ai.patterns.chart.engine import ChartPatternEngine

class LivePredictionPipeline:
    def __init__(self, model, config, embedder, vector_store, news_provider):
        self.model = model
        self.config = config
        self.embedder = embedder
        self.vector_store = vector_store
        self.news_provider = news_provider
        self.candlestick_engine = CandlestickEngine()
        self.chart_engine = ChartPatternEngine()

    def predict(self, ticker: str, market: str, market_data: pd.DataFrame, prediction_timestamp: datetime) -> PredictionSnapshot:
        """
        Generate a point-in-time prospective prediction.
        """
        if prediction_timestamp.tzinfo is None:
            raise ValueError("prediction_timestamp must be timezone aware")
            
        # 1. As-of Filter Market Data
        # Ensure no future data is in the dataframe
        valid_market_data = market_data[market_data.index <= prediction_timestamp]
        if len(valid_market_data) == 0:
            raise ValueError("No valid market data available at prediction timestamp")
            
        current_row = valid_market_data.iloc[-1:]
        
        # 2. Extract technical features
        tech_features = {}
        for f in self.config.data.features:
            if f in current_row.columns:
                tech_features[f] = float(current_row[f].iloc[0])
                
        # 3. Deterministic Patterns
        patterns = {
            "breakout": bool(self.chart_engine.detect_breakout(valid_market_data).iloc[-1]),
            "support_bounce": bool(self.chart_engine.detect_support_bounce(valid_market_data).iloc[-1]),
            "double_bottom": bool(self.chart_engine.detect_double_bottom(valid_market_data).iloc[-1]),
            "double_top": bool(self.chart_engine.detect_double_top(valid_market_data).iloc[-1]),
            "head_and_shoulders": bool(self.chart_engine.detect_head_and_shoulders(valid_market_data).iloc[-1])
        }
        
        # 4. News Retrieval (Point-in-Time)
        # Using the retriever logically to fetch news strictly published < prediction_timestamp
        # Here we mock the behavior since we don't have the fully injected retriever
        retrieved_articles = []
        article_ids = []
        article_hashes = []
        sentiment_output = None
        
        if self.news_provider:
            # fetch raw news and filter
            raw_news = self.news_provider.fetch_live_news(ticker)
            for n in raw_news:
                if n.published_at < prediction_timestamp:
                    retrieved_articles.append(n)
                    article_ids.append(n.article_id)
                    article_hashes.append(n.content_hash)
            
            # Mock sentiment
            sentiment_output = {
                "status": "unavailable",
                "reason": "zero-budget constraints"
            }
        else:
            sentiment_output = {"status": "unavailable"}

        # 5. Model Prediction
        # Flatten features
        X = [tech_features[f] for f in self.config.data.features if f in tech_features]
        try:
            if hasattr(self.model, 'predict_proba'):
                prob = float(self.model.predict_proba([X])[0][1])
            else:
                prob = 0.5
        except Exception:
            prob = 0.5
            
        pred_class = 1 if prob > 0.5 else 0

        # Pattern ensemble (simplified mock logic for live prospective)
        bullish = patterns["breakout"] or patterns["support_bounce"] or patterns["double_bottom"]
        bearish = patterns["double_top"] or patterns["head_and_shoulders"]
        
        if bullish and not bearish:
            prob = prob * 0.8 + 0.8 * 0.2
        elif bearish and not bullish:
            prob = prob * 0.8 + 0.2 * 0.2

        # Hash inputs for provenance
        config_hash = hashlib.sha256(json.dumps(self.config.model_dump(), sort_keys=True, default=str).encode()).hexdigest()
        
        snapshot = PredictionSnapshot(
            prediction_id=str(uuid.uuid4()),
            ticker=ticker,
            market=market,
            prediction_timestamp=prediction_timestamp,
            as_of_timestamp=prediction_timestamp,
            model_version="1.0.0",
            model_hash="dummy_model_hash",
            config_hash=config_hash,
            feature_version="1.0.0",
            target_definition={"horizon": 5, "threshold": 0.02},
            predicted_probability=prob,
            predicted_class=pred_class,
            technical_feature_snapshot=tech_features,
            pattern_snapshot=patterns,
            news_article_ids=article_ids,
            news_hashes=article_hashes,
            sentiment_output=sentiment_output,
            retrieval_metadata={"count": len(retrieved_articles)}
        )
        
        return snapshot
