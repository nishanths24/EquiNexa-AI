from .llm_provider import LLMProvider, LLMRequest, LLMResponse, ProviderHealth, LLMCapabilities
from pydantic import BaseModel

class FakeLLMProvider(LLMProvider):
    def __init__(self):
        self.name = "fake"
        self.model = "fake-model-1"
        self.capabilities = LLMCapabilities(
            supports_json_mode=True,
            supports_vision=False,
            max_input_tokens=8192,
            max_output_tokens=2048
        )

    def generate(self, request: LLMRequest) -> LLMResponse:
        return LLMResponse(
            text="fake response",
            provider=self.name,
            model=self.model,
            latency_ms=10.0
        )

    def generate_structured(self, request: LLMRequest, schema: type[BaseModel]) -> BaseModel:
        # returns an empty instance of the schema for testing
        return schema.model_construct()

    def health_check(self) -> ProviderHealth:
        return ProviderHealth(status="ok", latency_ms=5.0)

    def count_tokens(self, text: str) -> int:
        return len(text.split())
