import pandas as pd
from typing import Dict, Any

def calculate_pivots_cpr(high: float, low: float, close: float) -> Dict[str, float]:
    """
    Calculate standard Pivot Points and Central Pivot Range (CPR) for the next period 
    given the High, Low, Close of the previous period.
    """
    pivot = (high + low + close) / 3.0
    bc = (high + low) / 2.0
    tc = (pivot - bc) + pivot
    
    # Standard supports and resistances
    r1 = (2 * pivot) - low
    s1 = (2 * pivot) - high
    r2 = pivot + (high - low)
    s2 = pivot - (high - low)
    r3 = high + 2 * (pivot - low)
    s3 = low - 2 * (high - pivot)
    
    return {
        "pivot": pivot,
        "tc": tc,
        "bc": bc,
        "r1": r1,
        "s1": s1,
        "r2": r2,
        "s2": s2,
        "r3": r3,
        "s3": s3
    }
