from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class FinancialStatementItem(BaseModel):
    """
    Phase 7 Normalization requirement: Schema retention of source/original field.
    """
    unified_value: float
    original_field: str
    original_value: float
    source: str

class IncomeStatement(BaseModel):
    revenue: FinancialStatementItem
    net_income: FinancialStatementItem
    operating_income: Optional[FinancialStatementItem] = None

class BalanceSheet(BaseModel):
    total_assets: FinancialStatementItem
    total_liabilities: FinancialStatementItem
    total_equity: FinancialStatementItem

class CashFlow(BaseModel):
    operating_cash_flow: FinancialStatementItem
    free_cash_flow: Optional[FinancialStatementItem] = None

class KeyRatios(BaseModel):
    pe_ratio: Optional[float] = None
    pb_ratio: Optional[float] = None
    ps_ratio: Optional[float] = None
    peg_ratio: Optional[float] = None
    roe: Optional[float] = None
    roce: Optional[float] = None
    debt_to_equity: Optional[float] = None
    current_ratio: Optional[float] = None
    quick_ratio: Optional[float] = None
    dividend_yield: Optional[float] = None

class FundamentalsData(BaseModel):
    """Phase 7: Master Fundamentals Model (E9)"""
    symbol: str
    income_statement: Optional[IncomeStatement] = None
    balance_sheet: Optional[BalanceSheet] = None
    cash_flow: Optional[CashFlow] = None
    key_ratios: Optional[KeyRatios] = None
    
    # Store the raw JSON from the provider directly for the V1->V2 frozen ledger audit
    raw_response: Dict[str, Any] = Field(default_factory=dict)
