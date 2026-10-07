import { useEffect, useRef } from 'react';
import { createChart, IChartApi, ISeriesApi, Time } from 'lightweight-charts';

export interface ChartData {
  time: string;
  open: number;
  high: number;
  low: number;
  close: number;
}

interface V2AdvancedChartProps {
  data: ChartData[];
  width?: number;
  height?: number;
}

export function V2AdvancedChart({ data, width = 600, height = 400 }: V2AdvancedChartProps) {
  const chartContainerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const seriesRef = useRef<ISeriesApi<"Candlestick"> | null>(null);

  useEffect(() => {
    if (!chartContainerRef.current) return;

    const handleResize = () => {
      chartRef.current?.applyOptions({
        width: chartContainerRef.current?.clientWidth || width,
      });
    };

    const chart = createChart(chartContainerRef.current, {
      layout: {
        background: { color: '#ffffff' },
        textColor: '#333',
      },
      grid: {
        vertLines: { color: '#f0f3fa' },
        horzLines: { color: '#f0f3fa' },
      },
      width: chartContainerRef.current.clientWidth || width,
      height,
    });

    const candlestickSeries = chart.addCandlestickSeries({
      upColor: '#26a69a',
      downColor: '#ef5350',
      borderVisible: false,
      wickUpColor: '#26a69a',
      wickDownColor: '#ef5350',
    });

    chartRef.current = chart;
    seriesRef.current = candlestickSeries;

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      chart.remove();
    };
  }, [width, height]);

  useEffect(() => {
    if (seriesRef.current && data.length > 0) {
      // Cast time to Time type for lightweight-charts
      const formattedData = data.map(d => ({
        ...d,
        time: d.time as Time
      }));
      seriesRef.current.setData(formattedData);
    }
  }, [data]);

  return (
    <div
      ref={chartContainerRef}
      data-testid="v2-advanced-chart"
      className="w-full h-full min-h-[400px] rounded-lg shadow-sm overflow-hidden"
    />
  );
}
