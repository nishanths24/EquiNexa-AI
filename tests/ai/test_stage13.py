import pytest
from backend.app.ai.vision.processor import VisionProcessor
from backend.app.ai.providers.fake_llm import FakeLLMProvider

def test_vision_processor():
    provider = FakeLLMProvider()
    # By default fake provider has supports_vision=False
    processor = VisionProcessor(provider)
    
    val_res = processor.validate_image(b"fakebytes", "image/png")
    assert val_res.is_valid
    
    val_res2 = processor.validate_image(b"fakebytes", "application/pdf")
    assert not val_res2.is_valid
    
    interp = processor.interpret_chart(b"fakebytes")
    assert not interp.has_sufficient_evidence
    assert interp.reasoning == "Vision not supported by provider."
    
    # Test with vision capable provider
    provider.capabilities.supports_vision = True
    interp2 = processor.interpret_chart(b"fakebytes")
    # Fake structured generator just constructs an empty instance
    # bool default is False for has_sufficient_evidence
    assert not interp2.has_sufficient_evidence
