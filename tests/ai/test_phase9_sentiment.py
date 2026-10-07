import pytest
from app.ai.sentiment.nlp_pipeline import NLPSentimentPipeline

def test_sentiment_validation_set():
    """
    Phase 9 Exit Gate: label/score validation set results
    """
    pipeline = NLPSentimentPipeline()
    
    validation_set = [
        ("Apple earnings beat expectations, stock surges", "Bullish"),
        ("Tesla misses delivery targets, shares drop", "Bearish"),
        ("Company X announces routine board meeting", "Neutral"),
        ("Market remains flat despite inflation data", "Neutral"),
        ("Massive profit jump for Amazon", "Bullish"),
        ("Huge loss and downgrade for Intel", "Bearish")
    ]
    
    correct = 0
    for text, expected in validation_set:
        label, score = pipeline.analyze(text)
        if label == expected:
            correct += 1
        else:
            print(f"Failed on: {text}. Expected {expected}, got {label}")
            
    # Exit gate requirement: Validate the score on the set
    accuracy = correct / len(validation_set)
    assert accuracy == 1.0, f"Validation set failed. Accuracy: {accuracy}"
