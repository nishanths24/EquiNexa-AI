import sys
import os
from datetime import datetime, timezone
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from backend.app.ai.schemas.prediction import PredictionSnapshot

def test_model_version_frozen():
    # Phase 8.2 Requirement: Model version must strictly be "1.0.0"
    p = PredictionSnapshot(
        prediction_id="abc",
        ticker="AAPL",
        market="US",
        prediction_timestamp=datetime(2022, 1, 7, tzinfo=timezone.utc),
        as_of_timestamp=datetime(2022, 1, 7, tzinfo=timezone.utc),
        model_version="1.0.0",
        model_hash="frozen_hash",
        config_hash="frozen_config",
        feature_version="1.0",
        target_definition={"horizon": 5, "threshold": 0.02},
        predicted_probability=0.8,
        predicted_class=1,
        technical_feature_snapshot={},
        pattern_snapshot={},
        news_article_ids=[],
        news_hashes=[]
    )
    assert p.model_version == "1.0.0", "Model version has been modified. Phase 8.2 STRICTLY requires 1.0.0"
