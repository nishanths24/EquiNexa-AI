import json
from typing import Dict, Any

class DSLParser:
    """
    Parses safe JSON-based domain specific language for setup configurations.
    Explicitly avoids `eval()` for safety.
    """
    def parse(self, config_str: str) -> Dict[str, Any]:
        try:
            config = json.loads(config_str)
            # Basic schema validation
            if "setup_name" not in config or "rules" not in config:
                raise ValueError("Invalid setup configuration schema.")
            return config
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON Parsing Error: {str(e)}")
            
    def validate_rules(self, rules: Dict[str, Any], features: Dict[str, Any]) -> bool:
        """
        Safely evaluates rules against features without eval().
        """
        for rule_key, condition in rules.items():
            if rule_key == "rsi_threshold":
                if features.get("rsi", 100) > condition:
                    return False
            elif rule_key == "volume_spike":
                if features.get("volume", 0) <= condition:
                    return False
            # Extensible for other simple rule primitives
        return True
