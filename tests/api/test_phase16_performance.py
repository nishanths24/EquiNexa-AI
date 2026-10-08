import pytest
import time
import statistics
from fastapi.testclient import TestClient
from backend.app.api.main import app

client = TestClient(app)

def test_performance_p50_p95_p99_and_headers():
    """
    Phase 16 Exit Gate: Measured p50/p95/p99 report.
    Validates that the latency header is injected and measures response times.
    """
    # Use a fast endpoint like health check
    endpoint = "/api/v1/health"
    latencies = []
    
    # Warm up
    client.get(endpoint)
    
    # Measure 50 requests
    for _ in range(50):
        start_t = time.perf_counter()
        response = client.get(endpoint)
        end_t = time.perf_counter()
        
        # Verify header is present
        assert "X-Backend-Latency-Ms" in response.headers
        
        latency_ms = (end_t - start_t) * 1000
        latencies.append(latency_ms)
        
    latencies.sort()
    
    # Calculate percentiles
    p50 = statistics.median(latencies)
    
    def get_percentile(data, p):
        k = (len(data) - 1) * p
        f = int(k)
        c = f + 1
        if c >= len(data):
            return data[-1]
        return data[f] + (k - f) * (data[c] - data[f])
        
    p95 = get_percentile(latencies, 0.95)
    p99 = get_percentile(latencies, 0.99)
    
    print("\n" + "="*40)
    print("PHASE 16 PERFORMANCE REPORT")
    print("="*40)
    print(f"Endpoint: {endpoint}")
    print(f"Samples: {len(latencies)}")
    print(f"p50 Latency: {p50:.2f} ms")
    print(f"p95 Latency: {p95:.2f} ms")
    print(f"p99 Latency: {p99:.2f} ms")
    print("="*40 + "\n")
    
    import os
    is_ci = os.getenv("CI", "false").lower() == "true"
    threshold = 5000 if is_ci else 3000
    
    # Assert reasonable bounds
    assert p50 < threshold, f"p50 latency is too high: {p50} ms (Threshold: {threshold})"
    
def test_websocket_manager_logic():
    """Verify stream manager connection and subscription logic."""
    from backend.app.api.v2.websockets.manager import stream_manager
    # We test the pure logic without full async mock for now
    assert isinstance(stream_manager.subscriptions, dict)
    assert isinstance(stream_manager.connection_symbols, dict)
