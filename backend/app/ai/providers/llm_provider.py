from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import Optional, Any, List

class LLMCapabilities(BaseModel):
    supports_json_mode: bool
    supports_vision: bool
    max_input_tokens: int
    max_output_tokens: int

class LLMRequest(BaseModel):
    system_prompt: str
    user_content: Any
    temperature: float = 0.0
    max_output_tokens: Optional[int] = None
    timeout_s: float = 30.0
    request_id: str
    purpose: str
    cache_policy: Optional[str] = None

class LLMResponse(BaseModel):
    text: str
    parsed: Optional[Any] = None
    provider: str
    model: str
    model_version_if_reported: Optional[str] = None
    latency_ms: float
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    finish_reason: Optional[str] = None
    cached: bool = False
    attempt_count: int = 1
    fallback_used: bool = False
    raw_response_ref: Optional[str] = None

class ProviderHealth(BaseModel):
    status: str
    latency_ms: Optional[float] = None
    message: Optional[str] = None

class LLMProvider(ABC):
    name: str
    model: str
    capabilities: LLMCapabilities

    @abstractmethod
    def generate(self, request: LLMRequest) -> LLMResponse:
        pass

    @abstractmethod
    def generate_structured(self, request: LLMRequest, schema: type[BaseModel]) -> BaseModel:
        pass

    @abstractmethod
    def health_check(self) -> ProviderHealth:
        pass

    @abstractmethod
    def count_tokens(self, text: str) -> int:
        pass
