import pytest
import os
import json
import sys
from datetime import datetime, timezone

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from backend.app.ai.research.monitor import ObservationMonitor, IntegrityViolationError

def test_model_freeze_enforcement(tmp_path):
    ledger = str(tmp_path / "ledger.jsonl")
    flag = str(tmp_path / "flag.txt")
    
    with open(ledger, "w") as f:
        f.write(json.dumps({
            "prediction_id": "1",
            "model_version": "1.0.1",
            "_idempotency_key": "x",
            "prediction_timestamp": "2022-01-01T00:00:00+00:00"
        }) + "\n")
        
    monitor = ObservationMonitor(ledger_path=ledger, outcomes_path=str(tmp_path / "o.jsonl"), flag_path=flag)
    
    with pytest.raises(IntegrityViolationError, match="CRITICAL: Model version modified"):
        monitor.get_status()

def test_duplicate_idempotency_detection(tmp_path):
    ledger = str(tmp_path / "ledger.jsonl")
    flag = str(tmp_path / "flag.txt")
    
    with open(ledger, "w") as f:
        f.write(json.dumps({
            "prediction_id": "1",
            "model_version": "1.0.0",
            "_idempotency_key": "DUPE",
            "prediction_timestamp": "2022-01-01T00:00:00+00:00"
        }) + "\n")
        f.write(json.dumps({
            "prediction_id": "2",
            "model_version": "1.0.0",
            "_idempotency_key": "DUPE",
            "prediction_timestamp": "2022-01-01T00:00:00+00:00"
        }) + "\n")
        
    monitor = ObservationMonitor(ledger_path=ledger, outcomes_path=str(tmp_path / "o.jsonl"), flag_path=flag)
    
    with pytest.raises(IntegrityViolationError, match="Duplicate idempotency key"):
        monitor.get_status()

def test_sample_size_tracking_and_trigger(tmp_path):
    ledger = str(tmp_path / "ledger.jsonl")
    outcomes = str(tmp_path / "o.jsonl")
    flag = str(tmp_path / "flag.txt")
    
    with open(ledger, "w") as f:
        for i in range(105):
            f.write(json.dumps({
                "prediction_id": str(i),
                "model_version": "1.0.0",
                "_idempotency_key": f"key_{i}",
                "prediction_timestamp": "2022-01-01T00:00:00+00:00"
            }) + "\n")
            
    with open(outcomes, "w") as f:
        for i in range(100): 
            f.write(json.dumps({
                "prediction_id": str(i),
                "evaluation_status": "EVALUATED"
            }) + "\n")
            
    monitor = ObservationMonitor(ledger_path=ledger, outcomes_path=outcomes, flag_path=flag)
    status = monitor.get_status()
    
    assert status['evaluated'] == 100
    assert status['pending'] == 5
    assert status['remaining'] == 0
    assert status['review_status'] == "READY_FOR_REVIEW"
    assert os.path.exists(flag)
