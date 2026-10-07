# ADR 0001: Chart Engine Selection

**Date**: 2026-10-03  
**Status**: Accepted  

## Context
Phase 5 of the EquiNexa AI trading platform upgrade requires a robust Charting Workspace supporting candlestick, OHLC, line, and area charts, a volume pane, synchronised panes, crosshair tooltips, and dynamic interval and range selection. The engine must perform well with thousands of OHLC bars.

## Options Considered
1. **TradingView Lightweight Charts**: Small bundle, canvas-based, excellent performance for time-series data. Has candlestick, OHLC, line, area, and histogram (volume). Does not have built-in drawing tools or indicators, so these must be implemented natively. Open-source license allows usage with attribution.
2. **KLineChart**: Open-source with built-in indicators and drawings, but has a larger bundle and smaller community/ecosystem.
3. **Apache ECharts**: Very flexible, but large bundle and custom candlestick implementation is heavier.
4. **Recharts**: Already installed for simple line charts, but inadequate for performance-intensive OHLC candlestick rendering with >5,000 bars.

## Decision
We select **TradingView Lightweight Charts (`lightweight-charts`)**. 

It is already present in `package.json` (`v4.2.3`), meaning minimal bundle delta. It provides the best performance/size trade-off. We will build a `ChartEngine` adapter around it to encapsulate its API, making it easier to mock or replace later if required.

## Consequences
- **Pros**: High FPS during pan/zoom; small bundle footprint; mobile gestures work natively.
- **Cons**: We must implement our own indicator pane layout, Heikin-Ashi transform, and drawing tools manually over the base API. 
- **Mitigation**: The `ChartEngine` adapter pattern shields the rest of the React application from these complexities.
