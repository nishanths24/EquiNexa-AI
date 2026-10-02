import os
import json

ledger_path = "backend/app/ai/research/registry/prospective_ledger.jsonl"
outcomes_path = "backend/app/ai/research/registry/prospective_outcomes.jsonl"

predictions = {}
if os.path.exists(ledger_path):
    with open(ledger_path, 'r') as f:
        for line in f:
            if not line.strip(): continue
            p = json.loads(line)
            predictions[p['prediction_id']] = p

outcomes = {}
if os.path.exists(outcomes_path):
    with open(outcomes_path, 'r') as f:
        for line in f:
            if not line.strip(): continue
            o = json.loads(line)
            outcomes[o['prediction_id']] = o

evaluated = [pid for pid, o in outcomes.items() if o.get('evaluation_status') == 'EVALUATED']
pending = [pid for pid in predictions if pid not in evaluated]

print(f"Total Predictions: {len(predictions)}")
print(f"Evaluated Predictions (N): {len(evaluated)}")
print(f"Pending Predictions: {len(pending)}")
