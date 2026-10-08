import { Bell, Plus, Settings, AlertTriangle, TrendingUp, Clock, Search } from 'lucide-react';

const MOCK_ALERTS = [
  { id: 1, type: 'price', symbol: 'RELIANCE', condition: 'Crosses Above', value: '2,600.00', status: 'active', created: '2 hrs ago' },
  { id: 2, type: 'price', symbol: 'NIFTY 50', condition: 'Drops Below', value: '22,000.00', status: 'active', created: '1 day ago' },
  { id: 3, type: 'news', symbol: 'TCS', condition: 'Earnings Release', value: 'Any Sentiment', status: 'triggered', created: '3 days ago' },
  { id: 4, type: 'ai', symbol: 'HDFCBANK', condition: 'AI Bias Shifts', value: 'To Bullish', status: 'active', created: '5 hrs ago' }
];

const Alerts = () => {
  return (
    <div className="flex flex-col h-full bg-black-bg text-text-primary p-4 lg:p-6 max-w-screen-xl mx-auto w-full space-y-6">
      
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between md:items-center gap-4">
        <div>
          <h1 className="text-2xl font-bold flex items-center">
            <Bell className="w-6 h-6 mr-2 text-blue-500" /> Trading Alerts Engine
          </h1>
          <p className="text-sm text-text-muted mt-1">Configure price thresholds, news triggers, and AI logic alerts.</p>
        </div>
        
        <button className="flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-md text-sm font-semibold transition-colors">
          <Plus className="w-4 h-4 mr-2" /> Create Alert
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 flex-1 min-h-0">
        
        {/* Left Column: Stats & Settings */}
        <div className="lg:col-span-1 space-y-6">
          <div className="bg-card-bg border border-border-subtle rounded-lg p-5">
            <h3 className="text-sm font-semibold text-text-secondary uppercase tracking-wider mb-4">Alert Usage</h3>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span>Active Alerts</span>
                  <span className="font-mono">3 / 50</span>
                </div>
                <div className="w-full bg-border-subtle rounded-full h-1.5">
                  <div className="bg-blue-500 h-1.5 rounded-full" style={{ width: '6%' }}></div>
                </div>
              </div>
              <div className="pt-4 border-t border-border-subtle">
                <div className="flex items-center text-sm text-text-muted hover:text-text-primary cursor-pointer transition-colors">
                  <Settings className="w-4 h-4 mr-2" /> Notification Preferences
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: Alert List */}
        <div className="lg:col-span-3 bg-card-bg border border-border-subtle rounded-lg flex flex-col">
          <div className="p-4 border-b border-border-subtle flex justify-between items-center bg-hover-bg rounded-t-lg">
            <h2 className="text-sm font-semibold text-text-primary">Managed Alerts</h2>
            <div className="relative">
              <Search className="w-4 h-4 text-text-muted absolute left-2.5 top-2" />
              <input type="text" placeholder="Search alerts..." className="pl-9 pr-3 py-1.5 bg-black-bg border border-border-subtle rounded text-sm focus:outline-none focus:border-text-muted transition-colors" />
            </div>
          </div>
          
          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {MOCK_ALERTS.map(alert => (
              <div key={alert.id} className={`p-4 border rounded-lg flex flex-col md:flex-row md:items-center justify-between transition-colors ${
                alert.status === 'triggered' 
                  ? 'bg-red-950/20 border-red-900/50' 
                  : 'bg-black-bg border-border-subtle hover:border-text-muted'
              }`}>
                <div className="flex items-center mb-3 md:mb-0">
                  <div className={`w-10 h-10 rounded-full flex items-center justify-center mr-4 ${
                    alert.type === 'price' ? 'bg-blue-900/30 text-blue-500' :
                    alert.type === 'news' ? 'bg-purple-900/30 text-purple-500' :
                    'bg-green-900/30 text-market-up'
                  }`}>
                    {alert.type === 'price' ? <TrendingUp className="w-5 h-5" /> :
                     alert.type === 'news' ? <Bell className="w-5 h-5" /> :
                     <AlertTriangle className="w-5 h-5" />}
                  </div>
                  <div>
                    <div className="font-bold text-text-primary text-lg">{alert.symbol}</div>
                    <div className="text-sm text-text-muted flex items-center mt-0.5">
                      <span className="font-medium text-text-secondary mr-2">{alert.condition}</span> 
                      <span className="font-mono text-xs px-2 py-0.5 bg-card-bg border border-border-subtle rounded">{alert.value}</span>
                    </div>
                  </div>
                </div>
                
                <div className="flex items-center justify-between md:justify-end md:space-x-6">
                  <div className="flex items-center text-xs text-text-muted">
                    <Clock className="w-3 h-3 mr-1" /> {alert.created}
                  </div>
                  <div className={`px-3 py-1 text-xs font-bold rounded-full uppercase tracking-wider border ${
                    alert.status === 'triggered' 
                      ? 'bg-red-900/30 text-red-400 border-red-900/50' 
                      : 'bg-green-900/20 text-market-up border-green-900/50'
                  }`}>
                    {alert.status}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
        
      </div>
    </div>
  );
};

export default Alerts;
