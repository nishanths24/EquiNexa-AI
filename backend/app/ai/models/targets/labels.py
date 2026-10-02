import pandas as pd
import numpy as np
from typing import Literal

def compute_labels(df: pd.DataFrame, horizon: int, threshold: float = 0.0) -> pd.Series:
    """
    Compute classification labels: 1 for UP, 0 for DOWN, based on future return over `horizon` bars.
    Label is aligned such that the label for row t uses price at t+horizon.
    """
    future_return = df['close'].pct_change(horizon).shift(-horizon)
    labels = np.where(future_return > threshold, 1.0, 0.0)
    
    # Set the last `horizon` rows to NaN
    labels[-horizon:] = np.nan
    return pd.Series(labels, index=df.index)

def compute_multiclass_labels(df: pd.DataFrame, horizon: int, threshold_up: float, threshold_down: float) -> pd.Series:
    future_return = df['close'].pct_change(horizon).shift(-horizon)
    
    conditions = [
        future_return > threshold_up,
        future_return < threshold_down
    ]
    choices = [1, -1] # 1=UP, -1=DOWN, 0=NEUTRAL
    
    labels = np.select(conditions, choices, default=0)
    labels = labels.astype(float)
    labels[-horizon:] = np.nan
    
    return pd.Series(labels, index=df.index)
