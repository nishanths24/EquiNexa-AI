# AI Analysis Setup Rules

As defined in Part G4, the AI orchestrator must map market conditions to strict setup categories.

## 1. BREAKOUT
- **Condition:** `close > resistance_zone_high AND relative_volume > threshold AND higher-TF trend != STRONGLY_BEARISH`
- **Entry Zone:** Breakout level to retest level
- **Stop Loss:** Structural invalidation (below retest low / ATR-buffered)
- **Target:** Measured move or ATR-multiple extension

## 2. BREAKDOWN
- **Condition:** `close < support_zone_low AND relative_volume > threshold AND higher-TF trend != STRONGLY_BULLISH`
- **Entry Zone:** Breakdown level to retest level
- **Stop Loss:** Structural invalidation (above retest high)
- **Target:** Measured move down

## 3. PULLBACK
- **Condition:** Price retraces to support (e.g., EMA/VWAP) within an established upward trend.
- **Entry Zone:** Support zone
- **Stop Loss:** Below support zone / ATR-buffered
- **Target:** Previous high

## 4. TREND_CONTINUATION
- **Condition:** Momentum indicators reset while structural trend holds.
- **Entry Zone:** Current consolidation phase
- **Stop Loss:** Below local structure
- **Target:** Trend extension

## 5. REVERSAL
- **Condition:** Divergence (e.g., RSI) + Reversal candle pattern + S/R rejection.
- **Entry Zone:** Confirmation of reversal structure
- **Stop Loss:** Beyond the extreme of the rejection wick
- **Target:** Next major S/R level

## 6. RANGE_TRADE
- **Condition:** Price oscillating between clear S/R bounds with flat MAs.
- **Entry Zone:** At support (for long) or resistance (for short)
- **Stop Loss:** Outside the range boundary
- **Target:** Opposite range boundary

## 7. MOMENTUM
- **Condition:** Extreme relative volume + breakout + steep MA angle.
- **Entry Zone:** Immediate momentum entry (often intraday)
- **Stop Loss:** Tight trailing stop (e.g. 1-2 ATR)
- **Target:** Trailing exit logic

## 8. MEAN_REVERSION
- **Condition:** Extreme deviation from mean (e.g., Bollinger Band pierce) + fading momentum.
- **Entry Zone:** Reversion confirmation
- **Stop Loss:** Beyond the extreme deviation
- **Target:** The mean (e.g., 20 SMA)
