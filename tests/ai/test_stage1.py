import pytest
from pydantic import BaseModel
from datetime import datetime

from backend.app.ai.schemas.base import ErrorResponse, ErrorEnvelope, ProviderHealth
from backend.app.ai.schemas.canonical import PredictionOutput, CanonicalResponse
from backend.app.ai.safety.forbidden_phrases import LanguageLinter
from backend.app.ai.providers.fake_llm import FakeLLMProvider
from backend.app.ai.providers.llm_provider import LLMRequest

def test_language_linter():
    linter = LanguageLinter()
    assert not linter.contains_forbidden("This is a safe neutral sentence.")
    
    with pytest.raises(ValueError):
        linter.lint("This is a 100% accurate system.")
    
    with pytest.raises(ValueError):
        linter.lint("You should buy AAPL now!")

def test_fake_llm_provider():
    provider = FakeLLMProvider()
    request = LLMRequest(
        system_prompt="sys",
        user_content="user",
        request_id="test1",
        purpose="test"
    )
    
    resp = provider.generate(request)
    assert resp.text == "fake response"
    assert resp.provider == "fake"
    
    class DummySchema(BaseModel):
        field: str = "default"
        
    structured = provider.generate_structured(request, DummySchema)
    assert isinstance(structured, DummySchema)
    
    health = provider.health_check()
    assert health.status == "ok"
    
    assert provider.count_tokens("hello world") == 2
