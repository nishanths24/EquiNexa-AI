from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import os
import json
import sys

# Append root for python module resolution if running directly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from backend.app.ai.research.monitor import ObservationMonitor

app = FastAPI(title="EquiNexa AI Prospective Engine API", version="1.0.0")

# Allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/v1/health")
def health_check():
    return {"status": "ok", "version": "1.0.0", "timestamp": datetime.utcnow().isoformat()}

@app.get("/api/v1/research/status")
def get_research_status():
    try:
        monitor = ObservationMonitor()
        status = monitor.get_status()
        
        return {
            "model_version": "1.0.0",
            "target": "5-day return > 2%",
            "evaluated": status.get('evaluated', 0),
            "pending": status.get('pending', 0),
            "required": 100,
            "remaining": max(0, 100 - status.get('evaluated', 0)),
            "total_logged": status.get('total_logged', 0),
            "rejected_duplicates": status.get('rejected_duplicates', 0),
            "integrity_violations": status.get('integrity_violations', 0),
            "oldest_pending": status.get('oldest_pending', "None"),
            "latest_prediction": status.get('latest_prediction', "None"),
            "review_status": "READY_FOR_REVIEW" if status.get('ready_for_review') else "COLLECTING"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unable to read prospective registry state.")

@app.get("/api/v1/markets/indices")
def get_indices():
    # Currently the backend provider doesn't reliably cache indices outside of prediction windows.
    # To prevent displaying stale data or faking values, we explicitly return UNAVAILABLE.
    return {"status": "UNAVAILABLE", "reason": "No real-time index provider configured for read-only endpoint"}

@app.get("/api/v1/markets/search")
def search_markets(q: str = Query(..., min_length=1)):
    # Currently no instrument master exists.
    return {"status": "UNAVAILABLE", "results": []}

@app.get("/api/v1/predictions/latest")
def get_latest_prediction(ticker: str):
    ledger_path = "backend/app/ai/research/registry/prospective_ledger.jsonl"
    if not os.path.exists(ledger_path):
        raise HTTPException(status_code=404, detail="No prospective ledger found")
        
    latest_pred = None
    with open(ledger_path, 'r') as f:
        for line in f:
            if not line.strip(): continue
            try:
                record = json.loads(line)
                if record.get('ticker') == ticker:
                    latest_pred = record
            except json.JSONDecodeError:
                pass
                
    if not latest_pred:
        raise HTTPException(status_code=404, detail="Prediction not found for ticker")
        
    return {
        "prediction_id": latest_pred.get("prediction_id"),
        "model_version": latest_pred.get("model_version"),
        "prediction_timestamp": latest_pred.get("prediction_timestamp"),
        "ticker": latest_pred.get("ticker"),
        "predicted_probability": latest_pred.get("predicted_probability")
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.api.main:app", host="127.0.0.1", port=8000, reload=True)
