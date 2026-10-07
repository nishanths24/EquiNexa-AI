import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { AlertCircle, TrendingUp } from 'lucide-react';
import { fetchHistory, type OHLCV } from '../services/api/markets';
import { ChartWidget } from '../components/ChartWidget';
import ReactMarkdown from 'react-markdown';

const PERIODS = [
  { label: '1D', value: '1D' },
  { label: '5D', value: '5D' },
  { label: '1M', value: '1M' },
  { label: '3M', value: '3M' },
  { label: '6M', value: '6M' },
  { label: 'YTD', value: 'YTD' },
  { label: '1Y', value: '1Y' },
  { label: '5Y', value: '5Y' },
  { label: 'Max', value: 'MAX' }
];

const INTERVALS = [
  { label: '1m', value: '1m' },
  { label: '5m', value: '5m' },
  { label: '15m', value: '15m' },
  { label: '30m', value: '30m' },
  { label: '1h', value: '1h' },
  { label: '1d', value: '1d' },
  { label: '1wk', value: '1wk' },
  { label: '1mo', value: '1mo' }
];

const StockAnalysis = () => {
  const [searchParams] = useSearchParams();
  const ticker = searchParams.get('ticker');
  
  const [chartData, setChartData] = useState<OHLCV[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [analysisLoading, setAnalysisLoading] = useState(false);
  const [analysisError, setAnalysisError] = useState<string | null>(null);
  const [analysisResult, setAnalysisResult] = useState<string | null>(null);

  const [period, setPeriod] = useState('3M');
  const [interval, setInterval] = useState('1d');
  const [chartType, setChartType] = useState<'candlestick' | 'line' | 'area'>('candlestick');

  const [indicators, setIndicators] = useState({
    sma20: false,
    sma50: false,
    sma200: false,
    ema12: false,
    ema26: false,
    ema50: false,
    bb: false,
    rsi: false,
    macd: false,
    atr: false
  });

  useEffect(() => {
    if (!ticker) return;
    
    const loadData = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await fetchHistory(ticker, period, interval);
        setChartData(data);
      } catch (err: any) {
        setError(err.message || 'Failed to fetch historical data');
      } finally {
        setLoading(false);
      }
    };
    
    loadData();
  }, [ticker, period, interval]);

  if (!ticker) {
    return (
      <div className="space-y-6 max-w-5xl">
        <div>
          <h1 className="text-2xl font-bold text-text-primary">Stock Analysis</h1>
          <p className="text-text-secondary mt-1">Select a ticker to view technicals and prospective predictions.</p>
        </div>
        <div className="bg-card-bg border border-border-subtle rounded-xl p-12 text-center flex flex-col items-center">
          <TrendingUp className="w-12 h-12 text-text-muted mb-4" />
          <h3 className="text-lg font-medium text-text-primary">No Ticker Selected</h3>
          <p className="text-text-secondary mt-2">Use the search bar above to select a company.</p>
        </div>
      </div>
    );
  }

  const toggleIndicator = (key: keyof typeof indicators) => {
    setIndicators(prev => ({ ...prev, [key]: !prev[key] }));
  };

  return (
    <div className="space-y-6 max-w-5xl">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-text-primary">{ticker} Analysis</h1>
          <p className="text-text-secondary mt-1">Historical data and technical overview.</p>
        </div>
      </div>
      
      {error && (
        <div className="bg-red-950/30 border border-market-down/50 rounded-lg p-4 flex items-start text-market-down">
          <AlertCircle className="w-5 h-5 mr-3 mt-0.5 flex-shrink-0" />
          <p className="text-sm">{error}</p>
        </div>
      )}

      {/* Toolbar */}
      <div className="bg-card-bg p-4 rounded-xl border border-border-subtle shadow-sm flex flex-wrap gap-4 items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="text-xs font-medium text-text-muted uppercase tracking-wider">Period</span>
          <div className="flex bg-black-bg rounded-lg border border-border-subtle overflow-hidden">
            {PERIODS.map(p => (
              <button
                key={p.value}
                onClick={() => setPeriod(p.value)}
                className={`px-3 py-1.5 text-xs font-medium transition-colors ${period === p.value ? 'bg-text-primary text-black-bg' : 'text-text-secondary hover:bg-border-subtle'}`}
              >
                {p.label}
              </button>
            ))}
          </div>
        </div>

        <div className="flex items-center gap-2">
          <span className="text-xs font-medium text-text-muted uppercase tracking-wider">Interval</span>
          <select 
            value={interval}
            onChange={(e) => setInterval(e.target.value)}
            className="bg-black-bg border border-border-subtle rounded-md px-2 py-1 text-sm text-text-primary focus:outline-none focus:ring-1 focus:ring-text-secondary"
          >
            {INTERVALS.map(i => <option key={i.value} value={i.value}>{i.label}</option>)}
          </select>
        </div>

        <div className="flex items-center gap-2">
          <span className="text-xs font-medium text-text-muted uppercase tracking-wider">Type</span>
          <select 
            value={chartType}
            onChange={(e) => setChartType(e.target.value as any)}
            className="bg-black-bg border border-border-subtle rounded-md px-2 py-1 text-sm text-text-primary focus:outline-none focus:ring-1 focus:ring-text-secondary"
          >
            <option value="candlestick">Candlestick</option>
            <option value="line">Line</option>
            <option value="area">Area</option>
          </select>
        </div>
      </div>

      <div className="bg-card-bg p-4 rounded-xl border border-border-subtle shadow-sm flex flex-wrap gap-2 items-center">
        <span className="text-xs font-medium text-text-muted uppercase tracking-wider mr-2">Indicators</span>
        {Object.keys(indicators).map(key => (
          <button
            key={key}
            onClick={() => toggleIndicator(key as any)}
            className={`px-3 py-1 text-xs rounded-full border transition-colors ${
              indicators[key as keyof typeof indicators] 
                ? 'bg-text-primary text-black-bg border-text-primary font-medium' 
                : 'bg-black-bg text-text-secondary border-border-subtle hover:border-text-muted'
            }`}
          >
            {key.toUpperCase()}
          </button>
        ))}
      </div>

      <div className="bg-card-bg p-6 rounded-xl border border-border-subtle shadow-sm h-[500px] flex flex-col">
        {loading ? (
          <div className="w-full h-full flex items-center justify-center">
            <div className="w-6 h-6 border-2 border-text-primary border-t-transparent rounded-full animate-spin"></div>
          </div>
        ) : chartData.length > 0 ? (
          <ChartWidget data={chartData} type={chartType} indicators={indicators} />
        ) : (
           <div className="w-full h-full flex items-center justify-center text-text-muted">No historical data available</div>
        )}
      </div>

      <div className="bg-card-bg border border-border-subtle rounded-xl p-8">
        <div className="flex justify-between items-center mb-6">
          <h3 className="text-xl font-semibold text-text-primary">Forecast / Analysis</h3>
          <button
            onClick={async () => {
              setAnalysisLoading(true);
              setAnalysisError(null);
              try {
                const { fetchClient } = await import('../services/api/client');
                const data = await fetchClient('/api/v1/research/query', {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({ 
                    ticker: ticker, 
                    query: `Provide a comprehensive technical and AI forecast for this ticker over a ${period} period using a ${interval} interval. Focus on technical indicators, chart patterns, current news, and calibrated probabilities.` 
                  })
                });
                setAnalysisResult(data.report);
              } catch (err: any) {
                setAnalysisError(err.message || 'Analysis failed');
              } finally {
                setAnalysisLoading(false);
              }
            }}
            disabled={analysisLoading}
            className="px-4 py-2 bg-text-primary text-black-bg rounded-lg font-medium hover:bg-white transition-colors disabled:opacity-50"
          >
            {analysisLoading ? 'Analyzing...' : 'Generate Analysis'}
          </button>
        </div>

        {analysisError && (
          <div className="bg-red-950/30 border border-market-down/50 rounded-lg p-4 flex items-start text-market-down mb-4">
            <AlertCircle className="w-5 h-5 mr-3 mt-0.5 flex-shrink-0" />
            <p className="text-sm">{analysisError}</p>
          </div>
        )}

        {analysisResult ? (
          <div className="text-text-primary text-sm leading-relaxed whitespace-pre-wrap max-w-none">
            <ReactMarkdown
              components={{
                h1: ({...props}) => <h1 className="text-2xl font-bold mt-6 mb-3" {...props} />,
                h2: ({...props}) => <h2 className="text-xl font-bold mt-5 mb-3" {...props} />,
                h3: ({...props}) => <h3 className="text-lg font-semibold mt-4 mb-2" {...props} />,
                p: ({...props}) => <p className="mb-4" {...props} />,
                ul: ({...props}) => <ul className="list-disc list-inside mb-4" {...props} />,
                ol: ({...props}) => <ol className="list-decimal list-inside mb-4" {...props} />,
                li: ({...props}) => <li className="mb-1" {...props} />,
                a: ({...props}) => <a className="text-blue-400 hover:underline" target="_blank" rel="noopener noreferrer" {...props} />,
                strong: ({...props}) => <strong className="font-bold text-white" {...props} />,
              }}
            >
              {analysisResult}
            </ReactMarkdown>
          </div>
        ) : (
          <div className="text-center text-text-muted py-8">
            <TrendingUp className="w-12 h-12 text-text-muted mx-auto mb-4 opacity-50" />
            <p>Click Generate Analysis to run the prospective model and technical pattern engines.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default StockAnalysis;
