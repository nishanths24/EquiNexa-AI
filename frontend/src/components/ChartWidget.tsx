import React, { useEffect, useRef } from 'react';
import { createChart, ColorType, CrosshairMode } from 'lightweight-charts';
import type { IChartApi, Time } from 'lightweight-charts';
import { calculateSMA, calculateEMA, calculateBollingerBands, calculateRSI, calculateMACD, calculateATR } from '../utils/indicators';
import type { OHLCV } from '../utils/indicators';

interface ChartWidgetProps {
  data: OHLCV[];
  type: 'candlestick' | 'line' | 'area';
  indicators: {
    sma20: boolean; sma50: boolean; sma200: boolean;
    ema12: boolean; ema26: boolean; ema50: boolean;
    bb: boolean; rsi: boolean; macd: boolean; atr: boolean;
  };
}

const toUnixSeconds = (value: string | number): number => {
  if (typeof value === 'number') return value > 1e12 ? value / 1000 : value;
  const ms = Date.parse(value);
  if (!Number.isFinite(ms)) throw new Error(`Invalid chart timestamp: ${value}`);
  return Math.floor(ms / 1000);
};

const cleanData = (rows: OHLCV[]) => {
  const byTime = new Map<number, OHLCV>();
  for (const row of rows) {
    if (![row.open, row.high, row.low, row.close, row.volume].every(Number.isFinite)) continue;
    const time = toUnixSeconds(row.time);
    byTime.set(time, { ...row, time: new Date(time * 1000).toISOString() });
  }
  return [...byTime.entries()].sort((a, b) => a[0] - b[0]).map(([time, row]) => ({ time, row }));
};

