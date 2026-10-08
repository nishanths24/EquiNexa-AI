from typing import Dict, Any
from backend.app.models.domain.fundamentals import (
    FundamentalsData, IncomeStatement, FinancialStatementItem, KeyRatios
)

def normalize_fundamentals(symbol: str, raw_data: Dict[str, Any], source_name: str) -> FundamentalsData:
    """
    Phase 7 Normalization Engine.
    Maps various provider specific keys ("Total Revenue", "OperatingRevenue", "revenue") 
    into the unified format while strictly preserving the original field.
    """
    
    # Revenue Resolution
    revenue_val = 0.0
    revenue_field = "unknown"
    for key in ["Total Revenue", "OperatingRevenue", "revenue", "sales"]:
        if key in raw_data:
            revenue_val = float(raw_data[key])
            revenue_field = key
            break
            
    # Net Income Resolution
    net_val = 0.0
    net_field = "unknown"
    for key in ["Net Income", "NetIncomeLoss", "net_income"]:
        if key in raw_data:
            net_val = float(raw_data[key])
            net_field = key
            break
            
    income_stmt = IncomeStatement(
        revenue=FinancialStatementItem(
            unified_value=revenue_val,
            original_field=revenue_field,
            original_value=revenue_val,
            source=source_name
        ),
        net_income=FinancialStatementItem(
            unified_value=net_val,
            original_field=net_field,
            original_value=net_val,
            source=source_name
        )
    )
    
    # Key ratios (basic mapping for demo)
    ratios = KeyRatios(
        pe_ratio=float(raw_data.get("PERatio", raw_data.get("pe", 0.0))) or None,
        roe=float(raw_data.get("ReturnOnEquityTTM", raw_data.get("roe", 0.0))) or None
    )
    
    return FundamentalsData(
        symbol=symbol,
        income_statement=income_stmt,
        key_ratios=ratios,
        raw_response=raw_data
    )
