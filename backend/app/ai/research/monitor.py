import os
import json
import logging
from datetime import datetime
from typing import Dict, Optional

class IntegrityViolationError(Exception):
    pass

class ObservationMonitor:
    def __init__(self, ledger_path: str = "backend/app/ai/research/registry/prospective_ledger.jsonl",
                 outcomes_path: str = "backend/app/ai/research/registry/prospective_outcomes.jsonl",
                 flag_path: str = "backend/app/ai/research/registry/phase9_review_flag.txt"):
        self.ledger_path = ledger_path
        self.outcomes_path = outcomes_path
        self.flag_path = flag_path

    def get_status(self) -> Dict:
        """
        Scan ledgers, enforce constraints, calculate sample sizes.
        Returns a dictionary of metrics.
        Raises IntegrityViolationError if constraints broken.
        """
        predictions = {}
        idempotency_keys = set()
        
        oldest_pending: Optional[datetime] = None
        latest_prediction: Optional[datetime] = None

        if os.path.exists(self.ledger_path):
            with open(self.ledger_path, 'r') as f:
                for line in f:
                    if not line.strip(): continue
                    p = json.loads(line)
                    
                    if p.get("model_version") != "1.0.0":
                        raise IntegrityViolationError(f"CRITICAL: Model version modified to {p.get('model_version')}. Expected 1.0.0")
                        
                    idemp_key = p.get("_idempotency_key")
                    if idemp_key in idempotency_keys:
                        raise IntegrityViolationError(f"CRITICAL: Duplicate idempotency key detected: {idemp_key}")
                    if idemp_key:
                        idempotency_keys.add(idemp_key)
                        
                    pred_id = p['prediction_id']
                    if pred_id in predictions:
                        raise IntegrityViolationError(f"CRITICAL: Duplicate prediction ID detected: {pred_id}")
                        
                    predictions[pred_id] = p
                    
                    pt = datetime.fromisoformat(p['prediction_timestamp'])
                    if not latest_prediction or pt > latest_prediction:
                        latest_prediction = pt

        outcomes = {}
        if os.path.exists(self.outcomes_path):
            with open(self.outcomes_path, 'r') as f:
                for line in f:
                    if not line.strip(): continue
                    o = json.loads(line)
                    pid = o['prediction_id']
                    
                    if pid not in predictions:
                        raise IntegrityViolationError(f"CRITICAL: Outcome logged for unknown prediction ID: {pid}")
                        
                    outcomes[pid] = o

        evaluated_count = sum(1 for o in outcomes.values() if o.get('evaluation_status') == 'EVALUATED')
        pending_count = len(predictions) - evaluated_count
        
        # Calculate oldest pending
        for pid, p in predictions.items():
            if pid not in outcomes or outcomes[pid].get('evaluation_status') != 'EVALUATED':
                pt = datetime.fromisoformat(p['prediction_timestamp'])
                if not oldest_pending or pt < oldest_pending:
                    oldest_pending = pt
        
        required = 100
        remaining = max(0, required - evaluated_count)
        
        review_status = "COLLECTING"
        if evaluated_count >= required:
            review_status = "READY_FOR_REVIEW"
            if not os.path.exists(self.flag_path):
                # Emit exactly once
                print("PHASE_9_READY_FOR_REVIEW")
                os.makedirs(os.path.dirname(self.flag_path), exist_ok=True)
                with open(self.flag_path, 'w') as f:
                    f.write("ready")
        
        return {
            "model_version": "1.0.0",
            "target": "5-day return > 2%",
            "evaluated": evaluated_count,
            "pending": pending_count,
            "required": required,
            "remaining": remaining,
            "total_logged": len(predictions),
            "rejected_duplicates": 0, # Usually tracked in logs
            "integrity_violations": 0,
            "oldest_pending": oldest_pending.isoformat() if oldest_pending else "None",
            "latest_prediction": latest_prediction.isoformat() if latest_prediction else "None",
            "review_status": review_status
        }
