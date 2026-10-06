import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { fetchIndices, type MarketIndex, fetchHistory, type OHLCV } from '../services/api/markets';
import { AlertCircle } from 'lucide-react';

const Overview = () => {
  const navigate = useNavigate();
  const [indices, setIndices] = useState<MarketIndex[]>([]);
  const [chartData, setChartData] = useState<OHLCV[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    const loadData = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await fetchIndices();
        if (!active) return;
        setIndices(data);

        // Fetch history for the first index for the chart
        if (data.length > 0) {
          try {
            const hist = await fetchHistory(data[0].symbol, '1M', '1d');
            if (active) setChartData(hist);
          } catch (chartErr: any) {
            console.warn('Index chart history unavailable:', chartErr);
          }
        }
      } catch (err: any) {
        if (active) setError(err.message || 'Failed to load market data');
      } finally {
        if (active) setLoading(false);
      }
    };

    loadData();
    return () => { active = false; };
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-text-primary">Market Overview</h1>
        <span className="text-sm text-text-muted">Data subject to provider delays</span>
      </div>

      {error && (
        <div className="bg-red-950/30 border border-market-down/50 rounded-lg p-4 flex items-start text-market-down">
          <AlertCircle className="w-5 h-5 mr-3 mt-0.5 flex-shrink-0" />
          <p className="text-sm">{error}</p>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4">
        {loading ? (
          ['NIFTY 50', 'SENSEX', 'S&P 500', 'NASDAQ', 'Dow Jones'].map(idx => (
            <div key={idx} className="bg-card-bg p-4 rounded-xl border border-border-subtle animate-pulse h-28" />
          ))
        ) : (
          [
            { symbol: '^NSEI', name: 'NIFTY 50' },
            { symbol: '^BSESN', name: 'SENSEX' },
            { symbol: '^GSPC', name: 'S&P 500' },
            { symbol: '^IXIC', name: 'NASDAQ' },
            { symbol: '^DJI', name: 'Dow Jones' }
          ].map(expected => {
            const idx = indices.find(i => i.symbol === expected.symbol);
            if (!idx) {
              return (
                <div key={expected.symbol} className="w-full bg-card-bg p-4 rounded-xl border border-border-subtle shadow-sm opacity-60">
                  <div className="flex justify-between items-start">
                    <h3 className="text-text-secondary text-xs font-medium truncate" title={expected.name}>{expected.name}</h3>
                  </div>
                  <div className="mt-2 text-text-muted text-sm italic">
                    Data unavailable
                  </div>
                </div>
              );
            }
            return (
            <button 
              key={idx.symbol} 
              onClick={() => navigate(`/analysis?ticker=${encodeURIComponent(idx.symbol)}`)}
              className="text-left w-full bg-card-bg p-4 rounded-xl border border-border-subtle shadow-sm hover:bg-hover-bg transition-colors"
            >
              <div className="flex justify-between items-start">
                <h3 className="text-text-secondary text-xs font-medium truncate" title={idx.name}>{idx.name}</h3>
                <span className="text-[10px] text-text-muted bg-border-subtle px-1.5 py-0.5 rounded uppercase">{idx.currency}</span>
              </div>
              <div className="mt-2">
                <span className="text-xl font-bold text-text-primary">{idx.price.toLocaleString(undefined, { minimumFractionDigits: 2 })}</span>
              </div>
              <div className={`text-sm mt-1 flex items-center ${idx.change >= 0 ? 'text-market-up' : 'text-market-down'}`}>
                <span>{idx.change >= 0 ? '+' : ''}{idx.change.toFixed(2)} ({idx.change_percent.toFixed(2)}%)</span>
              </div>
              <p className="text-[10px] text-text-muted mt-1 uppercase tracking-wider">{idx.status}</p>
            </button>
            );
          })
        )}
      </div>

      <div className="bg-card-bg p-6 rounded-xl border border-border-subtle shadow-sm h-96">
        <h3 className="text-lg font-semibold mb-4 text-text-primary">
          Market Trend {indices.length > 0 ? `(${indices[0].name})` : ''}
        </h3>
        
        {loading ? (
          <div className="w-full h-full flex items-center justify-center">
            <div className="w-6 h-6 border-2 border-text-primary border-t-transparent rounded-full animate-spin"></div>
          </div>
        ) : chartData.length > 0 ? (
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#242424" />
              <XAxis 
                dataKey="time" 
                axisLine={false} 
                tickLine={false} 
                stroke="#737373" 
                tickFormatter={(val) => new Date(val).toLocaleDateString(undefined, {month: 'short', day: 'numeric'})}
              />
              <YAxis 
                domain={['auto', 'auto']} 
                axisLine={false} 
                tickLine={false} 
                stroke="#737373" 
                tickFormatter={(val) => val.toLocaleString()}
              />
              <Tooltip 
                contentStyle={{ backgroundColor: '#0b0b0b', borderColor: '#242424', color: '#f5f5f5' }} 
                labelFormatter={(val) => new Date(val as string).toLocaleDateString()}
              />
              <Line type="monotone" dataKey="close" stroke="#f5f5f5" strokeWidth={2} dot={false} activeDot={{ r: 4 }} />
            </LineChart>
          </ResponsiveContainer>
        ) : (
           <div className="w-full h-full flex items-center justify-center text-text-muted">No chart data available</div>
        )}
      </div>
    </div>
  );
};

export default Overview;
