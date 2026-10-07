import pandas as pd
import json
from typing import Dict, Any, List
from backend.app.ai.marketdata.market_data_provider import PriceFrame
from backend.app.ai.patterns.candlestick.engine import CandlestickEngine
from backend.app.ai.patterns.chart.engine import ChartPatternEngine
from backend.app.ai.patterns.evidence import EvidenceEngine
from backend.app.ai.technical.indicators import INDICATOR_CATALOGUE
from google import genai
from google.genai import types
import os

class DataDrivenChartAnalyzer:
    def __init__(self):
        self.c_engine = CandlestickEngine()
        self.ch_engine = ChartPatternEngine()
        self.ev_engine = EvidenceEngine()
        self.api_key = os.environ.get("GEMINI_API_KEY", "")
        self.client = genai.Client(api_key=self.api_key) if self.api_key else None
        
    def analyze(self, df: PriceFrame, ticker: str, period: str, interval: str) -> Dict[str, Any]:
        """
        Orchestrates Data-Driven Chart Analysis.
        1. Takes real OHLCV data.
        2. Generates FeatureSnapshot (patterns + indicators).
        3. Invokes LLM for narration based strictly on the snapshot.
        """
        if df.empty:
            return {"status": "ERROR", "reason": "Empty dataset"}
            
        # 1. Generate FeatureSnapshot
        # Last 5 bars of indicators
        rsi_func = INDICATOR_CATALOGUE["RSI"]["func"]
        rsi_series = rsi_func(df)
        
        macd_func = INDICATOR_CATALOGUE["MACD"]["func"]
        macd_dict = macd_func(df)
        
        # Patterns
        c_results = self.c_engine.detect_all(df)
        ch_results = self.ch_engine.detect_all(df)
        all_patterns = pd.concat([c_results, ch_results], axis=1)
        
        # Get active patterns on the last bar
        last_idx = -1
        active_patterns = []
        for col in all_patterns.columns:
            if all_patterns[col].iloc[last_idx] > 0:
                ev_df = self.ev_engine.compute_evidence(df, col, all_patterns[col])
                confidence = ev_df['confidence'].iloc[last_idx]
                active_patterns.append({"pattern": col, "confidence": round(confidence, 2)})
                
        last_close = df['close'].iloc[-1]
        last_rsi = rsi_series.iloc[-1]
        last_macd = macd_dict["macd"].iloc[-1]
        last_signal = macd_dict["signal"].iloc[-1]
        
        snapshot = {
            "ticker": ticker,
            "period": period,
            "interval": interval,
            "last_close": round(last_close, 2),
            "indicators": {
                "RSI": round(last_rsi, 2) if not pd.isna(last_rsi) else None,
                "MACD": round(last_macd, 2) if not pd.isna(last_macd) else None,
                "MACD_Signal": round(last_signal, 2) if not pd.isna(last_signal) else None
            },
            "active_patterns": active_patterns
        }
        
        # 2. Narration Guard & Prompt
        prompt = f"""
You are EquiNexa AI Chart Analyzer. 
You are strictly a data-driven narrative engine. Do NOT invent prices or patterns.
Use the following FeatureSnapshot to generate a brief chart analysis:

{json.dumps(snapshot, indent=2)}

Provide your response in JSON format exactly matching:
{{
  "trend_summary": "brief sentence",
  "key_observations": ["bullet 1", "bullet 2"],
  "narration": "A paragraph explaining the technical context based ONLY on the snapshot."
}}
"""
        
        sections_status = {
            "snapshot": "OK",
            "narration": "OK"
        }
        
        try:
            if not self.client:
                raise Exception("Missing API Key")
            resp = self.client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    max_output_tokens=500
                )
            )
            narrative = json.loads(resp.text)
        except Exception as e:
            sections_status["narration"] = "FAILED"
            narrative = {
                "trend_summary": "Unavailable",
                "key_observations": [],
                "narration": "Narration guard blocked response or LLM failed."
            }
            
        return {
            "status": "OK",
            "snapshot": snapshot,
            "analysis": narrative,
            "sections_status": sections_status
        }
