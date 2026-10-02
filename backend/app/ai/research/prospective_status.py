import sys
import os

# Ensure backend module is resolvable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))

from backend.app.ai.research.monitor import ObservationMonitor, IntegrityViolationError

def print_status():
    monitor = ObservationMonitor()
    try:
        status = monitor.get_status()
    except IntegrityViolationError as e:
        status = {
            "model_version": "1.0.0",
            "target": "5-day return > 2%",
            "evaluated": 0,
            "pending": 0,
            "required": 100,
            "remaining": 100,
            "total_logged": 0,
            "rejected_duplicates": 0,
            "integrity_violations": 1,
            "oldest_pending": "None",
            "latest_prediction": "None",
            "review_status": "HALTED - INTEGRITY VIOLATION"
        }
        print(f"CRITICAL ERROR: {str(e)}")
        
    print("Prospective Observation Status")
    print("------------------------------")
    print(f"Model Version: {status['model_version']}")
    print(f"Target: {status['target']}")
    print(f"Evaluated: {status['evaluated']}")
    print(f"Pending: {status['pending']}")
    print(f"Required: {status['required']}")
    print(f"Remaining: {status['remaining']}")
    print(f"Total Logged: {status['total_logged']}")
    print(f"Rejected Duplicates: {status['rejected_duplicates']}")
    print(f"Integrity Violations: {status['integrity_violations']}")
    print(f"Oldest Pending: {status['oldest_pending']}")
    print(f"Latest Prediction: {status['latest_prediction']}")
    print(f"Review Status: {status['review_status']}")

if __name__ == "__main__":
    print_status()
