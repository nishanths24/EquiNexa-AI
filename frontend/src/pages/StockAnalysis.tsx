
import { Lock } from 'lucide-react';

const StockAnalysis = () => {
  return (
    <div className="space-y-6 max-w-5xl">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold">Stock Analysis</h1>
          <p className="text-neutral-500 mt-1">Select a ticker to view technicals and prospective predictions.</p>
        </div>
      </div>

      <div className="bg-white border border-neutral-200 rounded-xl p-12 text-center">
        <Lock className="w-12 h-12 text-neutral-300 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-neutral-900">Prediction Unavailable</h3>
        <p className="text-neutral-500 mt-2 max-w-md mx-auto">
          No valid prediction data was returned. The prospective observation engine is currently accumulating N=100 observations. 
          Individual prediction insights will be unlocked after the review gate passes.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-xl border border-neutral-200 shadow-sm h-64 flex flex-col items-center justify-center">
          <p className="text-neutral-400">Technical Indicators (Unavailable)</p>
        </div>
        <div className="bg-white p-6 rounded-xl border border-neutral-200 shadow-sm h-64 flex flex-col items-center justify-center">
          <p className="text-neutral-400">Chart Patterns (Unavailable)</p>
        </div>
      </div>
    </div>
  );
};

export default StockAnalysis;
