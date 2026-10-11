import React, { useEffect, useRef, useState } from 'react';
import { ChartEngine } from './ChartEngine';
import { useOhlcv } from './useOhlcv';
import { useTheme } from '../../context/ThemeContext';

interface ChartWorkspaceProps {
  ticker: string;
}

const INTERVALS = ['1m', '5m', '15m', '30m', '1h', '1d', '1wk', '1mo'];
const RANGES = ['1D', '5D', '1M', '3M', '6M', 'YTD', '1Y', '3Y', '5Y', 'MAX'];
const CHART_TYPES = ['Candlestick', 'Line', 'Area', 'Heikin-Ashi'];

export const ChartWorkspace: React.FC<ChartWorkspaceProps> = ({ ticker }) => {
  const { theme } = useTheme();
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
    if (engineRef.current) {
      engineRef.current.applyTheme(theme === 'dark');
    }
  }, [theme]);

  useEffect(() => {
    if (engineRef.current && data.length > 0) {
      engineRef.current.setData(data);
    }
  }, [data, chartType]);

  return (
    <div className="flex flex-col w-full h-full bg-eq-bg border border-eq-border rounded-lg overflow-hidden shadow-xl text-eq-text">
      {/* Toolbar */}
      <div className="flex items-center gap-4 p-2 bg-eq-surface-card border-b border-eq-border text-sm overflow-x-auto">
        <div className="flex items-center gap-1 font-semibold text-eq-text px-2 border-r border-eq-border">
          {ticker}
        </div>
        
        <div className="flex items-center gap-1 border-r border-eq-border pr-4">
          {INTERVALS.map(int => (
            <button
              key={int}
              onClick={() => setInterval(int)}
              className={`px-2 py-1 rounded transition-colors ${interval === int ? 'bg-eq-purple text-white' : 'text-eq-text-muted hover:text-eq-text hover:bg-eq-surface-elevated'}`}
            >
              {int}
            </button>
          ))}
        </div>

        <div className="flex items-center gap-1 border-r border-eq-border pr-4">
           {RANGES.map(rng => (
            <button
              key={rng}
              onClick={() => setRange(rng)}
              className={`px-2 py-1 rounded transition-colors ${range === rng ? 'bg-eq-purple text-white' : 'text-eq-text-muted hover:text-eq-text hover:bg-eq-surface-elevated'}`}
            >
              {rng}
            </button>
          ))}
        </div>
        
        <div className="flex items-center gap-1">
           <select 
              value={chartType} 
              onChange={(e) => setChartType(e.target.value)}
              className="bg-eq-surface-elevated text-eq-text border border-eq-border rounded px-2 py-1 outline-none focus:ring-1 focus:ring-eq-purple"
           >
              {CHART_TYPES.map(type => (
                <option key={type} value={type}>{type}</option>
              ))}
           </select>
        </div>
      </div>

      {/* Chart Area */}
      <div className="relative flex-1 w-full bg-eq-bg" ref={containerRef}>
         {loading && (
            <div className="absolute inset-0 flex items-center justify-center bg-eq-bg/50 z-10">
               <div className="w-8 h-8 border-4 border-eq-purple border-t-transparent rounded-full animate-spin"></div>
            </div>
         )}
         {error && (
            <div className="absolute inset-0 flex items-center justify-center bg-eq-bg z-10 flex-col gap-2">
               <span className="text-eq-red font-medium">Error loading data</span>
               <span className="text-eq-text-muted text-sm max-w-md text-center">{error}</span>
               <button onClick={() => setRange(range)} className="mt-2 px-4 py-2 bg-eq-surface-elevated hover:bg-eq-border text-eq-text rounded">Retry</button>
            </div>
         )}
         {!loading && !error && data.length === 0 && (
            <div className="absolute inset-0 flex items-center justify-center bg-eq-bg z-10">
               <span className="text-eq-text-muted text-sm">No data available for this range</span>
            </div>
         )}
      </div>
    </div>
  );
};
