import { Globe2, BarChart2, TrendingUp, TrendingDown, Percent, Activity } from 'lucide-react';

const MOCK_MACRO = [
  { id: 'US10Y', name: 'US 10-Year Treasury Yield', value: '4.25%', change: '+0.03', trend: 'up' },
  { id: 'IN10Y', name: 'India 10-Year Bond Yield', value: '7.12%', change: '-0.02', trend: 'down' },
  { id: 'USINF', name: 'US Core Inflation (YoY)', value: '3.1%', change: '0.0', trend: 'neutral' },
  { id: 'ININF', name: 'India CPI Inflation (YoY)', value: '5.09%', change: '-0.01', trend: 'down' },
  { id: 'BRENT', name: 'Brent Crude Oil', value: '$82.50', change: '+1.20', trend: 'up' },
  { id: 'GOLD', name: 'Gold Futures', value: '$2,150', change: '+15.00', trend: 'up' },
];

const Macro = () => {
  return (
    <div className="flex flex-col h-full bg-black-bg text-text-primary p-4 lg:p-6 max-w-screen-xl mx-auto w-full space-y-6">
      
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between md:items-center gap-4">
        <div>
          <h1 className="text-2xl font-bold flex items-center">
            <Globe2 className="w-6 h-6 mr-2 text-blue-500" /> Macroeconomics & Yields
          </h1>
          <p className="text-sm text-text-muted mt-1">FRED data integrations tracking global bonds, inflation, and commodities.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        
        {MOCK_MACRO.map(item => (
          <div key={item.id} className="bg-card-bg border border-border-subtle rounded-lg p-5 hover:border-text-muted transition-colors cursor-pointer group">
            <div className="flex justify-between items-start mb-4">
              <h3 className="font-semibold text-text-secondary group-hover:text-blue-400 transition-colors">{item.name}</h3>
              {item.id.includes('INF') ? <Percent className="w-5 h-5 text-text-muted" /> : 
               item.id.includes('10Y') ? <Activity className="w-5 h-5 text-text-muted" /> :
               <BarChart2 className="w-5 h-5 text-text-muted" />}
            </div>
            
            <div className="flex items-end space-x-3">
              <span className="text-3xl font-mono font-bold text-text-primary">{item.value}</span>
              <span className={`font-mono text-sm font-medium mb-1 flex items-center ${
                item.trend === 'up' ? 'text-market-up' : item.trend === 'down' ? 'text-market-down' : 'text-text-muted'
              }`}>
                {item.trend === 'up' && <TrendingUp className="w-4 h-4 mr-1" />}
                {item.trend === 'down' && <TrendingDown className="w-4 h-4 mr-1" />}
                {item.change}
              </span>
            </div>
            
            <div className="mt-4 pt-4 border-t border-border-subtle text-xs text-text-muted flex justify-between">
              <span>Source: Federal Reserve (FRED)</span>
              <span>Updated: Today</span>
            </div>
          </div>
        ))}

      </div>

      {/* Yield Curve Chart Placeholder */}
      <div className="bg-card-bg border border-border-subtle rounded-lg p-6 mt-4">
        <h3 className="text-lg font-bold mb-4 flex items-center">
          <Activity className="w-5 h-5 mr-2 text-blue-400" /> US vs India Yield Curve Comparison
        </h3>
        <div className="h-64 bg-black-bg border border-border-subtle rounded-lg flex items-center justify-center">
          <p className="text-text-muted font-medium flex items-center">
            <BarChart2 className="w-5 h-5 mr-2" /> V2 Chart Data Rendering...
          </p>
        </div>
      </div>

    </div>
  );
};

export default Macro;
