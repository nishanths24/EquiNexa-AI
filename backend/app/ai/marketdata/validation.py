import pandas as pd
from typing import List, Dict, Any
from pydantic import BaseModel

class DataIssue(BaseModel):
    issue_type: str
    description: str
    affected_rows: int
    
class DataQualityReport(BaseModel):
    score: float # [0, 1]
    issues: List[DataIssue]
    is_valid: bool

def validate_price_frame(df: pd.DataFrame) -> DataQualityReport:
    issues = []
    
    if df.empty:
        return DataQualityReport(
            score=0.0,
            issues=[DataIssue(issue_type="empty", description="DataFrame is empty", affected_rows=0)],
            is_valid=False
        )
        
    total_rows = len(df)
    
    # Check for NaN in OHLCV
    nan_counts = df[['open', 'high', 'low', 'close', 'volume']].isna().sum()
    total_nans = int(nan_counts.sum())
    if total_nans > 0:
        issues.append(DataIssue(
            issue_type="missing_data",
            description="NaN values found in OHLCV columns",
            affected_rows=total_nans
        ))
        
    # Check OHLC consistency (low <= open, close <= high)
    # Use fillna(0) just for the check to avoid errors on NaNs
    inconsistent = ((df['low'] > df['open']) | (df['low'] > df['close']) | 
                    (df['high'] < df['open']) | (df['high'] < df['close'])).sum()
    if inconsistent > 0:
        issues.append(DataIssue(
            issue_type="ohlc_inconsistency",
            description="low > open/close or high < open/close",
            affected_rows=int(inconsistent)
        ))
        
    # Check negative volume
    neg_vol = (df['volume'] < 0).sum()
    if neg_vol > 0:
        issues.append(DataIssue(
            issue_type="negative_volume",
            description="Volume cannot be negative",
            affected_rows=int(neg_vol)
        ))
        
    score = 1.0 - (len(issues) * 0.1)
    score = max(0.0, score)
    is_valid = score >= 0.8
    
    return DataQualityReport(score=score, issues=issues, is_valid=is_valid)
