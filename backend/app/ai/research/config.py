from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class ValidationConfig(BaseModel):
    method: str = "walk_forward"
    initial_train_size: int = 100
    step_size: int = 20
    embargo_bars: int = 1

class TargetConfig(BaseModel):
    horizon: int = 5
    threshold: float = 0.02
    type: str = "binary" # binary or multiclass

class DataConfig(BaseModel):
    dataset_path: str = "data/historical_dataset.csv"
    tickers: List[str]
    start_date: str
    end_date: str
    features: List[str]

class ModelConfig(BaseModel):
    model_type: str = "LogisticRegression"
    hyperparameters: Dict[str, Any] = {}
    use_patterns: bool = False

class ExperimentConfig(BaseModel):
    experiment_id: str
    description: str
    data: DataConfig
    target: TargetConfig
    validation: ValidationConfig
    model: ModelConfig = Field(default_factory=ModelConfig)
    random_seed: int = 42

class ExperimentResult(BaseModel):
    experiment_id: str
    timestamp: str
    config_hash: str
    dataset_hash: str
    metrics: Dict[str, Any]
    artifacts: List[str] = []
