import { createChart, ColorType, CrosshairMode } from 'lightweight-charts';
import type { IChartApi, ISeriesApi } from 'lightweight-charts';
import type { OhlcvData } from './useOhlcv';

export class ChartEngine {
  private chart: IChartApi;
  private mainSeries: ISeriesApi<any>;
  private volumeSeries: ISeriesApi<"Histogram">;
  private currentType: string = "Candlestick";
  private cachedData: OhlcvData[] = [];

  constructor(container: HTMLElement) {
    this.chart = createChart(container, {
      layout: {
        background: { type: ColorType.Solid, color: '#111827' }, // tailwind gray-900
        textColor: '#9ca3af', // tailwind gray-400
      },
      grid: {
        vertLines: { color: '#374151' },
        horzLines: { color: '#374151' },
      },
      crosshair: {
        mode: CrosshairMode.Normal,
      },
      rightPriceScale: {
        borderColor: '#374151',
      },
      timeScale: {
        borderColor: '#374151',
        timeVisible: true,
        secondsVisible: false,
      },
      autoSize: true,
    });

    this.mainSeries = this.createMainSeries("Candlestick");

    this.volumeSeries = this.chart.addHistogramSeries({
      color: '#374151',
      priceFormat: { type: 'volume' },
      priceScaleId: '', // acts as an overlay
    });

    this.volumeSeries.priceScale().applyOptions({
      scaleMargins: { top: 0.8, bottom: 0 },
    });
  }

  private createMainSeries(type: string): ISeriesApi<any> {
    if (type === 'Line') {
      return this.chart.addLineSeries({
        color: '#3b82f6',
        lineWidth: 2,
      });
    } else if (type === 'Area') {
      return this.chart.addAreaSeries({
        lineColor: '#3b82f6',
        topColor: 'rgba(59, 130, 246, 0.4)',
        bottomColor: 'rgba(59, 130, 246, 0.0)',
        lineWidth: 2,
      });
    } else {
      return this.chart.addCandlestickSeries({
        upColor: '#10b981', // green-500
        downColor: '#ef4444', // red-500
        borderVisible: false,
        wickUpColor: '#10b981',
        wickDownColor: '#ef4444',
      });
    }
  }

  public setData(data: OhlcvData[]) {
    this.cachedData = data;
    this.renderData();
  }

  private renderData() {
    const data = this.cachedData;
    if (this.currentType === 'Line' || this.currentType === 'Area') {
      this.mainSeries.setData(data.map(d => ({
        time: d.time as import('lightweight-charts').Time,
        value: d.close,
      })));
    } else {
      this.mainSeries.setData(data.map(d => ({
        time: d.time as import('lightweight-charts').Time,
        open: d.open,
        high: d.high,
        low: d.low,
        close: d.close,
      })));
    }

    this.volumeSeries.setData(data.map(d => ({
      time: d.time as import('lightweight-charts').Time,
      value: d.volume,
      color: d.close >= d.open ? 'rgba(16, 185, 129, 0.3)' : 'rgba(239, 68, 68, 0.3)',
    })));
  }

  public setChartType(type: string) {
    if (this.currentType === type) return;
    this.currentType = type;
    this.chart.removeSeries(this.mainSeries);
    this.mainSeries = this.createMainSeries(type);
    this.renderData();
  }

  public destroy() {
    this.chart.remove();
  }
}
