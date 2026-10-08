import { Activity, TrendingUp, TrendingDown, Globe, PieChart, BarChart3, LineChart, FileText, Clock } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const MOCK_INDICES = [
  { name: 'NIFTY 50', value: '22,450.50', change: '+125.20', percent: '+0.56%', trend: 'up' },
  { name: 'SENSEX', value: '73,900.10', change: '+410.80', percent: '+0.56%', trend: 'up' },
  { name: 'NIFTY BANK', value: '47,500.25', change: '-80.10', percent: '-0.17%', trend: 'down' },
  { name: 'S&P 500', value: '5,120.40', change: '+45.30', percent: '+0.89%', trend: 'up' },
  { name: 'NASDAQ', value: '16,250.80', change: '+210.50', percent: '+1.31%', trend: 'up' },
  { name: 'INDIA VIX', value: '14.20', change: '-0.40', percent: '-2.74%', trend: 'down' }
];

const MOCK_TOP_MOVERS = [
  { symbol: 'RELIANCE', change: '+2.4%', price: '2,540' },
  { symbol: 'TCS', change: '+1.8%', price: '3,950' },
  { symbol: 'HDFCBANK', change: '-1.2%', price: '1,420' },
  { symbol: 'INFY', change: '+0.9%', price: '1,580' },
];

const MOCK_LATEST_NEWS = [
  { id: 1, headline: "RBI Maintains Repo Rate at 6.5%, Shifts Stance to Neutral", time: "10 mins ago", source: "Central Bank Wire" },
  { id: 2, headline: "TCS Q2 Results: Net Profit Rises 8% to ₹11,342 Crore", time: "1 hr ago", source: "Financial Express" },
  { id: 3, headline: "Oil Prices Surge 4% Amid Geopolitical Tensions in Middle East", time: "2 hrs ago", source: "Global Energy News" },
];

