import pytest
import os
import json
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from backend.app.ai.research.prospective_review import run_phase_9_4_review, ReviewBlockedError

def test_review_blocked_n0(tmp_path):
    ledger = str(tmp_path / "ledger.jsonl")
    outcomes = str(tmp_path / "o.jsonl")
    
    with open(ledger, "w") as f: pass
    with open(outcomes, "w") as f: pass
    
    with pytest.raises(ReviewBlockedError, match="PHASE_9_REVIEW_BLOCKED: Reason: evaluated_count=0, required=100"):
        run_phase_9_4_review(ledger, outcomes)

def test_review_blocked_n99(tmp_path):
    ledger = str(tmp_path / "ledger.jsonl")
    outcomes = str(tmp_path / "o.jsonl")
    
    with open(ledger, "w") as f:
        for i in range(99):
            f.write(json.dumps({
                "prediction_id": str(i), "model_version": "1.0.0", "_idempotency_key": str(i),
                "config_hash": "c", "technical_feature_snapshot": {}, "pattern_snapshot": {},
                "predicted_probability": 0.5, "prediction_timestamp": "2022-01-01T00:00:00+00:00"
            }) + "\n")
    with open(outcomes, "w") as f:
        for i in range(99):
            f.write(json.dumps({
                "prediction_id": str(i), "evaluation_status": "EVALUATED",
                "outcome_timestamp": "2022-01-08T00:00:00+00:00"
            }) + "\n")
            
    with pytest.raises(ReviewBlockedError, match="PHASE_9_REVIEW_BLOCKED: Reason: evaluated_count=99, required=100"):
        run_phase_9_4_review(ledger, outcomes)

def test_review_allowed_n100(tmp_path):
    ledger = str(tmp_path / "ledger.jsonl")
    outcomes = str(tmp_path / "o.jsonl")
    
    with open(ledger, "w") as f:
        for i in range(100):
            f.write(json.dumps({
                "prediction_id": str(i), "model_version": "1.0.0", "_idempotency_key": str(i),
                "config_hash": "c", "technical_feature_snapshot": {}, "pattern_snapshot": {},
                "predicted_probability": 0.5, "prediction_timestamp": "2022-01-01T00:00:00+00:00"
            }) + "\n")
    with open(outcomes, "w") as f:
        for i in range(100):
            f.write(json.dumps({
                "prediction_id": str(i), "evaluation_status": "EVALUATED",
                "outcome_timestamp": "2022-01-08T00:00:00+00:00"
            }) + "\n")
            
    result = run_phase_9_4_review(ledger, outcomes)
    assert result["status"] == "COMPLETED"
    assert result["evaluated_count"] == 100

def test_review_blocked_integrity_violation(tmp_path):
    ledger = str(tmp_path / "ledger.jsonl")
    outcomes = str(tmp_path / "o.jsonl")
    
    with open(ledger, "w") as f:
        for i in range(100):
            # i==0 has wrong model version
            f.write(json.dumps({
                "prediction_id": str(i), "model_version": "1.0.1" if i == 0 else "1.0.0",
                "_idempotency_key": str(i), "config_hash": "c", "technical_feature_snapshot": {},
                "pattern_snapshot": {}, "predicted_probability": 0.5,
                "prediction_timestamp": "2022-01-01T00:00:00+00:00"
            }) + "\n")
    with open(outcomes, "w") as f:
        for i in range(100):
            f.write(json.dumps({
                "prediction_id": str(i), "evaluation_status": "EVALUATED",
                "outcome_timestamp": "2022-01-08T00:00:00+00:00"
            }) + "\n")
            
    with pytest.raises(ReviewBlockedError, match="PHASE_9_REVIEW_BLOCKED: Reason: Integrity audit failed."):
        run_phase_9_4_review(ledger, outcomes)
