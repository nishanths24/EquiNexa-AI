import os
from pathlib import Path

def test_docs_exist():
    base_dir = Path(__file__).parent.parent.parent / "docs"
    
    provider_doc = base_dir / "provider_verification.md"
    benchmark_doc = base_dir / "benchmark_claims.md"
    model_card = base_dir / "model_cards" / "model_card_1.0.0.md"
    
    assert provider_doc.exists(), "provider_verification.md is missing"
    assert benchmark_doc.exists(), "benchmark_claims.md is missing"
    assert model_card.exists(), "model_card_1.0.0.md is missing"
    
    assert provider_doc.stat().st_size > 0
    assert benchmark_doc.stat().st_size > 0
    assert model_card.stat().st_size > 0

def test_model_card_content():
    model_card = Path(__file__).parent.parent.parent / "docs" / "model_cards" / "model_card_1.0.0.md"
    content = model_card.read_text(encoding="utf-8")
    
    assert "1.0.0" in content, "Model card must identify version 1.0.0"
    assert "0" in content, "Model card must mention 0 evaluated observations"
    assert "LOCKED" in content, "Model card must mention the gate is locked"

def test_benchmark_claims_content():
    benchmark_doc = Path(__file__).parent.parent.parent / "docs" / "benchmark_claims.md"
    content = benchmark_doc.read_text(encoding="utf-8")
    
    assert "UNVERIFIED" in content or "NOT REPRODUCED" in content, "Benchmark claims must explicitly state unverified status for the 96% claim"
