import { useState, useEffect, useRef } from 'react';
import { createChart, ColorType } from 'lightweight-charts';
import type { IChartApi, ISeriesApi } from 'lightweight-charts';
import { LineChart, DollarSign, ArrowUpRight, ArrowDownRight, RefreshCw, Activity } from 'lucide-react';

const MOCK_FOREX_PAIRS = [
  { pair: 'USD/INR', price: '83.24', change: '+0.12', percent: '+0.14%', trend: 'up' },
  { pair: 'EUR/USD', price: '1.0850', change: '-0.0020', percent: '-0.18%', trend: 'down' },
  { pair: 'GBP/USD', price: '1.2640', change: '+0.0015', percent: '+0.12%', trend: 'up' },
  { pair: 'USD/JPY', price: '148.50', change: '-0.45', percent: '-0.30%', trend: 'down' },
  { pair: 'AUD/USD', price: '0.6520', change: '+0.0030', percent: '+0.46%', trend: 'up' },
  { pair: 'USD/CHF', price: '0.8840', change: '-0.0010', percent: '-0.11%', trend: 'down' }
];

const MOCK_LINE_DATA = [
  { time: '2026-10-01', value: 83.10 },
  { time: '2026-10-02', value: 83.15 },
  { time: '2026-10-03', value: 83.05 },
  { time: '2026-10-04', value: 83.20 },
  { time: '2026-10-05', value: 83.18 },
  { time: '2026-10-06', value: 83.25 },
  { time: '2026-10-07', value: 83.22 },
  { time: '2026-10-08', value: 83.24 }
];

const Forex = () => {
  const chartContainerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const lineSeriesRef = useRef<ISeriesApi<"Line"> | null>(null);
  const [activePair, setActivePair] = useState(MOCK_FOREX_PAIRS[0]);
  const [isUpdating, setIsUpdating] = useState(false);

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
      height: 450,
      timeScale: {
        timeVisible: true,
        secondsVisible: false,
      },
    });

    const lineSeries = chart.addLineSeries({
      color: '#3b82f6', // blue-500
      lineWidth: 2,
      crosshairMarkerVisible: true,
      crosshairMarkerRadius: 4,
    });

    lineSeries.setData(MOCK_LINE_DATA as any);

    chartRef.current = chart;
    lineSeriesRef.current = lineSeries;

    const handleResize = () => {
      if (chartContainerRef.current && chartRef.current) {
        chartRef.current.applyOptions({ width: chartContainerRef.current.clientWidth });
      }
    };

    window.addEventListener('resize', handleResize);
    return () => {
      window.removeEventListener('resize', handleResize);
      chart.remove();
    };
  }, []);

  const refreshData = () => {
    setIsUpdating(true);
    setTimeout(() => setIsUpdating(false), 1000);
  };

  return (
    <div className="flex flex-col h-full bg-black-bg text-text-primary p-4 lg:p-6 max-w-screen-2xl mx-auto w-full space-y-6">
      
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between md:items-center gap-4">
        <div>
          <h1 className="text-2xl font-bold flex items-center">
            <DollarSign className="w-6 h-6 mr-2 text-blue-500" /> Global Forex Markets
          </h1>
          <p className="text-sm text-text-muted mt-1">Real-time currency exchange rates and historical trends.</p>
        </div>
        
        <button 
          onClick={refreshData}
          disabled={isUpdating}
          className="flex items-center px-4 py-2 bg-card-bg border border-border-subtle hover:bg-hover-bg rounded-md text-sm font-medium transition-colors disabled:opacity-50"
        >
          <RefreshCw className={`w-4 h-4 mr-2 ${isUpdating ? 'animate-spin' : ''}`} />
          Refresh Rates
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 flex-1">
        
        {/* Left Column: Currency Pairs List */}
        <div className="lg:col-span-1 bg-card-bg border border-border-subtle rounded-lg flex flex-col h-full">
          <div className="p-4 border-b border-border-subtle bg-hover-bg rounded-t-lg">
            <h2 className="text-sm font-semibold uppercase tracking-wider text-text-secondary flex items-center">
              <Activity className="w-4 h-4 mr-2" /> Live Rates
            </h2>
          </div>
          <div className="flex-1 overflow-y-auto p-2 space-y-1">
            {MOCK_FOREX_PAIRS.map((pair) => (
              <button
                key={pair.pair}
                onClick={() => setActivePair(pair)}
                className={`w-full text-left p-3 rounded-lg flex justify-between items-center transition-colors ${
                  activePair.pair === pair.pair 
                    ? 'bg-blue-900/20 border border-blue-500/30' 
                    : 'hover:bg-hover-bg border border-transparent'
                }`}
              >
                <div>
                  <div className="font-bold text-text-primary">{pair.pair}</div>
                  <div className="text-xs text-text-muted mt-0.5">FX Provider</div>
                </div>
                <div className="text-right">
                  <div className="font-mono font-medium">{pair.price}</div>
                  <div className={`text-xs font-mono font-medium flex items-center justify-end mt-0.5 ${pair.trend === 'up' ? 'text-market-up' : 'text-market-down'}`}>
                    {pair.trend === 'up' ? <ArrowUpRight className="w-3 h-3 mr-0.5" /> : <ArrowDownRight className="w-3 h-3 mr-0.5" />}
                    {pair.percent}
                  </div>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Right Column: Main Chart area */}
        <div className="lg:col-span-3 flex flex-col space-y-4">
          
          {/* Active Pair Stats */}
          <div className="bg-card-bg border border-border-subtle rounded-lg p-5 flex justify-between items-center">
            <div>
              <div className="text-sm text-text-muted mb-1">Current Rate</div>
              <div className="flex items-end space-x-3">
                <span className="text-3xl font-mono font-bold">{activePair.price}</span>
                <span className={`font-mono text-sm font-medium mb-1 flex items-center ${activePair.trend === 'up' ? 'text-market-up' : 'text-market-down'}`}>
                  {activePair.change} ({activePair.percent})
                </span>
              </div>
            </div>
            
            <div className="flex items-center space-x-2">
              <span className="px-2 py-0.5 bg-green-900/30 text-market-up border border-green-900/50 text-xs rounded font-medium flex items-center">
                <span className="relative flex h-2 w-2 mr-1.5">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-market-up opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-market-up"></span>
                </span>
                LIVE FEED
              </span>
            </div>
          </div>

          {/* Chart */}
          <div className="bg-card-bg border border-border-subtle rounded-lg p-1 flex-1 flex flex-col min-h-[450px]">
             <div className="flex items-center justify-between p-3 border-b border-border-subtle">
               <h3 className="text-sm font-semibold text-text-primary flex items-center">
                 <LineChart className="w-4 h-4 mr-2 text-text-muted" />
                 {activePair.pair} Line Chart
               </h3>
               <div className="flex space-x-1">
                 {['1H', '4H', '1D', '1W'].map(tf => (
                   <button key={tf} className={`px-2.5 py-1 rounded text-xs font-medium transition-colors ${tf === '1D' ? 'bg-hover-bg text-text-primary' : 'text-text-muted hover:bg-hover-bg hover:text-text-secondary'}`}>
                     {tf}
                   </button>
                 ))}
               </div>
             </div>
             <div ref={chartContainerRef} className="flex-1 w-full relative" />
          </div>

        </div>

      </div>
    </div>
  );
};

export default Forex;
