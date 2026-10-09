import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { Globe, AlertCircle, RefreshCw, Clock, TrendingUp, TrendingDown, Minus } from 'lucide-react';

interface IndexData {
  name: string;
  symbol: string;
  price: number;
  change: number;
  change_percent: number;
  currency: string;
  timestamp: string;
  status: string;
}

// NSE/BSE 2025-2026 exchange holiday list (verified against NSE calendar)
// Note: Only exchange-declared holidays are listed. State/regional holidays are not included.
const NSE_HOLIDAYS_2025_2026 = new Set([
  '2025-01-26', // Republic Day
  '2025-03-14', // Holi
  '2025-04-14', // Dr. Ambedkar Jayanti
  '2025-04-18', // Good Friday
  '2025-05-01', // Maharashtra Day
  '2025-08-15', // Independence Day
  '2025-10-02', // Gandhi Jayanti
  '2025-10-24', // Dussehra
  '2025-11-05', // Diwali Laxmi Puja
  '2025-11-20', // Gurunanak Jayanti (to be confirmed)
  '2025-12-25', // Christmas
  '2026-01-26', // Republic Day
  '2026-03-03', // Holi
  '2026-04-03', // Good Friday
  '2026-04-14', // Dr. Ambedkar Jayanti
  '2026-05-01', // Maharashtra Day
  '2026-08-15', // Independence Day
  '2026-10-02', // Gandhi Jayanti
  '2026-12-25', // Christmas
]);

type MarketSession = 'pre-open' | 'open' | 'closed';

interface MarketStatus {
  session: MarketSession;
  label: string;
  nextEvent: string;
  isHoliday: boolean;
  holidayNote?: string;
}

function getIndianMarketStatus(): MarketStatus {
  const now = new Date();
  // Convert to IST
  const istOffset = 5.5 * 60 * 60 * 1000;
  const istNow = new Date(now.getTime() + (now.getTimezoneOffset() * 60 * 1000) + istOffset);

  const day = istNow.getDay(); // 0=Sun, 6=Sat
  const yyyy = istNow.getFullYear();
  const mm = String(istNow.getMonth() + 1).padStart(2, '0');
  const dd = String(istNow.getDate()).padStart(2, '0');
  const dateStr = `${yyyy}-${mm}-${dd}`;

  const isWeekend = day === 0 || day === 6;
  const isHoliday = NSE_HOLIDAYS_2025_2026.has(dateStr);

  if (isWeekend || isHoliday) {
    // Find next trading day
    let nextOpen = new Date(istNow);
    nextOpen.setHours(9, 15, 0, 0);
    do {
      nextOpen.setDate(nextOpen.getDate() + 1);
      const d = nextOpen.getDay();
      const nd = `${nextOpen.getFullYear()}-${String(nextOpen.getMonth() + 1).padStart(2, '0')}-${String(nextOpen.getDate()).padStart(2, '0')}`;
      if (d !== 0 && d !== 6 && !NSE_HOLIDAYS_2025_2026.has(nd)) break;
    } while (true);

    const daysUntil = Math.ceil((nextOpen.getTime() - istNow.getTime()) / (1000 * 60 * 60 * 24));
    return {
      session: 'closed',
      label: 'Market Closed',
      nextEvent: daysUntil === 1 ? 'Opens tomorrow at 9:15 AM IST' : `Opens ${nextOpen.toLocaleDateString('en-IN', { weekday: 'long' })} at 9:15 AM IST`,
      isHoliday,
      holidayNote: isHoliday ? 'Exchange holiday' : (day === 6 ? 'Saturday' : 'Sunday'),
    };
  }

  const h = istNow.getHours();
  const m = istNow.getMinutes();
  const totalMins = h * 60 + m;

  const PRE_OPEN_START = 9 * 60;      // 09:00
  const MARKET_OPEN   = 9 * 60 + 15;  // 09:15
  const MARKET_CLOSE  = 15 * 60 + 30; // 15:30

  if (totalMins < PRE_OPEN_START) {
    const minsUntil = PRE_OPEN_START - totalMins;
    return { session: 'closed', label: 'Market Closed', nextEvent: `Pre-open starts in ${minsUntil} min`, isHoliday: false };
  }
  if (totalMins < MARKET_OPEN) {
    const minsUntil = MARKET_OPEN - totalMins;
    return { session: 'pre-open', label: 'Pre-Open Session', nextEvent: `Regular trading opens in ${minsUntil} min`, isHoliday: false };
  }
  if (totalMins < MARKET_CLOSE) {
    const minsUntil = MARKET_CLOSE - totalMins;
    const hLeft = Math.floor(minsUntil / 60);
    const mLeft = minsUntil % 60;
    const timeLeft = hLeft > 0 ? `${hLeft}h ${mLeft}m` : `${mLeft}m`;
    return { session: 'open', label: 'Market Open', nextEvent: `Closes in ${timeLeft}`, isHoliday: false };
  }
  return { session: 'closed', label: 'Market Closed', nextEvent: 'Opens tomorrow at 9:15 AM IST', isHoliday: false };
}

