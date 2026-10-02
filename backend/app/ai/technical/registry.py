from typing import Dict, Any, Callable
from pydantic import BaseModel
import pandas as pd
from backend.app.ai.marketdata.market_data_provider import PriceFrame

class FeatureSpec(BaseModel):
    name: str
    version: str
    window: int
    inputs: list[str]
    warmup_bars: int
    params_hash: str

class FeatureRegistry:
    def __init__(self):
        self._features: Dict[str, FeatureSpec] = {}
        self._computers: Dict[str, Callable[[PriceFrame], pd.Series]] = {}
        
    def register(self, spec: FeatureSpec, computer: Callable[[PriceFrame], pd.Series]):
        self._features[spec.name] = spec
        self._computers[spec.name] = computer
        
    def get_spec(self, name: str) -> FeatureSpec:
        return self._features[name]
        
    def compute(self, name: str, df: PriceFrame) -> pd.Series:
        if name not in self._computers:
            raise ValueError(f"Feature {name} not registered")
        return self._computers[name](df)

    def compute_all(self, df: PriceFrame) -> pd.DataFrame:
        df_out = df.copy()
        for name, computer in self._computers.items():
            df_out[name] = computer(df)
        return df_out

feature_registry = FeatureRegistry()
