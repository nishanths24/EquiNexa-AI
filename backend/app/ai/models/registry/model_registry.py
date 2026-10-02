import json
import os
from datetime import datetime
from pydantic import BaseModel
from typing import Dict, Any, Optional

class ModelMetadata(BaseModel):
    version: str
    model_type: str
    created_at: datetime
    hyperparameters: Dict[str, Any]
    metrics: Dict[str, float]
    artifact_path: str
    is_production: bool = False

class ModelRegistry:
    def __init__(self, storage_dir: str):
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)
        self.registry_file = os.path.join(self.storage_dir, "registry.json")
        self._load()
        
    def _load(self):
        if os.path.exists(self.registry_file):
            with open(self.registry_file, 'r') as f:
                data = json.load(f)
                self.models = {k: ModelMetadata(**v) for k, v in data.items()}
        else:
            self.models = {}
            
    def _save(self):
        with open(self.registry_file, 'w') as f:
            json.dump({k: v.model_dump(mode='json') for k, v in self.models.items()}, f, indent=2)
            
    def register_model(self, model_id: str, metadata: ModelMetadata):
        self.models[model_id] = metadata
        self._save()
        
    def get_model(self, model_id: str) -> Optional[ModelMetadata]:
        return self.models.get(model_id)
        
    def set_production(self, model_id: str, model_type: str):
        # Demote others of same type
        for mid, meta in self.models.items():
            if meta.model_type == model_type and meta.is_production:
                meta.is_production = False
                
        if model_id in self.models:
            self.models[model_id].is_production = True
        self._save()
        
    def get_production_model(self, model_type: str) -> Optional[ModelMetadata]:
        for meta in self.models.values():
            if meta.model_type == model_type and meta.is_production:
                return meta
        return None