export const ChartWidget: React.FC<ChartWidgetProps> = ({ data, type, indicators }) => {
  const mainRef = useRef<HTMLDivElement>(null);
  const rsiRef = useRef<HTMLDivElement>(null);
  const macdRef = useRef<HTMLDivElement>(null);
  const atrRef = useRef<HTMLDivElement>(null);
  const chartsRef = useRef<IChartApi[]>([]);

  useEffect(() => {
    if (!mainRef.current || data.length === 0) return;
    chartsRef.current.forEach(chart => chart.remove());
    chartsRef.current = [];

    const cleaned = cleanData(data);
    if (!cleaned.length) return;

    const rows = cleaned.map(x => x.row);
    const commonOptions = {
      width: mainRef.current.clientWidth,
      height: mainRef.current.clientHeight || 480,
      layout: { background: { type: ColorType.Solid, color: '#080808' }, textColor: '#a3a3a3' },
      grid: { vertLines: { color: '#1f1f1f' }, horzLines: { color: '#1f1f1f' } },
      crosshair: { mode: CrosshairMode.Normal },
      rightPriceScale: { borderColor: '#2a2a2a', autoScale: true },
      timeScale: { borderColor: '#2a2a2a', timeVisible: true, secondsVisible: false, rightOffset: 4 },
      handleScroll: { mouseWheel: true, pressedMouseMove: true },
      handleScale: { mouseWheel: true, pinch: true, axisPressedMouseMove: true },
    } as any;

    const main = createChart(mainRef.current, commonOptions);
    chartsRef.current.push(main);

    if (type === 'candlestick') {
      const series = main.addCandlestickSeries({
        upColor: '#22c55e', downColor: '#ef4444', borderVisible: false,
        wickUpColor: '#22c55e', wickDownColor: '#ef4444',
      });
      series.setData(cleaned.map(({ time, row }) => ({ time: time as Time, open: row.open, high: row.high, low: row.low, close: row.close })));
    } else if (type === 'area') {
      const series = main.addAreaSeries({ lineColor: '#e5e7eb', topColor: 'rgba(229,231,235,0.18)', bottomColor: 'rgba(229,231,235,0.01)', lineWidth: 2 });
      series.setData(cleaned.map(({ time, row }) => ({ time: time as Time, value: row.close })));
    } else {
      const series = main.addLineSeries({ color: '#e5e7eb', lineWidth: 2 });
      series.setData(cleaned.map(({ time, row }) => ({ time: time as Time, value: row.close })));
    }

    const volume = main.addHistogramSeries({
      priceFormat: { type: 'volume' },
      priceScaleId: '',
      lastValueVisible: false,
      priceLineVisible: false,
    });
    volume.priceScale().applyOptions({ scaleMargins: { top: 0.82, bottom: 0 } });
    volume.setData(cleaned.map(({ time, row }, i) => ({
      time: time as Time, value: row.volume,
      color: i > 0 && row.close >= rows[i - 1].close ? 'rgba(34,197,94,0.35)' : 'rgba(239,68,68,0.35)',
    })));

    const overlay = (seriesData: { time: string; value: number }[], color: string, title: string) => {
      if (!seriesData.length) return;
      const series = main.addLineSeries({ color, lineWidth: 1, title });
      series.setData(seriesData.map(d => ({ time: toUnixSeconds(d.time) as Time, value: d.value })));
    };
    if (indicators.sma20) overlay(calculateSMA(rows, 20), '#f59e0b', 'SMA20');
    if (indicators.sma50) overlay(calculateSMA(rows, 50), '#fde047', 'SMA50');
    if (indicators.sma200) overlay(calculateSMA(rows, 200), '#a78bfa', 'SMA200');
    if (indicators.ema12) overlay(calculateEMA(rows, 12), '#f472b6', 'EMA12');
    if (indicators.ema26) overlay(calculateEMA(rows, 26), '#c084fc', 'EMA26');
    if (indicators.ema50) overlay(calculateEMA(rows, 50), '#60a5fa', 'EMA50');
    if (indicators.bb) {
      const bb = calculateBollingerBands(rows, 20, 2);
      overlay(bb.map(d => ({ time: d.time, value: d.upper })), '#94a3b8', 'BB Upper');
      overlay(bb.map(d => ({ time: d.time, value: d.lower })), '#94a3b8', 'BB Lower');
    }

    const makePane = (ref: React.RefObject<HTMLDivElement | null>, height: number, title: string, seriesBuilder: (chart: IChartApi) => void) => {
      if (!ref.current) return;
      const chart = createChart(ref.current, { ...commonOptions, width: ref.current.clientWidth, height });
      chartsRef.current.push(chart);
      seriesBuilder(chart);
      chart.timeScale().fitContent();
      chart.applyOptions({ watermark: { visible: true, text: title, color: '#444', fontSize: 11, horzAlign: 'left', vertAlign: 'top' } } as any);
    };

    if (indicators.rsi) {
      const rsi = calculateRSI(rows, 14);
      makePane(rsiRef, 150, 'RSI 14', chart => {
        const series = chart.addLineSeries({ color: '#60a5fa', lineWidth: 2 });
        series.setData(rsi.map(d => ({ time: toUnixSeconds(d.time) as Time, value: d.value })));
      });
    }
    if (indicators.macd) {
      const macd = calculateMACD(rows, 12, 26, 9);
      makePane(macdRef, 170, 'MACD', chart => {
        chart.addLineSeries({ color: '#c084fc', lineWidth: 1 }).setData(macd.map(d => ({ time: toUnixSeconds(d.time) as Time, value: d.macd })));
        chart.addLineSeries({ color: '#f59e0b', lineWidth: 1 }).setData(macd.map(d => ({ time: toUnixSeconds(d.time) as Time, value: d.signal })));
        chart.addHistogramSeries({ priceFormat: { type: 'price' } }).setData(macd.map(d => ({ time: toUnixSeconds(d.time) as Time, value: d.histogram, color: d.histogram >= 0 ? 'rgba(34,197,94,0.6)' : 'rgba(239,68,68,0.6)' })));
      });
    }
    if (indicators.atr) {
      const atr = calculateATR(rows, 14);
      makePane(atrRef, 150, 'ATR 14', chart => {
        chart.addLineSeries({ color: '#facc15', lineWidth: 2 }).setData(atr.map(d => ({ time: toUnixSeconds(d.time) as Time, value: d.value })));
      });
    }

    main.timeScale().fitContent();
    const observer = new ResizeObserver(() => {
      if (mainRef.current) main.applyOptions({ width: mainRef.current.clientWidth, height: mainRef.current.clientHeight || 480 });
    });
    observer.observe(mainRef.current);

    return () => {
      observer.disconnect();
      chartsRef.current.forEach(chart => chart.remove());
      chartsRef.current = [];
    };
  }, [data, type, indicators]);

  if (!data.length) return <div className="w-full h-full flex items-center justify-center text-text-muted">No chart data available.</div>;

  return (
    <div className="w-full h-full min-h-0 flex flex-col gap-2 overflow-auto" role="region" aria-label="Interactive market chart">
      <div ref={mainRef} className="w-full min-h-[460px] flex-1" aria-label="Main price chart" />
      {indicators.rsi && <div ref={rsiRef} className="w-full h-[150px] flex-shrink-0 border-t border-border-subtle" aria-label="RSI panel" />}
      {indicators.macd && <div ref={macdRef} className="w-full h-[170px] flex-shrink-0 border-t border-border-subtle" aria-label="MACD panel" />}
      {indicators.atr && <div ref={atrRef} className="w-full h-[150px] flex-shrink-0 border-t border-border-subtle" aria-label="ATR panel" />}
    </div>
  );
};
