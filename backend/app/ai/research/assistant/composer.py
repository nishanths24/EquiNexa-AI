import json
import os
from typing import Dict, Any, List
from google import genai
from google.genai import types

class AnswerComposer:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY", "")
        self.client = genai.Client(api_key=self.api_key) if self.api_key else None
        
    def compose(self, plan: Dict[str, Any], evidence: Dict[str, Any]) -> Dict[str, Any]:
        """
        Uses the LLM to compose a response strictly from evidence.
        """
        query = plan.get("query_echo", "")
        
        prompt = f"""
You are the EquiNexa AI Research Assistant.
Answer the following question: "{query}"

Use ONLY the following evidence:
{json.dumps(evidence, indent=2)}

If the question asks for something not in the evidence, or if the question is out of scope (e.g., "should I buy?"), 
politely state that you cannot provide that information or financial advice, and provide what you do know based on the evidence.

Provide your response in JSON matching:
{{
  "answer": "Your composed answer in Markdown.",
  "unverified": ["list", "of", "missing facts"],
  "status": "success"
}}
"""
        
        try:
            if not self.client:
                raise Exception("Missing LLM Client")
                
            resp = self.client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    max_output_tokens=1024
                )
            )
            data = json.loads(resp.text)
            return {
                "query_echo": query,
                "answer_to_question": data.get("answer", ""),
                "unverified": data.get("unverified", []),
                "evidence": evidence,
                "status": data.get("status", "success")
            }
        except Exception as e:
            # Degraded fallback mode
            return {
                "query_echo": query,
                "answer_to_question": f"I encountered an error or am currently running in degraded mode. Here is the raw evidence I found: \n```json\n{json.dumps(evidence, indent=2)}\n```",
                "unverified": ["LLM processing failed."],
                "evidence": evidence,
                "status": "degraded"
            }
