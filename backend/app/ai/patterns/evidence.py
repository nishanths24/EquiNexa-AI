import pandas as pd
from typing import Dict, Any
from backend.app.ai.marketdata.market_data_provider import PriceFrame

class EvidenceEngine:
    def __init__(self):
        pass
        
    def compute_evidence(self, df: PriceFrame, pattern_name: str, pattern_indices: pd.Series) -> pd.DataFrame:
        """
        Computes evidence scores for detected patterns based on volume and trend alignment.
        """
        evidence_scores = pd.Series(0.0, index=df.index)
        
        if pattern_indices.sum() == 0:
            return pd.DataFrame({"confidence": evidence_scores, "factors": [{}] * len(df)})
            
        # Calculate volume factor: volume > 30-day average volume?
        vol_sma_30 = df['volume'].rolling(window=30, min_periods=1).mean()
        vol_factor = (df['volume'] > vol_sma_30).astype(float) * 0.3
        
        # Calculate trend factor: price > 50-day SMA?
        sma_50 = df['close'].rolling(window=50, min_periods=1).mean()
        trend_up = (df['close'] > sma_50).astype(float)
        trend_down = (df['close'] < sma_50).astype(float)
        
        # Assign trend factor based on pattern typical direction
        bullish_patterns = ['hammer', 'bullish_harami', 'double_bottom']
        bearish_patterns = ['hanging_man', 'bearish_harami', 'double_top']
        
        if pattern_name in bullish_patterns:
            trend_factor = trend_down * 0.5  # Reversal is stronger if it's actually downtrending
        elif pattern_name in bearish_patterns:
            trend_factor = trend_up * 0.5    # Reversal stronger if it's actually uptrending
        else:
            trend_factor = pd.Series(0.2, index=df.index)
            
        # Base confidence
        base_confidence = 0.2
        
        evidence_scores = (base_confidence + vol_factor + trend_factor) * pattern_indices.astype(bool)
        # Cap at 1.0
        evidence_scores = evidence_scores.clip(upper=1.0)
        
        # Build factors dictionary
        factors = []
        for i in range(len(df)):
            if pattern_indices.iloc[i]:
                f = {
                    "base": base_confidence,
                    "volume_boost": round(vol_factor.iloc[i], 2),
                    "trend_boost": round(trend_factor.iloc[i], 2)
                }
                factors.append(f)
            else:
                factors.append({})
                
        return pd.DataFrame({
            "confidence": evidence_scores,
            "factors": factors
        }, index=df.index)
