import sys
import os

from backend.app.ai.research.prospective_audit import ProspectiveAuditor

class ReviewBlockedError(Exception):
    pass

def run_phase_9_4_review(ledger_path: str = "backend/app/ai/research/registry/prospective_ledger.jsonl",
                         outcomes_path: str = "backend/app/ai/research/registry/prospective_outcomes.jsonl") -> dict:
    
    auditor = ProspectiveAuditor(ledger_path, outcomes_path)
    report = auditor.run_audit()
    
    # Check N
    if report.outcomes_evaluated < report.required:
        raise ReviewBlockedError(f"PHASE_9_REVIEW_BLOCKED: Reason: evaluated_count={report.outcomes_evaluated}, required={report.required}")
        
    # Check Integrity
    if report.predictions_invalid > 0 or report.temporal_violations > 0 or \
       report.config_version_mismatches > 0 or report.predictions_duplicate_id > 0 or \
       report.predictions_duplicate_key > 0:
        raise ReviewBlockedError("PHASE_9_REVIEW_BLOCKED: Reason: Integrity audit failed.")
        
    # If we pass the gate, we would theoretically calculate metrics here.
    # Since we are mock testing or running live, we return a dict representing the metric structure.
    return {
        "status": "COMPLETED",
        "evaluated_count": report.outcomes_evaluated,
        "accuracy": 0.0, # Placeholder until actually calculated
        "brier_score": 0.0
    }

if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))
    try:
        results = run_phase_9_4_review()
        print("Review completed.")
    except ReviewBlockedError as e:
        print(e)
