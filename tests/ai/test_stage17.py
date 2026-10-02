import pytest
import os
import tempfile
from datetime import datetime, timezone
from backend.app.ai.models.registry.model_registry import ModelRegistry, ModelMetadata

def test_model_registry():
    with tempfile.TemporaryDirectory() as tmpdir:
        registry = ModelRegistry(tmpdir)
        
        meta1 = ModelMetadata(
            version="1.0.0",
            model_type="technical_baseline",
            created_at=datetime.now(timezone.utc),
            hyperparameters={"C": 1.0},
            metrics={"accuracy": 0.52},
            artifact_path="models/v1.pkl",
            is_production=False
        )
        
        registry.register_model("model_1", meta1)
        
        assert registry.get_model("model_1").version == "1.0.0"
        
        # Test promotion
        registry.set_production("model_1", "technical_baseline")
        prod = registry.get_production_model("technical_baseline")
        assert prod is not None
        assert prod.version == "1.0.0"
        
        # Test demotion when new model is promoted
        meta2 = ModelMetadata(
            version="1.1.0",
            model_type="technical_baseline",
            created_at=datetime.now(timezone.utc),
            hyperparameters={"C": 0.5},
            metrics={"accuracy": 0.54},
            artifact_path="models/v2.pkl",
            is_production=False
        )
        registry.register_model("model_2", meta2)
        registry.set_production("model_2", "technical_baseline")
        
        prod2 = registry.get_production_model("technical_baseline")
        assert prod2.version == "1.1.0"
        assert not registry.get_model("model_1").is_production
