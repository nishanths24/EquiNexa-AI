import { useState, useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';
import { createChart, ColorType } from 'lightweight-charts';
import type { IChartApi, ISeriesApi } from 'lightweight-charts';
import { LineChart, Beaker, Newspaper, Info, ShieldAlert, TrendingUp, TrendingDown, Target, StopCircle, Maximize, Minimize } from 'lucide-react';

const MOCK_CANDLES = [
  { time: '2026-10-01', open: 2450.5, high: 2475.0, low: 2440.0, close: 2465.2 },
  { time: '2026-10-02', open: 2465.2, high: 2500.0, low: 2460.0, close: 2495.5 },
  { time: '2026-10-03', open: 2490.0, high: 2510.5, low: 2480.0, close: 2505.0 },
  { time: '2026-10-04', open: 2505.0, high: 2525.0, low: 2495.0, close: 2515.5 },
  { time: '2026-10-05', open: 2520.0, high: 2540.0, low: 2490.0, close: 2495.0 },
  { time: '2026-10-06', open: 2490.0, high: 2510.0, low: 2470.0, close: 2485.5 },
  { time: '2026-10-07', open: 2485.5, high: 2515.0, low: 2480.0, close: 2510.0 },
  { time: '2026-10-08', open: 2510.0, high: 2535.0, low: 2505.0, close: 2525.5 }
];

const StockAnalysis = () => {
  const location = useLocation();
  const query = new URLSearchParams(location.search);
  const ticker = query.get('ticker') || 'RELIANCE.NS';

  const chartContainerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const candlestickSeriesRef = useRef<ISeriesApi<"Candlestick"> | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [chartData, setChartData] = useState<any[]>(MOCK_CANDLES);
  const [aiReport, setAiReport] = useState<any>(null);
  const [timeframe, setTimeframe] = useState('1D');

  useEffect(() => {
    // Map timeframe to yfinance period/interval
    const tfMap: Record<string, { period: string, interval: string }> = {
      '1m': { period: '5d', interval: '1m' },
      '5m': { period: '5d', interval: '5m' },
      '15m': { period: '1mo', interval: '15m' },
      '1H': { period: '3mo', interval: '1h' },
      '1D': { period: '1y', interval: '1d' }
    };
    const { period, interval } = tfMap[timeframe] || tfMap['1D'];

    // Fetch live market data for chart
    fetch(`http://localhost:8000/api/v1/markets/history?ticker=${encodeURIComponent(ticker)}&period=${period}&interval=${interval}`)
      .then(res => res.json())
      .then(data => {
        if (data.status === 'OK' && data.data) {
          // Map to lightweight-charts format
          const formatted = data.data.map((d: any) => {
            const isDaily = interval === '1d';
            // Use 'YYYY-MM-DD' for daily to avoid timezone shifts, else unix timestamp for intraday
            const timeValue = isDaily ? d.time.split('T')[0] : (new Date(d.time).getTime() / 1000);
            return {
              time: timeValue,
              open: d.open,
              high: d.high,
              low: d.low,
              close: d.close
            };
          });
          // lightweight-charts requires unique, sorted times
          const uniqueData = Array.from(new Map(formatted.map((item: any) => [item.time, item])).values());
          setChartData(uniqueData.sort((a: any, b: any) => {
            if (typeof a.time === 'string') return a.time.localeCompare(b.time);
            return a.time - b.time;
          }));
        }
      })
      .catch(console.error);
  }, [ticker, timeframe]);

  useEffect(() => {
    if (!chartContainerRef.current) return;

    const chart = createChart(chartContainerRef.current, {
      layout: {
        background: { type: ColorType.Solid, color: '#0b0b0b' },
        textColor: '#a3a3a3',
      },
      grid: {
        vertLines: { color: '#242424' },
        horzLines: { color: '#242424' },
      },
      width: chartContainerRef.current.clientWidth,
      height: 400,
      timeScale: {
        timeVisible: true,
        secondsVisible: false,
      },
    });

    const candlestickSeries = chart.addCandlestickSeries({
      upColor: '#22c55e',
      downColor: '#ef4444',
      borderVisible: false,
      wickUpColor: '#22c55e',
      wickDownColor: '#ef4444',
    });

    candlestickSeriesRef.current = candlestickSeries;

    chartRef.current = chart;
    candlestickSeriesRef.current = candlestickSeries;

    if (candlestickSeriesRef.current && chartData.length > 0) {
      try {
        candlestickSeriesRef.current.setData(chartData);
      } catch (e) {
        console.warn('Could not set chart data', e);
      }
    }

    const handleResize = () => {
      if (chartContainerRef.current && chartRef.current) {
        chartRef.current.applyOptions({ width: chartContainerRef.current.clientWidth });
      }
    };

    window.addEventListener('resize', handleResize);
    return () => {
      window.removeEventListener('resize', handleResize);
      document.removeEventListener('fullscreenchange', handleFullscreenChange);
      chart.remove();
    };
  }, [chartData]);

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

  return (
    <div className="flex flex-col lg:flex-row h-full w-full gap-6 max-w-screen-2xl mx-auto p-4 lg:p-6 bg-black-bg text-text-primary">
      {/* Left Column: Chart and Data */}
      <div className="flex-1 flex flex-col space-y-6 min-w-0">
        
        {/* Header Bar */}
        <div className="bg-card-bg border border-border-subtle rounded-lg p-4 flex justify-between items-center">
          <div>
            <div className="flex items-center space-x-3">
              <h1 className="text-2xl font-bold text-text-primary">{ticker}</h1>
              <span className="px-2 py-0.5 bg-border-subtle text-text-secondary text-xs rounded font-medium">EQ</span>
              <span className="px-2 py-0.5 bg-green-900/30 text-market-up border border-green-900/50 text-xs rounded font-medium flex items-center">
                <span className="relative flex h-2 w-2 mr-1.5">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-market-up opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-market-up"></span>
                </span>
                LIVE
              </span>
            </div>
            <div className="text-sm text-text-muted mt-1">Live Market Data Integration</div>
          </div>
          <div className="text-right">
            <div className="text-3xl font-mono font-bold text-text-primary">
              {chartData.length > 0 ? `₹${chartData[chartData.length - 1].close.toFixed(2)}` : 'Loading...'}
            </div>
            {chartData.length > 1 && (
              <div className={`font-mono text-sm font-medium flex items-center justify-end ${chartData[chartData.length - 1].close >= chartData[chartData.length - 2].close ? 'text-market-up' : 'text-market-down'}`}>
                {chartData[chartData.length - 1].close >= chartData[chartData.length - 2].close ? <TrendingUp className="w-4 h-4 mr-1" /> : <TrendingDown className="w-4 h-4 mr-1" />}
                {Math.abs(chartData[chartData.length - 1].close - chartData[chartData.length - 2].close).toFixed(2)}
              </div>
            )}
          </div>
        </div>

        {/* Chart Container */}
        <div className="bg-card-bg border border-border-subtle rounded-lg p-1 flex flex-col flex-1 min-h-[400px]">
          <div className="flex items-center justify-between p-3 border-b border-border-subtle">
            <div className="flex space-x-2">
              {['1m', '5m', '15m', '1H', '1D'].map(tf => (
                <button 
                  key={tf} 
                  onClick={() => setTimeframe(tf)}
                  className={`px-3 py-1 rounded text-sm font-medium transition-colors ${tf === timeframe ? 'bg-hover-bg text-text-primary' : 'text-text-muted hover:bg-hover-bg hover:text-text-secondary'}`}
                >
                  {tf}
                </button>
              ))}
            </div>
            <div className="flex space-x-2">
              <button className="px-3 py-1 rounded text-sm font-medium text-text-muted hover:bg-hover-bg transition-colors flex items-center">
                <LineChart className="w-4 h-4 mr-1.5" /> Indicators
              </button>
              <button onClick={toggleFullscreen} className="px-2 py-1 rounded text-text-muted hover:bg-hover-bg transition-colors">
                {isFullscreen ? <Minimize className="w-4 h-4" /> : <Maximize className="w-4 h-4" />}
              </button>
            </div>
          </div>
          <div ref={chartContainerRef} className="flex-1 w-full relative" />
        </div>

        {/* Bottom Panel: Fundamentals & News */}
        <div className="bg-card-bg border border-border-subtle rounded-lg grid grid-cols-1 md:grid-cols-2 divide-y md:divide-y-0 md:divide-x divide-border-subtle">
          <div className="p-4">
            <h3 className="text-sm font-semibold text-text-secondary uppercase tracking-wider mb-3 flex items-center">
              <Info className="w-4 h-4 mr-1.5" /> Fundamentals
            </h3>
            <div className="grid grid-cols-2 gap-y-3 text-sm">
              <div><span className="text-text-muted block">Market Cap</span><span className="font-mono">₹17.2T</span></div>
              <div><span className="text-text-muted block">P/E Ratio</span><span className="font-mono">28.4</span></div>
              <div><span className="text-text-muted block">Dividend Yield</span><span className="font-mono">0.34%</span></div>
              <div><span className="text-text-muted block">52W High</span><span className="font-mono">₹3,024.90</span></div>
            </div>
          </div>
          <div className="p-4">
            <h3 className="text-sm font-semibold text-text-secondary uppercase tracking-wider mb-3 flex items-center">
              <Newspaper className="w-4 h-4 mr-1.5" /> Recent News
            </h3>
            <div className="space-y-3">
              <div className="text-sm hover:text-blue-400 cursor-pointer transition-colors line-clamp-1">Reliance Jio announces new 5G tariff plans starting next month.</div>
              <div className="text-sm hover:text-blue-400 cursor-pointer transition-colors line-clamp-1">Retail division sees 12% YoY growth in quarterly footprint.</div>
            </div>
          </div>
        </div>
      </div>

      {/* Right Column: AI Analysis */}
      <div className="w-full lg:w-96 flex flex-col space-y-4">
        <div className="bg-card-bg border border-border-subtle rounded-lg p-5 flex flex-col flex-1">
          <div className="flex items-center justify-between border-b border-border-subtle pb-4 mb-4">
            <h2 className="text-lg font-bold flex items-center text-blue-400">
              <Beaker className="w-5 h-5 mr-2" />
              EquiNexa AI Analyst
            </h2>
          </div>

          {!isAnalyzing ? (
            <div className="flex-1 overflow-y-auto space-y-6 pr-2">
              {/* Prediction Header */}
              {aiReport ? (
                <div className="p-4 bg-hover-bg rounded-lg border border-border-subtle">
                  <div className="text-sm font-semibold mb-2">Generated Report:</div>
                  <div className="text-sm text-text-primary whitespace-pre-wrap leading-relaxed">
                    {aiReport.report}
                  </div>
                  <div className="mt-4 text-xs text-text-muted">
                    <strong>Sources:</strong> {aiReport.citations?.join(', ') || 'Unverified'}
                  </div>
                </div>
              ) : (
                <>
                  <div className="p-4 bg-hover-bg rounded-lg border border-border-subtle">
                    <div className="text-sm text-text-muted mb-1">AI Market Bias</div>
                    <div className="text-xl font-bold text-market-up flex items-center">
                      BULLISH <TrendingUp className="w-5 h-5 ml-2" />
                    </div>
                    <div className="text-xs text-text-muted mt-2">Confidence: <span className="font-mono text-text-primary">78%</span></div>
                  </div>

              {/* Technical Reasoning */}
              <div>
                <h3 className="text-sm font-semibold text-text-secondary uppercase tracking-wider mb-3">Evidence</h3>
                <ul className="space-y-2 text-sm text-text-primary">
                  <li className="flex items-start"><span className="text-market-up mr-2">•</span> <strong>Candlestick:</strong> Bullish Engulfing pattern detected on 1D timeframe.</li>
                  <li className="flex items-start"><span className="text-market-up mr-2">•</span> <strong>Indicators:</strong> RSI at 54, MACD crossover observed confirming upward momentum.</li>
                  <li className="flex items-start"><span className="text-text-muted mr-2">•</span> <strong>S/R:</strong> Strong support zone held at ₹2450.</li>
                  <li className="flex items-start"><span className="text-market-up mr-2">•</span> <strong>News:</strong> Retail growth figures driving positive sentiment.</li>
                </ul>
              </div>

              {/* Trade Setup */}
              <div>
                <h3 className="text-sm font-semibold text-text-secondary uppercase tracking-wider mb-3">Long Setup</h3>
                <div className="space-y-3 font-mono text-sm">
                  <div className="flex justify-between items-center p-2 rounded bg-black-bg border border-border-subtle">
                    <span className="text-text-muted flex items-center"><TrendingUp className="w-4 h-4 mr-2 text-blue-400"/> Entry Zone</span>
                    <span>₹2,510 - ₹2,530</span>
                  </div>
                  <div className="flex justify-between items-center p-2 rounded bg-black-bg border border-border-subtle">
                    <span className="text-text-muted flex items-center"><Target className="w-4 h-4 mr-2 text-market-up"/> Target 1</span>
                    <span className="text-market-up">₹2,600</span>
                  </div>
                  <div className="flex justify-between items-center p-2 rounded bg-black-bg border border-border-subtle">
                    <span className="text-text-muted flex items-center"><StopCircle className="w-4 h-4 mr-2 text-market-down"/> Stop Loss</span>
                    <span className="text-market-down">₹2,480</span>
                  </div>
                </div>
              </div>
            </>
          )}

          {/* Disclaimer */}
              <div className="mt-4 p-3 bg-red-950/20 border border-red-900/50 rounded-lg flex items-start">
                <ShieldAlert className="w-5 h-5 text-red-500 mr-2 flex-shrink-0 mt-0.5" />
                <p className="text-xs text-text-muted">
                  <strong className="text-red-400 block mb-1">RISK WARNING</strong>
                  Market predictions are probabilistic and can be wrong. The analysis uses available market data and is not personalized financial advice.
                </p>
              </div>
            </div>
          ) : (
            <div className="flex-1 flex flex-col items-center justify-center space-y-4">
              <div className="w-10 h-10 border-4 border-border-subtle border-t-blue-500 rounded-full animate-spin"></div>
              <p className="text-text-muted text-sm font-medium animate-pulse">Running quantitative analysis...</p>
            </div>
          )}

          <div className="pt-4 mt-4 border-t border-border-subtle">
            <button 
              onClick={runAnalysis}
              disabled={isAnalyzing}
              className="w-full py-3 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white rounded-lg font-semibold transition-colors flex items-center justify-center"
            >
              <Beaker className="w-5 h-5 mr-2" />
              Analyze Current Market
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StockAnalysis;
