import React, { useEffect, useRef } from 'react';
import { createChart, ColorType } from 'lightweight-charts';
import type { IChartApi, ISeriesApi, Time } from 'lightweight-charts';
import { calculateSMA, calculateEMA, calculateBollingerBands, calculateRSI, calculateMACD, calculateATR } from '../utils/indicators';
import type { OHLCV } from '../utils/indicators';

interface ChartWidgetProps {
  data: OHLCV[];
  type: 'candlestick' | 'line' | 'area';
  indicators: {
    sma20: boolean;
    sma50: boolean;
    sma200: boolean;
    ema12: boolean;
    ema26: boolean;
    ema50: boolean;
    bb: boolean;
    rsi: boolean;
    macd: boolean;
    atr: boolean;
  };
}

export const ChartWidget: React.FC<ChartWidgetProps> = ({ data, type, indicators }) => {
  const mainChartRef = useRef<HTMLDivElement>(null);
  const rsiChartRef = useRef<HTMLDivElement>(null);
  const macdChartRef = useRef<HTMLDivElement>(null);
  const atrChartRef = useRef<HTMLDivElement>(null);

  const chartsRef = useRef<IChartApi[]>([]);

  useEffect(() => {
    if (!mainChartRef.current || data.length === 0) return;

    chartsRef.current.forEach(c => c.remove());
    chartsRef.current = [];

    const commonOptions = {
      layout: {
        background: { type: ColorType.Solid, color: 'transparent' },
        textColor: '#d1d4dc',
      },
      grid: {
        vertLines: { color: 'rgba(42, 46, 57, 0.5)' },
        horzLines: { color: 'rgba(42, 46, 57, 0.5)' },
      },
      timeScale: {
        timeVisible: true,
        secondsVisible: false,
      },
      crosshair: {
        mode: 0,
      }
    };

    const mainChart = createChart(mainChartRef.current, commonOptions);
    chartsRef.current.push(mainChart);

    let mainSeries: ISeriesApi<any>;

    if (type === 'candlestick') {
      mainSeries = mainChart.addCandlestickSeries({
        upColor: '#26a69a',
        downColor: '#ef5350',
        borderVisible: false,
        wickUpColor: '#26a69a',
        wickDownColor: '#ef5350',
      });
      mainSeries.setData(data.map(d => ({
        time: (new Date(d.time).getTime() / 1000) as Time,
        open: d.open,
        high: d.high,
        low: d.low,
        close: d.close,
      })));
    } else if (type === 'area') {
      mainSeries = mainChart.addAreaSeries({
        lineColor: '#2962FF',
        topColor: '#2962FF',
        bottomColor: 'rgba(41, 98, 255, 0.28)',
      });
      mainSeries.setData(data.map(d => ({
        time: (new Date(d.time).getTime() / 1000) as Time,
        value: d.close,
      })));
    } else {
      mainSeries = mainChart.addLineSeries({
        color: '#2962FF',
        lineWidth: 2,
      });
      mainSeries.setData(data.map(d => ({
        time: (new Date(d.time).getTime() / 1000) as Time,
        value: d.close,
      })));
    }

    // Overlays
    if (indicators.sma20) {
      const smaData = calculateSMA(data, 20);
      const smaSeries = mainChart.addLineSeries({ color: '#f5a623', lineWidth: 1, title: 'SMA 20' });
      smaSeries.setData(smaData.map(d => ({ time: (new Date(d.time).getTime() / 1000) as Time, value: d.value })));
    }
    if (indicators.sma50) {
      const smaData = calculateSMA(data, 50);
      const smaSeries = mainChart.addLineSeries({ color: '#f8e71c', lineWidth: 1, title: 'SMA 50' });
      smaSeries.setData(smaData.map(d => ({ time: (new Date(d.time).getTime() / 1000) as Time, value: d.value })));
    }
    if (indicators.sma200) {
      const smaData = calculateSMA(data, 200);
      const smaSeries = mainChart.addLineSeries({ color: '#8b572a', lineWidth: 2, title: 'SMA 200' });
      smaSeries.setData(smaData.map(d => ({ time: (new Date(d.time).getTime() / 1000) as Time, value: d.value })));
    }
    if (indicators.ema12) {
      const emaData = calculateEMA(data, 12);
      const emaSeries = mainChart.addLineSeries({ color: '#bd10e0', lineWidth: 1, title: 'EMA 12' });
      emaSeries.setData(emaData.map(d => ({ time: (new Date(d.time).getTime() / 1000) as Time, value: d.value })));
    }
    if (indicators.ema26) {
      const emaData = calculateEMA(data, 26);
      const emaSeries = mainChart.addLineSeries({ color: '#9013fe', lineWidth: 1, title: 'EMA 26' });
      emaSeries.setData(emaData.map(d => ({ time: (new Date(d.time).getTime() / 1000) as Time, value: d.value })));
    }
    if (indicators.ema50) {
      const emaData = calculateEMA(data, 50);
      const emaSeries = mainChart.addLineSeries({ color: '#4a90e2', lineWidth: 1, title: 'EMA 50' });
      emaSeries.setData(emaData.map(d => ({ time: (new Date(d.time).getTime() / 1000) as Time, value: d.value })));
    }
    if (indicators.bb) {
      const bbData = calculateBollingerBands(data, 20, 2);
      const upperSeries = mainChart.addLineSeries({ color: 'rgba(255, 255, 255, 0.3)', lineWidth: 1, title: 'BB Upper' });
      const lowerSeries = mainChart.addLineSeries({ color: 'rgba(255, 255, 255, 0.3)', lineWidth: 1, title: 'BB Lower' });
      upperSeries.setData(bbData.map(d => ({ time: (new Date(d.time).getTime() / 1000) as Time, value: d.upper })));
      lowerSeries.setData(bbData.map(d => ({ time: (new Date(d.time).getTime() / 1000) as Time, value: d.lower })));
    }

    // Subcharts sync logic
    const syncScale = (sourceChart: IChartApi, targetChart: IChartApi) => {
      sourceChart.timeScale().subscribeVisibleLogicalRangeChange(range => {
        if (range) targetChart.timeScale().setVisibleLogicalRange(range);
      });
    };

    if (indicators.rsi && rsiChartRef.current) {
      const rsiChart = createChart(rsiChartRef.current, commonOptions);
      chartsRef.current.push(rsiChart);
      const rsiSeries = rsiChart.addLineSeries({ color: '#4a90e2', lineWidth: 2, title: 'RSI 14' });
      const rsiData = calculateRSI(data, 14);
      rsiSeries.setData(rsiData.map(d => ({ time: (new Date(d.time).getTime() / 1000) as Time, value: d.value })));
      
      // Sync
      syncScale(mainChart, rsiChart);
      syncScale(rsiChart, mainChart);
    }

    if (indicators.macd && macdChartRef.current) {
      const macdChart = createChart(macdChartRef.current, commonOptions);
      chartsRef.current.push(macdChart);
      
      const macdData = calculateMACD(data, 12, 26, 9);
      const macdSeries = macdChart.addLineSeries({ color: '#bd10e0', lineWidth: 1, title: 'MACD' });
      const signalSeries = macdChart.addLineSeries({ color: '#f5a623', lineWidth: 1, title: 'Signal' });
      const histSeries = macdChart.addHistogramSeries({
        color: '#26a69a',
        priceFormat: { type: 'volume' },
      });

      macdSeries.setData(macdData.map(d => ({ time: (new Date(d.time).getTime() / 1000) as Time, value: d.macd })));
      signalSeries.setData(macdData.map(d => ({ time: (new Date(d.time).getTime() / 1000) as Time, value: d.signal })));
      histSeries.setData(macdData.map(d => ({ 
        time: (new Date(d.time).getTime() / 1000) as Time, 
        value: d.histogram, 
        color: d.histogram > 0 ? '#26a69a' : '#ef5350' 
      })));

      syncScale(mainChart, macdChart);
      syncScale(macdChart, mainChart);
    }

    if (indicators.atr && atrChartRef.current) {
      const atrChart = createChart(atrChartRef.current, commonOptions);
      chartsRef.current.push(atrChart);
      const atrSeries = atrChart.addLineSeries({ color: '#f8e71c', lineWidth: 1, title: 'ATR 14' });
      const atrData = calculateATR(data, 14);
      atrSeries.setData(atrData.map(d => ({ time: (new Date(d.time).getTime() / 1000) as Time, value: d.value })));
      
      syncScale(mainChart, atrChart);
      syncScale(atrChart, mainChart);
    }

    mainChart.timeScale().fitContent();

    const handleResize = () => {
      chartsRef.current.forEach(c => {
        c.applyOptions({ width: mainChartRef.current?.clientWidth });
      });
    };

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      chartsRef.current.forEach(c => c.remove());
      chartsRef.current = [];
    };
  }, [data, type, indicators]);

  if (!data || data.length === 0) {
    return (
      <div 
        className="w-full h-full flex items-center justify-center text-text-muted"
        role="alert" 
        aria-live="polite"
      >
        <span>No chart data available. Please select a valid ticker or timeframe.</span>
      </div>
    );
  }

  return (
    <div 
      className="w-full h-full flex flex-col gap-2 overflow-y-auto no-scrollbar"
      role="region"
      aria-label="Interactive Market Chart"
    >
      <div 
        ref={mainChartRef} 
        className="w-full flex-shrink-0" 
        style={{ height: indicators.rsi || indicators.macd || indicators.atr ? '400px' : '100%' }}
        aria-label="Main Price Chart"
      />
      {indicators.rsi && (
        <div 
          ref={rsiChartRef} 
          className="w-full h-40 flex-shrink-0 border-t border-border-subtle pt-2"
          aria-label="RSI Indicator Panel"
        />
      )}
      {indicators.macd && (
        <div 
          ref={macdChartRef} 
          className="w-full h-40 flex-shrink-0 border-t border-border-subtle pt-2"
          aria-label="MACD Indicator Panel"
        />
      )}
      {indicators.atr && (
        <div 
          ref={atrChartRef} 
          className="w-full h-40 flex-shrink-0 border-t border-border-subtle pt-2"
          aria-label="ATR Indicator Panel"
        />
      )}
    </div>
  );
};