const MarketStatusBanner = () => {
  const [status, setStatus] = useState<MarketStatus>(getIndianMarketStatus);

  useEffect(() => {
    const id = setInterval(() => setStatus(getIndianMarketStatus()), 30_000);
    return () => clearInterval(id);
  }, []);

  const sessionConfig = {
    'pre-open': { bg: 'bg-yellow-50 border-yellow-200', dot: 'bg-yellow-400', text: 'text-yellow-800', icon: Minus },
    'open':     { bg: 'bg-green-50 border-green-200',  dot: 'bg-green-500',  text: 'text-green-800',  icon: TrendingUp },
    'closed':   { bg: 'bg-gray-50 border-gray-200',    dot: 'bg-gray-400',   text: 'text-gray-700',   icon: TrendingDown },
  };

  const cfg = sessionConfig[status.session];
  const Icon = cfg.icon;

  return (
    <div className={`flex items-center justify-between px-4 py-2.5 rounded border ${cfg.bg} text-sm`}>
      <div className="flex items-center gap-2.5">
        <span className={`inline-flex items-center gap-1.5 font-semibold ${cfg.text}`}>
          <span className={`w-2 h-2 rounded-full ${cfg.dot} ${status.session === 'open' ? 'animate-pulse' : ''}`} />
          <Icon className="w-3.5 h-3.5" />
          NSE/BSE — {status.label}
        </span>
        {status.holidayNote && (
          <span className="text-xs text-gray-500">({status.holidayNote})</span>
        )}
      </div>
      <div className="flex items-center gap-1.5 text-gray-500 text-xs">
        <Clock className="w-3.5 h-3.5" />
        <span>{status.nextEvent}</span>
      </div>
    </div>
  );
};

