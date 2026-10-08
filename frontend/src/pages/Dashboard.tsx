import { Globe, PieChart, BarChart3, FileText, Clock } from 'lucide-react';
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
      <div className="flex items-center justify-between pb-4 border-b border-eq-border">
        <div>
          <h1 className="text-xl font-semibold flex items-center text-eq-text">
            Global Markets Overview
          </h1>
          <p className="text-xs text-eq-text-secondary mt-1">Real-time index tracking and market breadth analysis.</p>
        </div>
        <div className="flex items-center space-x-2">
           <span className="text-eq-green text-sm font-medium flex items-center">
              <span className="h-2 w-2 rounded-full bg-eq-green mr-2"></span>
              Markets Open
           </span>
        </div>
      </div>

      {/* Main Indices Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {MOCK_INDICES.map((idx) => (
          <div 
            key={idx.name} 
            onClick={() => handleNavigateToChart(idx.name)}
            className="bg-eq-surface border border-eq-border rounded p-4 hover:border-eq-border-active transition-all cursor-pointer group"
          >
            <div className="flex justify-between items-start mb-2">
              <h3 className="font-semibold text-[15px] text-eq-text-secondary group-hover:text-eq-text transition-colors">{idx.name}</h3>
              <span className={`text-xs font-medium ${idx.trend === 'up' ? 'text-eq-green' : 'text-eq-red'}`}>
                {idx.percent}
              </span>
            </div>
            <div className="flex flex-col mt-2">
              <div className="text-[22px] font-semibold text-eq-text tracking-tight">{idx.value}</div>
              <div className={`text-sm font-medium flex items-center mt-1 ${idx.trend === 'up' ? 'text-eq-green' : 'text-eq-red'}`}>
                {idx.change}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Analytics Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Global Market Status */}
        <div className="bg-eq-surface border border-eq-border rounded p-4 lg:col-span-1">
          <h3 className="text-xs font-semibold text-eq-text-secondary uppercase tracking-wider mb-4 flex items-center">
            <Globe className="w-4 h-4 mr-2" /> Regional Status
          </h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center py-2 border-b border-eq-border">
              <span className="text-[13px] text-eq-text font-medium">Asia Pacific</span>
              <span className="text-[12px] font-medium text-eq-text-secondary flex items-center"><span className="h-1.5 w-1.5 rounded-full bg-eq-text-disabled mr-1.5"></span>Closed</span>
            </div>
            <div className="flex justify-between items-center py-2 border-b border-eq-border">
              <span className="text-[13px] text-eq-text font-medium">Europe (EMEA)</span>
              <span className="text-[12px] font-medium text-eq-green flex items-center"><span className="h-1.5 w-1.5 rounded-full bg-eq-green mr-1.5"></span>Open</span>
            </div>
            <div className="flex justify-between items-center py-2">
              <span className="text-[13px] text-eq-text font-medium">Americas</span>
              <span className="text-[12px] font-medium text-eq-orange flex items-center"><span className="h-1.5 w-1.5 rounded-full bg-eq-orange mr-1.5"></span>Pre-Market</span>
            </div>
          </div>
        </div>

        {/* Top Movers / AI Analysis */}
        <div className="bg-eq-surface border border-eq-border rounded p-4 lg:col-span-2">
          <h3 className="text-xs font-semibold text-eq-text-secondary uppercase tracking-wider mb-4 flex items-center">
            <BarChart3 className="w-4 h-4 mr-2" /> Top Market Movers
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {MOCK_TOP_MOVERS.map(stock => (
              <div key={stock.symbol} className="bg-eq-surface-elevated border border-eq-border rounded p-3 text-center">
                <div className="font-semibold text-sm mb-1 text-eq-text">{stock.symbol}</div>
                <div className="text-sm text-eq-text-secondary mb-1">₹{stock.price}</div>
                <div className={`text-[13px] font-medium ${stock.change.startsWith('+') ? 'text-eq-green' : 'text-eq-red'}`}>
                  {stock.change}
                </div>
              </div>
            ))}
          </div>

          <div className="mt-4 p-4 bg-eq-purple-muted border border-eq-purple/20 rounded flex items-start">
            <PieChart className="w-5 h-5 text-eq-purple mr-3 flex-shrink-0 mt-0.5" />
            <div>
              <h4 className="text-[14px] font-semibold text-eq-purple mb-1">EquiNexa AI Summary</h4>
              <p className="text-[13px] text-eq-text-secondary leading-relaxed">
                Global equities are demonstrating resilience today. Technology and Banking sectors are leading the indices higher on the back of strong US economic data, offsetting localized geopolitical weakness in energy.
              </p>
            </div>
          </div>
        </div>

        {/* Live News Feed - First Page */}
        <div className="bg-eq-surface border border-eq-border rounded p-4 lg:col-span-3 mt-2">
          <div className="flex items-center justify-between mb-4 border-b border-eq-border pb-3">
            <h3 className="text-xs font-semibold text-eq-text uppercase tracking-wider flex items-center">
              <FileText className="w-4 h-4 mr-2 text-eq-text-muted" /> Live Market News
            </h3>
            <button onClick={() => navigate('/news')} className="text-xs text-eq-purple hover:underline">View All News</button>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {MOCK_LATEST_NEWS.map(news => (
              <div key={news.id} onClick={() => navigate('/news')} className="p-4 bg-eq-bg border border-eq-border rounded hover:border-eq-purple/50 cursor-pointer transition-colors group">
                <div className="flex items-center text-[11px] text-eq-text-muted mb-2">
                  <span className="font-semibold text-eq-text-secondary mr-2">{news.source}</span>
                  <Clock className="w-3 h-3 mr-1" /> {news.time}
                </div>
                <h4 className="text-[13px] font-semibold text-eq-text group-hover:text-eq-purple transition-colors leading-relaxed">
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

export default Dashboard;