const Dashboard = () => {
  const navigate = useNavigate();

  const handleNavigateToChart = (symbol: string) => {
    navigate(`/analysis?ticker=${encodeURIComponent(symbol)}`);
  };
  return (
    <div className="flex flex-col h-full bg-black-bg text-text-primary p-4 lg:p-6 max-w-screen-2xl mx-auto w-full space-y-6 overflow-y-auto">
      
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold flex items-center">
            <LayoutDashboard className="w-6 h-6 mr-2 text-blue-500" />
            Global Markets Overview
          </h1>
          <p className="text-sm text-text-muted mt-1">Real-time index tracking and market breadth analysis.</p>
        </div>
        <div className="flex items-center space-x-2">
           <span className="px-3 py-1 bg-green-900/30 text-market-up border border-green-900/50 text-sm rounded font-medium flex items-center">
              <span className="relative flex h-2 w-2 mr-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-market-up opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-market-up"></span>
              </span>
              MARKETS OPEN
           </span>
        </div>
      </div>

      {/* Main Indices Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {MOCK_INDICES.map((idx) => (
          <div 
            key={idx.name} 
            onClick={() => handleNavigateToChart(idx.name)}
            className="bg-card-bg border border-border-subtle rounded-lg p-5 hover:border-blue-500/50 hover:bg-hover-bg transition-all cursor-pointer group"
          >
            <div className="flex justify-between items-start mb-4">
              <h3 className="font-bold text-lg group-hover:text-blue-400 transition-colors">{idx.name}</h3>
              <Activity className={`w-5 h-5 ${idx.trend === 'up' ? 'text-market-up' : 'text-market-down'}`} />
            </div>
            <div className="flex justify-between items-end">
              <div>
                <div className="text-3xl font-mono font-bold">{idx.value}</div>
                <div className={`font-mono text-sm font-medium flex items-center mt-1 ${idx.trend === 'up' ? 'text-market-up' : 'text-market-down'}`}>
                  {idx.trend === 'up' ? <TrendingUp className="w-4 h-4 mr-1" /> : <TrendingDown className="w-4 h-4 mr-1" />}
                  {idx.change} ({idx.percent})
                </div>
              </div>
              <div className="w-20 h-10 bg-black-bg rounded border border-border-subtle flex items-center justify-center opacity-50">
                <LineChart className="w-5 h-5 text-text-muted" />
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Analytics Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Global Market Status */}
        <div className="bg-card-bg border border-border-subtle rounded-lg p-5 lg:col-span-1">
          <h3 className="text-sm font-semibold text-text-secondary uppercase tracking-wider mb-4 flex items-center">
            <Globe className="w-4 h-4 mr-2" /> Regional Status
          </h3>
          <div className="space-y-4 text-sm font-medium">
            <div className="flex justify-between items-center p-3 bg-black-bg border border-border-subtle rounded-lg">
              <span>Asia Pacific</span>
              <span className="text-market-up">Closed</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-black-bg border border-border-subtle rounded-lg">
              <span>Europe (EMEA)</span>
              <span className="text-market-up">Open</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-black-bg border border-border-subtle rounded-lg">
              <span>Americas</span>
              <span className="text-text-muted">Pre-Market</span>
            </div>
          </div>
        </div>

        {/* Top Movers / AI Analysis */}
        <div className="bg-card-bg border border-border-subtle rounded-lg p-5 lg:col-span-2">
          <h3 className="text-sm font-semibold text-text-secondary uppercase tracking-wider mb-4 flex items-center">
            <BarChart3 className="w-4 h-4 mr-2" /> Top Market Movers
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {MOCK_TOP_MOVERS.map(stock => (
              <div key={stock.symbol} className="bg-black-bg border border-border-subtle rounded-lg p-3 text-center">
                <div className="font-bold mb-1">{stock.symbol}</div>
                <div className="font-mono text-sm text-text-muted mb-1">₹{stock.price}</div>
                <div className={`font-mono text-xs font-bold ${stock.change.startsWith('+') ? 'text-market-up' : 'text-market-down'}`}>
                  {stock.change}
                </div>
              </div>
            ))}
          </div>

          <div className="mt-6 p-4 bg-blue-900/10 border border-blue-500/20 rounded-lg flex items-start">
            <PieChart className="w-5 h-5 text-blue-500 mr-3 flex-shrink-0 mt-0.5" />
            <div>
              <h4 className="text-sm font-bold text-blue-400 mb-1">EquiNexa AI Summary</h4>
              <p className="text-sm text-text-secondary leading-relaxed">
                Global equities are demonstrating resilience today. Technology and Banking sectors are leading the indices higher on the back of strong US economic data, offsetting localized geopolitical weakness in energy.
              </p>
            </div>
          </div>
        </div>

        {/* Live News Feed - First Page */}
        <div className="bg-card-bg border border-border-subtle rounded-lg p-5 lg:col-span-3 mt-2">
          <div className="flex items-center justify-between mb-4 border-b border-border-subtle pb-3">
            <h3 className="text-sm font-semibold text-text-primary uppercase tracking-wider flex items-center">
              <FileText className="w-4 h-4 mr-2 text-text-muted" /> Live Market News
            </h3>
            <button onClick={() => navigate('/news')} className="text-xs text-blue-500 hover:underline">View All News</button>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {MOCK_LATEST_NEWS.map(news => (
              <div key={news.id} onClick={() => navigate('/news')} className="p-4 bg-black-bg border border-border-subtle rounded-lg hover:border-blue-500/30 cursor-pointer transition-colors group">
                <div className="flex items-center text-xs text-text-muted mb-2">
                  <span className="font-semibold text-text-secondary mr-2">{news.source}</span>
                  <Clock className="w-3 h-3 mr-1" /> {news.time}
                </div>
                <h4 className="text-sm font-bold text-text-primary group-hover:text-blue-400 transition-colors leading-relaxed">
                  {news.headline}
                </h4>
              </div>
            ))}
          </div>
        </div>
        
      </div>
    </div>
  );
};

// Lucide icon not imported in top level to avoid clutter, importing locally for Dashboard
import { LayoutDashboard } from 'lucide-react';

export default Dashboard;
