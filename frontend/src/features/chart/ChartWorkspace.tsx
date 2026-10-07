import React, { useEffect, useRef, useState } from 'react';
import { ChartEngine } from './ChartEngine';
import { useOhlcv } from './useOhlcv';

interface ChartWorkspaceProps {
  ticker: string;
}

const INTERVALS = ['1m', '5m', '15m', '30m', '1h', '1d', '1wk', '1mo'];
const RANGES = ['1D', '5D', '1M', '3M', '6M', 'YTD', '1Y', '3Y', '5Y', 'MAX'];
const CHART_TYPES = ['Candlestick', 'Line', 'Area', 'Heikin-Ashi'];

export const ChartWorkspace: React.FC<ChartWorkspaceProps> = ({ ticker }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const engineRef = useRef<ChartEngine | null>(null);
  
  const [interval, setInterval] = useState('1d');
  const [range, setRange] = useState('1M');
  const [chartType, setChartType] = useState('Candlestick');
  
  const { data, loading, error } = useOhlcv(ticker, range, interval);

  useEffect(() => {
    if (containerRef.current && !engineRef.current) {
      engineRef.current = new ChartEngine(containerRef.current);
    }
    
    return () => {
      if (engineRef.current) {
        engineRef.current.destroy();
        engineRef.current = null;
      }
    };
  }, []);

  useEffect(() => {
    if (engineRef.current && data.length > 0) {
      // In a real implementation, HA transform would happen before passing to engine
      engineRef.current.setData(data);
    }
  }, [data, chartType]);

  return (
    <div className="flex flex-col w-full h-full bg-gray-900 border border-gray-800 rounded-lg overflow-hidden shadow-xl">
      {/* Toolbar */}
      <div className="flex items-center gap-4 p-2 bg-gray-800 border-b border-gray-700 text-sm overflow-x-auto">
        <div className="flex items-center gap-1 font-semibold text-white px-2 border-r border-gray-700">
          {ticker}
        </div>
        
        <div className="flex items-center gap-1 border-r border-gray-700 pr-4">
          {INTERVALS.map(int => (
            <button
              key={int}
              onClick={() => setInterval(int)}
              className={`px-2 py-1 rounded transition-colors ${interval === int ? 'bg-blue-600 text-white' : 'text-gray-400 hover:text-white hover:bg-gray-700'}`}
            >
              {int}
            </button>
          ))}
        </div>

        <div className="flex items-center gap-1 border-r border-gray-700 pr-4">
           {RANGES.map(rng => (
            <button
              key={rng}
              onClick={() => setRange(rng)}
              className={`px-2 py-1 rounded transition-colors ${range === rng ? 'bg-blue-600 text-white' : 'text-gray-400 hover:text-white hover:bg-gray-700'}`}
            >
              {rng}
            </button>
          ))}
        </div>
        
        <div className="flex items-center gap-1">
           <select 
              value={chartType} 
              onChange={(e) => setChartType(e.target.value)}
              className="bg-gray-700 text-gray-200 border-none rounded px-2 py-1 outline-none focus:ring-1 focus:ring-blue-500"
           >
              {CHART_TYPES.map(type => (
                <option key={type} value={type}>{type}</option>
              ))}
           </select>
        </div>
      </div>

      {/* Chart Area */}
      <div className="relative flex-1 w-full" ref={containerRef}>
         {loading && (
            <div className="absolute inset-0 flex items-center justify-center bg-gray-900/50 z-10">
               <div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
            </div>
         )}
         {error && (
            <div className="absolute inset-0 flex items-center justify-center bg-gray-900 z-10 flex-col gap-2">
               <span className="text-red-400 font-medium">Error loading data</span>
               <span className="text-gray-400 text-sm max-w-md text-center">{error}</span>
               <button onClick={() => setRange(range)} className="mt-2 px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded">Retry</button>
            </div>
         )}
         {!loading && !error && data.length === 0 && (
            <div className="absolute inset-0 flex items-center justify-center bg-gray-900 z-10">
               <span className="text-gray-500 text-sm">No data available for this range</span>
            </div>
         )}
      </div>
    </div>
  );
};
