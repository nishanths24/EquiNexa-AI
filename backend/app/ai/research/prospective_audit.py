import os
import json
from datetime import datetime
import sys

class AuditReport:
    def __init__(self):
        self.predictions_total = 0
        self.predictions_valid = 0
        self.predictions_invalid = 0
        self.predictions_duplicate_id = 0
        self.predictions_duplicate_key = 0
        
        self.temporal_valid = 0
        self.temporal_violations = 0
        
        self.config_valid = 0
        self.config_version_mismatches = 0
        self.config_hash_mismatches = 0
        
        self.outcomes_evaluated = 0
        self.outcomes_pending = 0
        self.outcomes_invalid = 0
        
        self.data_complete = 0
        self.data_partial = 0
        self.data_invalid = 0
        
        self.required = 100
        self.review_status = "COLLECTING"

class ProspectiveAuditor:
    def __init__(self, ledger_path: str = "backend/app/ai/research/registry/prospective_ledger.jsonl",
                 outcomes_path: str = "backend/app/ai/research/registry/prospective_outcomes.jsonl"):
        self.ledger_path = ledger_path
        self.outcomes_path = outcomes_path
        
    def run_audit(self) -> AuditReport:
        report = AuditReport()
        predictions = {}
        idempotency_keys = set()
        
        # 1. Parse Predictions
        if os.path.exists(self.ledger_path):
            with open(self.ledger_path, 'r') as f:
                for line in f:
                    if not line.strip(): continue
                    p = json.loads(line)
                    report.predictions_total += 1
                    
                    is_valid = True
                    
                    pid = p.get('prediction_id')
                    if not pid or pid in predictions:
                        report.predictions_duplicate_id += 1
                        is_valid = False
                    
                    idemp_key = p.get('_idempotency_key')
                    if not idemp_key or idemp_key in idempotency_keys:
                        report.predictions_duplicate_key += 1
                        is_valid = False
                    if idemp_key:
                        idempotency_keys.add(idemp_key)
                        
                    model_version = p.get('model_version')
                    if model_version != "1.0.0":
                        report.config_version_mismatches += 1
                        is_valid = False
                        
                    config_hash = p.get('config_hash')
                    if not config_hash:
                        report.config_hash_mismatches += 1
                        is_valid = False
                        
                    # Completeness
                    has_features = p.get('technical_feature_snapshot') is not None
                    has_patterns = p.get('pattern_snapshot') is not None
                    has_prob = p.get('predicted_probability') is not None
                    
                    if not (has_features and has_patterns and has_prob):
                        report.data_invalid += 1
                        is_valid = False
                    elif p.get('sentiment_output') is None:
                        report.data_partial += 1
                    else:
                        report.data_complete += 1
                        
                    if is_valid:
                        report.predictions_valid += 1
                        report.config_valid += 1
                    else:
                        report.predictions_invalid += 1
                        
                    if pid:
                        predictions[pid] = p

        # 2. Parse Outcomes
        outcomes = {}
        if os.path.exists(self.outcomes_path):
            with open(self.outcomes_path, 'r') as f:
                for line in f:
                    if not line.strip(): continue
                    o = json.loads(line)
                    pid = o.get('prediction_id')
                    
                    if not pid or pid not in predictions:
                        report.outcomes_invalid += 1
                        continue
                        
                    status = o.get('evaluation_status')
                    if status == "EVALUATED":
                        report.outcomes_evaluated += 1
                        
                        # Temporal audit
                        pred_ts = predictions[pid].get('prediction_timestamp')
                        out_ts = o.get('outcome_timestamp')
                        if pred_ts and out_ts:
                            try:
                                pt = datetime.fromisoformat(pred_ts)
                                ot = datetime.fromisoformat(out_ts)
                                if pt >= ot:
                                    report.temporal_violations += 1
                                else:
                                    report.temporal_valid += 1
                            except ValueError:
                                report.temporal_violations += 1
                        else:
                            report.temporal_violations += 1
                    else:
                        # Could be failed, but we only have pending
                        pass
                        
                    outcomes[pid] = o
                    
        report.outcomes_pending = report.predictions_total - report.outcomes_evaluated - report.outcomes_invalid
        
        if report.outcomes_evaluated >= report.required:
            report.review_status = "READY_FOR_REVIEW"
            
        return report

def main():
    # Fix paths for execution
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))
    
    auditor = ProspectiveAuditor()
    r = auditor.run_audit()
    
    print("Prospective Integrity Audit")
    print("---------------------------")
    print("Model Version: 1.0.0\n")
    print("Predictions:")
    print(f"  Total: {r.predictions_total}")
    print(f"  Valid: {r.predictions_valid}")
    print(f"  Invalid: {r.predictions_invalid}")
    print(f"  Duplicate: {r.predictions_duplicate_id + r.predictions_duplicate_key}\n")
    print("Temporal Integrity:")
    print(f"  Valid: {r.temporal_valid}")
    print(f"  Violations: {r.temporal_violations}\n")
    print("Configuration:")
    print(f"  Valid: {r.config_valid}")
    print(f"  Version Mismatches: {r.config_version_mismatches}")
    print(f"  Hash Mismatches: {r.config_hash_mismatches}\n")
    print("Outcomes:")
    print(f"  Evaluated: {r.outcomes_evaluated}")
    print(f"  Pending: {r.outcomes_pending}")
    print(f"  Invalid: {r.outcomes_invalid}\n")
    print("Data Completeness:")
    print(f"  Complete: {r.data_complete}")
    print(f"  Partial: {r.data_partial}")
    print(f"  Invalid: {r.data_invalid}\n")
    print("Review Threshold:")
    print(f"  Required: {r.required}")
    print(f"  Evaluated: {r.outcomes_evaluated}")
    print(f"  Remaining: {max(0, r.required - r.outcomes_evaluated)}")
    print(f"  Status: {r.review_status}")

if __name__ == "__main__":
    main()
