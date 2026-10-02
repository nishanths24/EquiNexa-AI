import pandas as pd
from typing import Generator, Tuple

def walk_forward_split(
    df: pd.DataFrame, 
    initial_train_size: int, 
    step_size: int, 
    embargo_bars: int
) -> Generator[Tuple[pd.Index, pd.Index], None, None]:
    """
    Yields (train_indices, test_indices) for walk-forward validation with embargo.
    """
    n = len(df)
    if n <= initial_train_size + embargo_bars:
        return
        
    start_test = initial_train_size + embargo_bars
    
    while start_test < n:
        end_test = min(start_test + step_size, n)
        
        train_idx = df.index[:start_test - embargo_bars]
        test_idx = df.index[start_test:end_test]
        
        yield train_idx, test_idx
        
        start_test += step_size
