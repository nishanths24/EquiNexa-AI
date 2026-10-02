from typing import Dict, Any, Type
from pydantic import BaseModel, ValidationError
from backend.app.ai.providers.llm_provider import LLMProvider, LLMRequest

class PromptInjectionDefense:
    def sanitize(self, text: str) -> str:
        # Very basic check, in production use proper defenses or LLM guardrails
        forbidden = ["ignore all previous instructions", "system prompt", "you are a developer"]
        lower = text.lower()
        if any(f in lower for f in forbidden):
            raise ValueError("Potential prompt injection detected.")
        return text

class StructuredChain:
    def __init__(self, provider: LLMProvider, system_template: str):
        self.provider = provider
        self.system_template = system_template
        self.defense = PromptInjectionDefense()
        
    def execute(self, user_input: str, schema: Type[BaseModel], **kwargs) -> BaseModel:
        # Defend
        clean_input = self.defense.sanitize(user_input)
        
        # Format
        system_prompt = self.system_template.format(**kwargs)
        
        req = LLMRequest(
            system_prompt=system_prompt,
            user_content=clean_input,
            request_id="generated_id",
            purpose="structured_extraction"
        )
        
        try:
            # Generate structured
            result = self.provider.generate_structured(req, schema)
            return result
        except Exception as e:
            # Deterministic fallback behavior
            # In a real app, maybe fall back to another provider or return empty schema
            return schema.model_construct()
