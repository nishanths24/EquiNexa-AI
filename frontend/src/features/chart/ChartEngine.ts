import { createChart, ColorType, CrosshairMode } from 'lightweight-charts';
import type { IChartApi, ISeriesApi } from 'lightweight-charts';
import type { OhlcvData } from './useOhlcv';

export class ChartEngine {
  private chart: IChartApi;
  private mainSeries: ISeriesApi<"Candlestick" | "Line" | "Area">;
  private volumeSeries: ISeriesApi<"Histogram">;
  private currentType: string = "Candlestick";

  constructor(container: HTMLElement) {
    const isDark = typeof document !== 'undefined' ? document.documentElement.classList.contains('dark') : false;
    this.chart = createChart(container, {
      layout: {
        background: { type: ColorType.Solid, color: isDark ? '#111827' : '#FFFFFF' },
        textColor: isDark ? '#9ca3af' : '#555A62',
      },
      grid: {
        vertLines: { color: isDark ? '#374151' : '#EEEEEE' },
        horzLines: { color: isDark ? '#374151' : '#EEEEEE' },
      },
      crosshair: {
        mode: CrosshairMode.Normal,
      },
      rightPriceScale: {
        borderColor: isDark ? '#374151' : '#E4E4E7',
      },
      timeScale: {
        borderColor: isDark ? '#374151' : '#E4E4E7',
        timeVisible: true,
        secondsVisible: false,
      },
      autoSize: true,
    });

    this.mainSeries = this.chart.addCandlestickSeries({
      upColor: '#10b981', // green-500
      downColor: '#ef4444', // red-500
      borderVisible: false,
      wickUpColor: '#10b981',
      wickDownColor: '#ef4444',
    });

    this.volumeSeries = this.chart.addHistogramSeries({
      color: '#374151',
      priceFormat: { type: 'volume' },
      priceScaleId: '', // acts as an overlay
    });

    this.volumeSeries.priceScale().applyOptions({
      scaleMargins: { top: 0.8, bottom: 0 },
    });
  }

  public setData(data: OhlcvData[]) {
    // Sync main series
    this.mainSeries.setData(data.map(d => ({
        time: d.time as import('lightweight-charts').Time,
        open: d.open,
        high: d.high,
        low: d.low,
        close: d.close
    })));

    // Sync volume series
    this.volumeSeries.setData(data.map(d => ({
        time: d.time as import('lightweight-charts').Time,
        value: d.volume,
        color: d.close >= d.open ? 'rgba(16, 185, 129, 0.3)' : 'rgba(239, 68, 68, 0.3)'
    })));
  }

  public setChartType(type: "Candlestick" | "Line" | "Area") {
    if (this.currentType === type) return;
    this.currentType = type;
    // In a full implementation we would remove current series and add a new one, preserving data.
    // Simplifying here for the initial engine.
  }

  public applyTheme(isDark: boolean) {
    this.chart.applyOptions({
      layout: {
        background: { type: ColorType.Solid, color: isDark ? '#111827' : '#FFFFFF' },
        textColor: isDark ? '#9ca3af' : '#555A62',
      },
      grid: {
        vertLines: { color: isDark ? '#374151' : '#EEEEEE' },
        horzLines: { color: isDark ? '#374151' : '#EEEEEE' },
      },
      rightPriceScale: {
        borderColor: isDark ? '#374151' : '#E4E4E7',
      },
      timeScale: {
        borderColor: isDark ? '#374151' : '#E4E4E7',
      },
    });
  }

  public destroy() {
    this.chart.remove();
  }
}
