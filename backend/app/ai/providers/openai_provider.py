import os
import json
from typing import Type
from pydantic import BaseModel
import openai
from backend.app.ai.providers.llm_provider import LLMProvider, LLMRequest, ProviderCapabilities

class OpenAIProvider(LLMProvider):
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
        # Require API key to be set in environment
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set. Real provider requires credentials.")
            
        self.client = openai.OpenAI(api_key=self.api_key)
        
    @property
    def capabilities(self) -> ProviderCapabilities:
        # GPT-4o-mini supports vision and structured outputs
        return ProviderCapabilities(
            supports_vision=True,
            supports_tools=True,
            supports_json_schema=True
        )
        
    def generate_structured(self, request: LLMRequest, schema: Type[BaseModel]) -> BaseModel:
        # For strict JSON schema extraction, we use response_format in openai >= 1.21
        messages = [
            {"role": "system", "content": request.system_prompt}
        ]
        
        # Format user content
        if isinstance(request.user_content, list):
            messages.append({"role": "user", "content": request.user_content})
        else:
            messages.append({"role": "user", "content": [{"type": "text", "text": request.user_content}]})
            
        response = self.client.beta.chat.completions.parse(
            model=self.model,
            messages=messages,
            response_format=schema
        )
        
        return response.choices[0].message.parsed
