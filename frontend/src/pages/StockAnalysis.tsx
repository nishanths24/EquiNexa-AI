import { useState, useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';
import { createChart, ColorType, CrosshairMode } from 'lightweight-charts';
import type { IChartApi, ISeriesApi } from 'lightweight-charts';
import { Maximize, Minimize, AlertCircle } from 'lucide-react';

const StockAnalysis = () => {
  const location = useLocation();
  const query = new URLSearchParams(location.search);
  const ticker = query.get('ticker') || 'RELIANCE.NS';

  const chartContainerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const candlestickSeriesRef = useRef<ISeriesApi<"Candlestick"> | null>(null);
  const volumeSeriesRef = useRef<ISeriesApi<"Histogram"> | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [chartData, setChartData] = useState<any[]>([]);
  const [aiReport, setAiReport] = useState<any>(null);
  const [tooltipData, setTooltipData] = useState<any>(null);
  
  // Independent Interval and Range
  const [interval, setInterval] = useState('1d');
  const [range, setRange] = useState('max');
  
  const intervals = [
    { label: '1m', value: '1m' },
    { label: '5m', value: '5m' },
    { label: '15m', value: '15m' },
    { label: '1H', value: '1h' },
    { label: '1D', value: '1d' },
    { label: '1W', value: '1wk' },
    { label: '1M', value: '1mo' },
  ];
  
  const ranges = [
    { label: '1D', value: '1d' },
    { label: '5D', value: '5d' },
    { label: '1M', value: '1mo' },
    { label: '3M', value: '3mo' },
    { label: '6M', value: '6mo' },
    { label: '1Y', value: '1y' },
    { label: '5Y', value: '5y' },
    { label: 'MAX', value: 'max' },
  ];

  useEffect(() => {
    // Fetch live market data for chart based on independent interval and period (range)
    fetch(`http://localhost:8000/api/v1/markets/history?ticker=${encodeURIComponent(ticker)}&period=${range}&interval=${interval}`)
      .then(res => res.json())
      .then(data => {
        if (data.status === 'OK' && data.data && data.data.length > 0) {
          const isDailyOrAbove = ['1d', '1wk', '1mo'].includes(interval);
          
          const formatted = data.data.map((d: any) => {
            const timeValue = isDailyOrAbove 
                ? d.time.split('T')[0] 
                : (new Date(d.time).getTime() / 1000);
                
            return {
              time: timeValue,
              open: d.open,
              high: d.high,
              low: d.low,
              close: d.close,
              value: d.volume, // volume
              color: d.close >= d.open ? 'rgba(38, 166, 154, 0.5)' : 'rgba(239, 83, 80, 0.5)' // volume color
            };
          });
          
          const uniqueData = Array.from(new Map(formatted.map((item: any) => [item.time, item])).values());
          const sorted = uniqueData.sort((a: any, b: any) => {
            if (typeof a.time === 'string') return a.time.localeCompare(b.time);
            return a.time - b.time;
          });
          
          setChartData(sorted);
        } else {
            setChartData([]); // clear old data if invalid combination
        }
      })
      .catch(err => {
          console.error(err);
          setChartData([]);
      });
  }, [ticker, interval, range]);

  useEffect(() => {
    if (!chartContainerRef.current) return;

    const chart = createChart(chartContainerRef.current, {
      layout: {
        background: { type: ColorType.Solid, color: '#121214' }, // eq-surface
        textColor: '#a1a1aa', // eq-text-secondary
      },
      grid: {
        vertLines: { color: 'rgba(39, 39, 42, 0.5)' }, // very subtle eq-border
        horzLines: { color: 'rgba(39, 39, 42, 0.5)' },
      },
      crosshair: {
        mode: CrosshairMode.Normal,
      },
      width: chartContainerRef.current.clientWidth,
      height: chartContainerRef.current.clientHeight,
      timeScale: {
        timeVisible: !['1d', '1wk', '1mo'].includes(interval),
        secondsVisible: false,
        rightOffset: 5,
        barSpacing: 8,
      },
      rightPriceScale: {
        borderColor: '#27272a', // eq-border
      }
    });

    const candlestickSeries = chart.addCandlestickSeries({
      upColor: '#16a34a',
      downColor: '#dc2626',
      borderVisible: false,
      wickUpColor: '#16a34a',
      wickDownColor: '#dc2626',
    });

    const volumeSeries = chart.addHistogramSeries({
        priceFormat: { type: 'volume' },
        priceScaleId: '',
    });
    volumeSeries.priceScale().applyOptions({
        scaleMargins: { top: 0.8, bottom: 0 },
    });

    chartRef.current = chart;
    candlestickSeriesRef.current = candlestickSeries;
    volumeSeriesRef.current = volumeSeries;

    if (chartData.length > 0) {
      try {
        candlestickSeriesRef.current.setData(chartData);
        volumeSeriesRef.current.setData(chartData);
      } catch (e) {
        console.warn('Could not set chart data', e);
      }
    }

    chart.subscribeCrosshairMove((param) => {
      if (
        param.point === undefined ||
        !param.time ||
        param.point.x < 0 ||
        param.point.x > chartContainerRef.current!.clientWidth ||
        param.point.y < 0 ||
        param.point.y > chartContainerRef.current!.clientHeight
      ) {
        setTooltipData(null);
        return;
      }

      const barData = param.seriesData.get(candlestickSeries);
      const volData = param.seriesData.get(volumeSeries);
      
      if (barData) {
        setTooltipData({
          time: param.time,
          open: (barData as any).open,
          high: (barData as any).high,
          low: (barData as any).low,
          close: (barData as any).close,
          volume: volData ? (volData as any).value : 0,
        });
      }
    });

    const handleResize = () => {
      if (chartContainerRef.current && chartRef.current) {
        chartRef.current.applyOptions({ 
            width: chartContainerRef.current.clientWidth,
            height: chartContainerRef.current.clientHeight 
        });
      }
    };

    window.addEventListener('resize', handleResize);
    return () => {
      window.removeEventListener('resize', handleResize);
      document.removeEventListener('fullscreenchange', handleFullscreenChange);
      chart.remove();
    };
  }, [chartData, interval]);

  const handleFullscreenChange = () => {
    setIsFullscreen(!!document.fullscreenElement);
  };

  useEffect(() => {
    document.addEventListener('fullscreenchange', handleFullscreenChange);
    return () => document.removeEventListener('fullscreenchange', handleFullscreenChange);
  }, []);

  const toggleFullscreen = () => {
    if (!document.fullscreenElement && chartContainerRef.current) {
      chartContainerRef.current.parentElement?.requestFullscreen().catch(err => {
        console.error(`Error attempting to enable fullscreen: ${err.message}`);
      });
    } else {
      document.exitFullscreen();
    }
  };

  const runAnalysis = async () => {
    setIsAnalyzing(true);
    try {
      const res = await fetch('http://localhost:8000/api/v1/research/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ticker, query: "Analyze current trends and give a quantitative prediction." })
      });
      const data = await res.json();
      setAiReport(data);
    } catch (e) {
      console.error(e);
    }
    setIsAnalyzing(false);
  };

  const currentPrice = chartData.length > 0 ? chartData[chartData.length - 1].close : null;
  const previousPrice = chartData.length > 1 ? chartData[chartData.length - 2].close : null;
  const priceChange = currentPrice && previousPrice ? currentPrice - previousPrice : 0;
  const priceChangePct = previousPrice ? (priceChange / previousPrice) * 100 : 0;
  const isUp = priceChange >= 0;

  return (
    <div className="flex flex-col lg:flex-row h-[calc(100vh-64px)] w-full overflow-hidden bg-eq-bg text-eq-text">
      
      {/* Center/Left: Chart Workspace */}
      <div className="flex-1 flex flex-col min-w-0 border-r border-eq-border">
        
        {/* Top Header */}
        <div className="h-16 bg-eq-surface border-b border-eq-border flex items-center justify-between px-4">
            <div className="flex items-center space-x-3">
                <h1 className="text-[16px] font-semibold">{ticker}</h1>
                <span className="text-[11px] text-eq-text-secondary border border-eq-border px-1.5 py-0.5 rounded">NSE</span>
                <span className="text-eq-green text-[11px] font-medium flex items-center ml-2">
                    <span className="h-1.5 w-1.5 rounded-full bg-eq-green mr-1.5"></span>
                    Live
                </span>
            </div>
            {currentPrice && (
                <div className="flex items-center space-x-3">
                    <div className="text-[24px] font-semibold tracking-tight">₹{currentPrice.toFixed(2)}</div>
                    <div className={`text-[13px] font-medium ${isUp ? 'text-eq-green' : 'text-eq-red'}`}>
                        {isUp ? '+' : ''}{priceChange.toFixed(2)} ({isUp ? '+' : ''}{priceChangePct.toFixed(2)}%)
                    </div>
                </div>
            )}
        </div>

        {/* Chart Toolbar (Intervals & Tools) */}
        <div className="h-10 bg-eq-surface border-b border-eq-border flex items-center justify-between px-2">
            <div className="flex items-center space-x-1">
                {intervals.map(tf => (
                    <button 
                        key={tf.value} 
                        onClick={() => setInterval(tf.value)}
                        className={`px-2 py-1 text-[13px] transition-colors ${
                            interval === tf.value 
                            ? 'text-eq-purple border-b-2 border-eq-purple font-medium' 
                            : 'text-eq-text-secondary hover:text-eq-text font-normal'
                        }`}
                    >
                        {tf.label}
                    </button>
                ))}
                
                <div className="w-px h-4 bg-eq-border mx-2"></div>
                
                <button className="px-2 py-1 text-xs font-medium text-eq-text-secondary hover:text-eq-text flex items-center">
                    Indicators
                </button>
            </div>
            <div className="flex items-center space-x-2">
                <button onClick={toggleFullscreen} className="p-1 text-eq-text-secondary hover:text-eq-text transition-colors">
                    {isFullscreen ? <Minimize className="w-4 h-4" /> : <Maximize className="w-4 h-4" />}
                </button>
            </div>
        </div>

        {/* Chart Area */}
        <div className="flex-1 relative bg-eq-surface">
            {!chartData.length && (
                <div className="absolute inset-0 flex items-center justify-center z-10 text-eq-text-muted">
                    No data available for this combination.
                </div>
            )}
            
            {/* Tooltip Overlay */}
            {tooltipData && (
                <div className="absolute top-2 left-4 z-20 flex space-x-3 text-xs font-mono pointer-events-none">
                    <span className="text-eq-text-secondary">
                        {typeof tooltipData.time === 'string' 
                            ? tooltipData.time 
                            : new Date(tooltipData.time * 1000).toLocaleString()}
                    </span>
                    <span className="text-eq-text-secondary">O <span className="text-eq-text">{tooltipData.open.toFixed(2)}</span></span>
                    <span className="text-eq-text-secondary">H <span className="text-eq-text">{tooltipData.high.toFixed(2)}</span></span>
                    <span className="text-eq-text-secondary">L <span className="text-eq-text">{tooltipData.low.toFixed(2)}</span></span>
                    <span className="text-eq-text-secondary">C <span className="text-eq-text">{tooltipData.close.toFixed(2)}</span></span>
                    <span className="text-eq-text-secondary">V <span className="text-eq-text">{tooltipData.volume > 1000000 ? (tooltipData.volume/1000000).toFixed(2)+'M' : tooltipData.volume > 1000 ? (tooltipData.volume/1000).toFixed(2)+'K' : tooltipData.volume}</span></span>
                </div>
            )}

            <div ref={chartContainerRef} className="absolute inset-0" />
        </div>

        {/* Bottom Toolbar (Range) */}
        <div className="h-10 bg-eq-surface border-t border-eq-border flex items-center px-4">
            <span className="text-xs text-eq-text-secondary mr-3 font-semibold uppercase">Range:</span>
            <div className="flex space-x-2">
                {ranges.map(r => (
                    <button 
                        key={r.value} 
                        onClick={() => setRange(r.value)}
                        className={`px-2 py-1 text-[13px] transition-colors rounded ${
                            range === r.value 
                            ? 'bg-eq-purple text-eq-text font-medium' 
                            : 'text-eq-text-secondary hover:bg-eq-surface-elevated hover:text-eq-text font-normal'
                        }`}
                    >
                        {r.label}
                    </button>
                ))}
            </div>
        </div>
      </div>

      {/* Right Column: AI Analysis */}
      <div className="w-full lg:w-[380px] flex flex-col bg-eq-surface border-l border-eq-border overflow-y-auto">
        <div className="p-4 border-b border-eq-border">
            <h2 className="text-[14px] font-semibold text-eq-purple tracking-wide">
                EquiNexa AI Analyst
            </h2>
        </div>

        <div className="p-4 flex-1 flex flex-col space-y-6">
            {!isAnalyzing ? (
                <>
                {aiReport ? (
                    <div className="space-y-4">
                        <div className="text-sm text-eq-text leading-relaxed">
                            {aiReport.report}
                        </div>
                    </div>
                ) : (
                    <>
                        {/* Summary Block */}
                        <div>
                            <div className="text-[11px] text-eq-text-secondary uppercase mb-1 tracking-wider">AI Market Bias</div>
                            <div className="text-[16px] font-semibold text-eq-green">Bullish</div>
                            <div className="text-[12px] text-eq-text-secondary mt-1">Confidence: <span className="text-eq-text font-medium">78%</span></div>
                        </div>
                        
                        {/* Evidence */}
                        <div>
                            <div className="text-xs text-eq-text-secondary uppercase mb-2 tracking-wider">Technical Signal</div>
                            <ul className="space-y-2 text-sm text-eq-text">
                                <li className="flex items-start">
                                    <span className="text-eq-green mr-2 font-bold">↑</span> 
                                    <span>Bullish Engulfing pattern on 1D.</span>
                                </li>
                                <li className="flex items-start">
                                    <span className="text-eq-green mr-2 font-bold">↑</span> 
                                    <span>RSI at 54, MACD crossover confirmed.</span>
                                </li>
                                <li className="flex items-start">
                                    <span className="text-eq-text-muted mr-2 font-bold">-</span> 
                                    <span>Strong support zone held at ₹2450.</span>
                                </li>
                            </ul>
                        </div>
                        
                        {/* Levels */}
                        <div>
                            <div className="text-xs text-eq-text-secondary uppercase mb-2 tracking-wider">Key Levels</div>
                            <div className="space-y-1 text-sm border border-eq-border rounded bg-eq-surface-elevated overflow-hidden font-medium">
                                <div className="flex justify-between items-center p-2 border-b border-eq-border">
                                    <span className="text-eq-text-secondary">Entry Zone</span>
                                    <span>₹2,510 - ₹2,530</span>
                                </div>
                                <div className="flex justify-between items-center p-2 border-b border-eq-border">
                                    <span className="text-eq-text-secondary">Target</span>
                                    <span className="text-eq-green">₹2,600</span>
                                </div>
                                <div className="flex justify-between items-center p-2">
                                    <span className="text-eq-text-secondary">Stop Loss</span>
                                    <span className="text-eq-red">₹2,480</span>
                                </div>
                            </div>
                        </div>
                    </>
                )}
                </>
            ) : (
                <div className="flex-1 flex flex-col items-center justify-center space-y-3 py-10">
                    <div className="w-8 h-8 border-2 border-eq-border border-t-eq-blue rounded-full animate-spin"></div>
                    <p className="text-eq-text-secondary text-xs font-medium animate-pulse">Running quantitative analysis...</p>
                </div>
            )}
        </div>

        <div className="p-4 border-t border-eq-border">
            {/* Disclaimer */}
            <div className="mb-4 p-2 border border-eq-orange-muted bg-[rgba(234,88,12,0.05)] rounded flex items-start">
                <AlertCircle className="w-4 h-4 text-eq-orange mr-2 flex-shrink-0 mt-0.5" />
                <p className="text-[10px] text-eq-text-secondary leading-tight">
                    <strong className="text-eq-orange block mb-0.5">RISK WARNING</strong>
                    Predictions are probabilistic. Use this tool as a reference, not as financial advice.
                </p>
            </div>
            
            <button 
              onClick={runAnalysis}
              disabled={isAnalyzing}
              className="w-full py-2 bg-eq-purple hover:bg-eq-purple-hover disabled:opacity-50 text-eq-text text-[13px] rounded font-medium transition-colors flex items-center justify-center"
            >
              Analyze Market
            </button>
        </div>
      </div>
    </div>
  );
};

export default StockAnalysis;
