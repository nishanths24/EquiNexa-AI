from typing import List, Dict, Any
import pandas as pd
from backend.app.ai.research.setups.dsl import DSLParser

class SetupEngine:
    def __init__(self):
        self.parser = DSLParser()
        
    def evaluate_setup(self, df: pd.DataFrame, config_str: str) -> Dict[str, Any]:
        """
        Evaluates a pre-registered setup configuration against historical intraday data.
        """
        if df.empty or len(df) < 5:
            return {"status": "cannot_evaluate", "reason": "Insufficient history"}
            
        try:
            config = self.parser.parse(config_str)
        except ValueError as e:
            return {"status": "error", "reason": str(e)}
            
        # Example feature extraction
        last_bar = df.iloc[-1]
        features = {
            "rsi": 25, # mocked indicator computation for brevity
            "volume": last_bar.get("volume", 0)
        }
        
        passed = self.parser.validate_rules(config["rules"], features)
        
        return {
            "status": "ok",
            "setup_name": config["setup_name"],
            "matched": passed,
            "features_evaluated": features
        }
