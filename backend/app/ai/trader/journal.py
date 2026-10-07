import json
import os
import copy
from typing import Dict, Any, List
from datetime import datetime

class JournalEngine:
    """
    Manages the trader journal, revisions, and discipline analytics.
    Ensures revision history immutability.
    """
    def __init__(self, storage_path: str = "journal_db.json"):
        self.storage_path = storage_path
        self._load()
        
    def _load(self):
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'r') as f:
                self.db = json.load(f)
        else:
            self.db = {"trades": {}}
            
    def _save(self):
        with open(self.storage_path, 'w') as f:
            json.dump(self.db, f, indent=2)
            
    def add_trade(self, trade_data: Dict[str, Any]) -> str:
        trade_id = f"trd_{int(datetime.utcnow().timestamp())}"
        trade_data["id"] = trade_id
        trade_data["created_at"] = datetime.utcnow().isoformat()
        trade_data["revisions"] = []
        
        self.db["trades"][trade_id] = trade_data
        self._save()
        return trade_id
        
    def update_trade(self, trade_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        if trade_id not in self.db["trades"]:
            return {"status": "error", "reason": "Trade not found"}
            
        trade = self.db["trades"][trade_id]
        
        # Save exact copy to revisions to ensure immutability of history
        revision_copy = copy.deepcopy(trade)
        revision_copy.pop("revisions", None)
        revision_copy["revised_at"] = datetime.utcnow().isoformat()
        
        trade["revisions"].append(revision_copy)
        
        for k, v in updates.items():
            if k not in ["id", "created_at", "revisions"]:
                trade[k] = v
                
        self._save()
        return {"status": "ok", "trade_id": trade_id}
        
    def get_analytics(self) -> Dict[str, Any]:
        trades = list(self.db["trades"].values())
        if not trades:
            return {"total_trades": 0}
            
        winners = [t for t in trades if t.get("pnl", 0) > 0]
        losers = [t for t in trades if t.get("pnl", 0) <= 0]
        
        # Analytics calculations
        return {
            "total_trades": len(trades),
            "win_rate": round(len(winners) / len(trades) * 100, 2) if trades else 0.0,
            "revenge_trade_warnings": 0 # P5 implementation: check timestamps between consecutive losers
        }
