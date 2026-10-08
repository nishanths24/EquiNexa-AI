import pytest
from backend.app.services.fundamentals_service import normalize_fundamentals

def test_fundamentals_schema_retention():
    """
    Phase 7 Exit Gate: schema retention of source/original field.
    We mock a response from a provider (e.g. Alpha Vantage) and ensure
    that our engine maps it to 'revenue' but explicitly retains the original 'OperatingRevenue' key.
    """
    mock_alpha_vantage_response = {
        "OperatingRevenue": "12500000000",
        "NetIncomeLoss": "3500000000",
        "PERatio": "24.5",
        "ReturnOnEquityTTM": "0.15"
    }
    
    normalized = normalize_fundamentals("AAPL", mock_alpha_vantage_response, "AlphaVantage")
    
    # Verify core normalization structure
    assert normalized.symbol == "AAPL"
    assert normalized.key_ratios.pe_ratio == 24.5
    assert normalized.key_ratios.roe == 0.15
    
    # Verify Phase 7 Exit Gate (Schema Retention)
    revenue_item = normalized.income_statement.revenue
    assert revenue_item.unified_value == 12500000000.0
    assert revenue_item.original_field == "OperatingRevenue" # <- The exact required gate
    assert revenue_item.source == "AlphaVantage"
    
    net_income_item = normalized.income_statement.net_income
    assert net_income_item.unified_value == 3500000000.0
    assert net_income_item.original_field == "NetIncomeLoss"
    
    # Verify raw response is fully retained
    assert normalized.raw_response["OperatingRevenue"] == "12500000000"

def test_fundamentals_different_provider():
    """Ensure it handles a different provider's format (e.g. Twelve Data)"""
    mock_twelve_data_response = {
        "Total Revenue": "12500000000",
        "Net Income": "3500000000",
        "pe": "24.5"
    }
    
    normalized = normalize_fundamentals("AAPL", mock_twelve_data_response, "TwelveData")
    
    assert normalized.income_statement.revenue.original_field == "Total Revenue"
    assert normalized.income_statement.net_income.original_field == "Net Income"
    assert normalized.key_ratios.pe_ratio == 24.5
