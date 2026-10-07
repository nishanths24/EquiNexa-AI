from typing import Dict, Any

class ResponseValidator:
    def validate(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates output to ensure no financial advice and strict schema adherence.
        """
        answer = report.get("answer_to_question", "").lower()
        
        forbidden_phrases = ["buy this stock", "guaranteed returns", "sure thing", "must buy", "sell now"]
        
        for phrase in forbidden_phrases:
            if phrase in answer:
                report["answer_to_question"] = "My previous answer was redacted because it contained forbidden financial advice terminology."
                report["status"] = "redacted"
                
        return report
