import pytest
import os
import json
import sys
from datetime import datetime, timezone, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from backend.app.ai.research.prospective_audit import ProspectiveAuditor

def test_audit_valid_observation(tmp_path):
    ledger = str(tmp_path / "ledger.jsonl")
    outcomes = str(tmp_path / "outcomes.jsonl")
    
    with open(ledger, "w") as f:
        f.write(json.dumps({
            "prediction_id": "p1",
            "model_version": "1.0.0",
            "_idempotency_key": "k1",
            "prediction_timestamp": "2022-01-01T00:00:00+00:00",
            "config_hash": "c1",
            "technical_feature_snapshot": {},
            "pattern_snapshot": {},
            "predicted_probability": 0.5,
            "sentiment_output": {}
        }) + "\n")
        
    with open(outcomes, "w") as f:
        f.write(json.dumps({
            "prediction_id": "p1",
            "evaluation_status": "EVALUATED",
            "outcome_timestamp": "2022-01-08T00:00:00+00:00"
        }) + "\n")
        
    auditor = ProspectiveAuditor(ledger, outcomes)
    report = auditor.run_audit()
    
    assert report.predictions_total == 1
    assert report.predictions_valid == 1
    assert report.temporal_valid == 1
    assert report.config_valid == 1
    assert report.outcomes_evaluated == 1
    assert report.data_complete == 1
    assert report.review_status == "COLLECTING"

def test_audit_duplicate_detection(tmp_path):
    ledger = str(tmp_path / "ledger.jsonl")
    outcomes = str(tmp_path / "outcomes.jsonl")
    
    with open(ledger, "w") as f:
        f.write(json.dumps({
            "prediction_id": "p1",
            "model_version": "1.0.0",
            "_idempotency_key": "k1",
            "prediction_timestamp": "2022-01-01T00:00:00+00:00"
        }) + "\n")
        f.write(json.dumps({
            "prediction_id": "p2",
            "model_version": "1.0.0",
            "_idempotency_key": "k1",  # Duplicate key
            "prediction_timestamp": "2022-01-01T00:00:00+00:00"
        }) + "\n")
        
    auditor = ProspectiveAuditor(ledger, outcomes)
    report = auditor.run_audit()
    
    assert report.predictions_total == 2
    assert report.predictions_duplicate_key == 1
    assert report.predictions_invalid == 2  # Missing fields too

def test_audit_temporal_violation(tmp_path):
    ledger = str(tmp_path / "ledger.jsonl")
    outcomes = str(tmp_path / "outcomes.jsonl")
    
    with open(ledger, "w") as f:
        f.write(json.dumps({
            "prediction_id": "p1",
            "model_version": "1.0.0",
            "_idempotency_key": "k1",
            "prediction_timestamp": "2022-01-08T00:00:00+00:00",
            "config_hash": "c1",
            "technical_feature_snapshot": {},
            "pattern_snapshot": {},
            "predicted_probability": 0.5,
            "sentiment_output": {}
        }) + "\n")
        
    with open(outcomes, "w") as f:
        f.write(json.dumps({
            "prediction_id": "p1",
            "evaluation_status": "EVALUATED",
            "outcome_timestamp": "2022-01-01T00:00:00+00:00"  # Premature outcome
        }) + "\n")
        
    auditor = ProspectiveAuditor(ledger, outcomes)
    report = auditor.run_audit()
    
    assert report.temporal_violations == 1
