import pandas as pd
import numpy as np

def compute_triple_barrier(df: pd.DataFrame, horizon: int = 10, pt: float = 0.02, sl: float = 0.02) -> pd.Series:
    """
    Computes Triple-Barrier labels.
    - pt: Profit-taking barrier (upper, e.g. +2%)
    - sl: Stop-loss barrier (lower, e.g. -2%)
    - horizon: Time barrier (e.g. 10 bars)
    
    Returns 1 if upper barrier is touched first, -1 if lower barrier is touched first, 
    and 0 if neither is touched before the horizon.
    """
    labels = pd.Series(np.nan, index=df.index)
    
    for i in range(len(df) - horizon):
        entry_price = df['close'].iloc[i]
        upper_barrier = entry_price * (1 + pt)
        lower_barrier = entry_price * (1 - sl)
        
        # Window of future prices up to the horizon
        future_window = df.iloc[i+1 : i+1+horizon]
        
        hit_upper = future_window[future_window['high'] >= upper_barrier]
        hit_lower = future_window[future_window['low'] <= lower_barrier]
        
        if hit_upper.empty and hit_lower.empty:
            labels.iloc[i] = 0.0
        elif hit_upper.empty:
            labels.iloc[i] = -1.0
        elif hit_lower.empty:
            labels.iloc[i] = 1.0
        else:
            # Both hit, check which occurred first
            idx_upper = hit_upper.index[0]
            idx_lower = hit_lower.index[0]
            
            if idx_upper < idx_lower:
                labels.iloc[i] = 1.0
            elif idx_lower < idx_upper:
                labels.iloc[i] = -1.0
            else:
                # If hit on the same bar, assume pessimistic/stop-loss first for risk management
                labels.iloc[i] = -1.0
                
    return labels
