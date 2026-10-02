import os
import json
import hashlib
from typing import List, Dict, Optional
from datetime import datetime

from backend.app.ai.schemas.prediction import PredictionSnapshot, OutcomeSnapshot

class PredictionLedger:
    def __init__(self, ledger_path: str = "backend/app/ai/research/registry/prospective_ledger.jsonl",
                 outcomes_path: str = "backend/app/ai/research/registry/prospective_outcomes.jsonl"):
        self.ledger_path = ledger_path
        self.outcomes_path = outcomes_path
        os.makedirs(os.path.dirname(self.ledger_path), exist_ok=True)
        
    def _generate_idempotency_key(self, p: PredictionSnapshot) -> str:
        # market + ticker + prediction_timestamp + model_version + config_hash
        raw = f"{p.market}_{p.ticker}_{p.prediction_timestamp.isoformat()}_{p.model_version}_{p.config_hash}"
        return hashlib.sha256(raw.encode()).hexdigest()

    def record_prediction(self, snapshot: PredictionSnapshot) -> bool:
        """
        Record a prediction. Returns False if duplicate (idempotency check).
        """
        idemp_key = self._generate_idempotency_key(snapshot)
        
        # Check idempotency
        if os.path.exists(self.ledger_path):
            with open(self.ledger_path, 'r') as f:
                for line in f:
                    if not line.strip(): continue
                    data = json.loads(line)
                    if data.get('_idempotency_key') == idemp_key:
                        return False # Duplicate
                        
        # Append record
        record = snapshot.model_dump()
        record['_idempotency_key'] = idemp_key
        record['status'] = 'PENDING'
        record['prediction_timestamp'] = snapshot.prediction_timestamp.isoformat()
        record['as_of_timestamp'] = snapshot.as_of_timestamp.isoformat()
        
        with open(self.ledger_path, 'a') as f:
            f.write(json.dumps(record) + '\n')
            
        return True

    def get_pending_predictions(self) -> List[Dict]:
        """
        Get predictions that do not yet have an EVALUATED or FAILED outcome.
        """
        predictions = {}
        if os.path.exists(self.ledger_path):
            with open(self.ledger_path, 'r') as f:
                for line in f:
                    if not line.strip(): continue
                    p = json.loads(line)
                    predictions[p['prediction_id']] = p
                    
        outcomes = {}
        if os.path.exists(self.outcomes_path):
            with open(self.outcomes_path, 'r') as f:
                for line in f:
                    if not line.strip(): continue
                    o = json.loads(line)
                    outcomes[o['prediction_id']] = o
                    
        pending = []
        for pid, p in predictions.items():
            if pid not in outcomes or outcomes[pid].get('evaluation_status') == 'PENDING':
                pending.append(p)
                
        return pending

    def record_outcome(self, outcome: OutcomeSnapshot):
        """
        Append an outcome record. Does not mutate the prediction snapshot.
        """
        record = outcome.model_dump()
        if record['outcome_timestamp']:
            record['outcome_timestamp'] = outcome.outcome_timestamp.isoformat()
            
        with open(self.outcomes_path, 'a') as f:
            f.write(json.dumps(record) + '\n')
