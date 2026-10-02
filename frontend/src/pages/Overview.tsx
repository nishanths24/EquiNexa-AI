
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const data = [
  { time: '09:30', price: 150 },
  { time: '10:30', price: 152 },
  { time: '11:30', price: 149 },
  { time: '12:30', price: 153 },
  { time: '13:30', price: 155 },
  { time: '14:30', price: 154 },
  { time: '15:30', price: 158 },
];

const Overview = () => {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">Market Overview</h1>
        <span className="text-sm text-neutral-500">Data delayed by 15 minutes</span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Mock Indices */}
        {['S&P 500', 'NASDAQ', 'NIFTY 50'].map(idx => (
          <div key={idx} className="bg-white p-6 rounded-xl border border-neutral-200 shadow-sm">
            <h3 className="text-neutral-500 text-sm font-medium">{idx}</h3>
            <div className="mt-2 flex items-baseline">
              <span className="text-3xl font-bold">Unavailable</span>
            </div>
            <p className="text-sm text-neutral-400 mt-1">Backend connection pending</p>
          </div>
        ))}
      </div>

      <div className="bg-white p-6 rounded-xl border border-neutral-200 shadow-sm h-96">
        <h3 className="text-lg font-semibold mb-4">Market Trend (Illustrative Placeholder)</h3>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey="time" axisLine={false} tickLine={false} />
            <YAxis domain={['auto', 'auto']} axisLine={false} tickLine={false} />
            <Tooltip />
            <Line type="monotone" dataKey="price" stroke="#2563EB" strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div className="bg-white p-6 rounded-xl border border-neutral-200 shadow-sm">
        <h3 className="text-lg font-semibold mb-4">Watchlist</h3>
        <div className="text-center py-12 text-neutral-500">
          No symbols added to watchlist.
        </div>
      </div>
    </div>
  );
};

export default Overview;