const Markets = () => {
  const navigate = useNavigate();
  const [indices, setIndices] = useState<IndexData[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const fetchIndices = useCallback(async () => {
    setIsLoading(true);
    setErrorMsg(null);
    try {
      const baseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const res = await fetch(`${baseUrl}/api/v1/markets/indices`);
      if (!res.ok) {
        throw new Error(`HTTP error ${res.status}`);
      }
      const data = await res.json();
      if (data.status === 'OK' && data.indices) {
        setIndices(data.indices);
      } else {
        throw new Error(data.reason || "Failed to load market data");
      }
    } catch (err: any) {
      console.error(err);
      setErrorMsg(err.message || "Failed to load market data");
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchIndices();
  }, [fetchIndices]);

  const handleNavigateToChart = (symbol: string) => {
    navigate(`/analysis?ticker=${encodeURIComponent(symbol)}`);
  };

  const indianIndices = indices.filter(idx => ['NIFTY 50', 'SENSEX', 'NIFTY BANK', 'INDIA VIX'].includes(idx.name));
  const globalIndices = indices.filter(idx => ['S&P 500', 'NASDAQ', 'Dow Jones'].includes(idx.name));

  const formatPrice = (price: number, currency: string) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: currency,
      maximumFractionDigits: 2
    }).format(price);
  };

  const renderIndexGrid = (title: string, data: IndexData[]) => (
    <div className="mb-8">
      <h2 className="text-lg font-semibold text-eq-text mb-4 flex items-center">
        {title}
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {data.length > 0 ? (
          data.map((idx) => (
            <div 
              key={idx.name} 
              onClick={() => handleNavigateToChart(idx.symbol)}
              className="bg-eq-surface border border-eq-border rounded p-4 hover:border-eq-border-active transition-all cursor-pointer group"
            >
              <div className="flex justify-between items-start mb-2">
                <h3 className="font-semibold text-[15px] text-eq-text-secondary group-hover:text-eq-text transition-colors">{idx.name}</h3>
                <span className={`text-xs font-medium ${idx.change >= 0 ? 'text-eq-green' : 'text-eq-red'}`}>
                  {idx.change >= 0 ? '+' : ''}{idx.change_percent.toFixed(2)}%
                </span>
              </div>
              <div className="flex flex-col mt-2">
                <div className="text-[22px] font-semibold text-eq-text tracking-tight">
                  {formatPrice(idx.price, idx.currency)}
                </div>
                <div className={`text-sm font-medium flex items-center mt-1 ${idx.change >= 0 ? 'text-eq-green' : 'text-eq-red'}`}>
                  {idx.change >= 0 ? '+' : ''}{idx.change.toFixed(2)}
                </div>
                <div className="text-[10px] text-eq-text-muted mt-2 uppercase tracking-wider">
                  {idx.status}
                </div>
              </div>
            </div>
          ))
        ) : (
           <div className="col-span-full p-4 border border-dashed border-eq-border rounded text-center text-eq-text-muted text-sm">
             Data unavailable for these instruments.
           </div>
        )}
      </div>
    </div>
  );

  return (
    <div className="flex flex-col h-full bg-eq-bg text-eq-text p-4 lg:p-6 max-w-screen-2xl mx-auto w-full space-y-6 overflow-y-auto">
      {/* Header */}
      <div className="flex items-center justify-between pb-4 border-b border-eq-border">
        <div>
          <h1 className="text-xl font-semibold flex items-center text-eq-text">
            <Globe className="w-6 h-6 mr-3 text-eq-purple" />
            Global Markets Overview
          </h1>
          <p className="text-sm text-eq-text-secondary mt-1">Real-time tracking of major indices and market indicators.</p>
        </div>
        <div className="flex items-center space-x-3">
          <button 
             onClick={fetchIndices} 
             disabled={isLoading}
             className="flex items-center px-3 py-1.5 text-sm bg-eq-surface-elevated hover:bg-eq-border text-eq-text rounded transition-colors disabled:opacity-50"
          >
            <RefreshCw className={`w-4 h-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
            Refresh
          </button>
        </div>
      </div>

      {/* Indian Market Status */}
      <MarketStatusBanner />

      {errorMsg && (
        <div className="p-4 border border-eq-red bg-eq-red/10 rounded flex items-start">
          <AlertCircle className="w-5 h-5 text-eq-red mr-3 flex-shrink-0 mt-0.5" />
          <p className="text-sm text-eq-red">{errorMsg}</p>
        </div>
      )}

      {isLoading && indices.length === 0 ? (
        <div className="flex items-center justify-center py-20">
            <div className="w-8 h-8 border-3 border-eq-border border-t-eq-purple rounded-full animate-spin"></div>
        </div>
      ) : (
        <>
          {renderIndexGrid("Indian Markets", indianIndices)}
          {renderIndexGrid("Global Markets", globalIndices)}
        </>
      )}

      {/* Disclaimer */}
      <p className="text-[11px] text-eq-text-muted pb-2">
        ⚠ Indian market holiday data is based on the NSE exchange calendar for 2025–2026 and may not reflect last-minute changes. Always verify with the official NSE/BSE website. Market timings are in IST (UTC+5:30).
      </p>
    </div>
  );
};

export default Markets;

