import { useEffect, useState } from 'react';
import { fetchProspectiveStatus, type ProspectiveStatus } from '../services/api/prospective';
import { AlertCircle, Lock } from 'lucide-react';

const Research = () => {
  const [status, setStatus] = useState<ProspectiveStatus | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProspectiveStatus().then(data => {
      setStatus(data);
      setLoading(false);
    });
  }, []);

  if (loading) return <div className="p-8">Loading prospective engine status...</div>;
  if (!status) return <div className="p-8">Error loading status.</div>;

  return (
    <div className="space-y-6 max-w-5xl">
      <div>
        <h1 className="text-2xl font-bold">Research & Experiments</h1>
        <p className="text-neutral-500 mt-1">Prospective Accumulation Status</p>
      </div>

      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 flex items-start">
        <AlertCircle className="w-5 h-5 text-blue-600 mt-0.5 mr-3 flex-shrink-0" />
        <div>
          <h4 className="text-sm font-semibold text-blue-900">Prospective evaluation in progress — no performance conclusion yet.</h4>
          <p className="text-sm text-blue-800 mt-1">The model is frozen at version {status.model_version}. We are awaiting {status.required} legitimate observations before opening the review gate.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-xl border border-neutral-200">
          <div className="text-sm text-neutral-500 mb-1">Evaluated</div>
          <div className="text-3xl font-bold">{status.evaluated}</div>
        </div>
        <div className="bg-white p-6 rounded-xl border border-neutral-200">
          <div className="text-sm text-neutral-500 mb-1">Pending</div>
          <div className="text-3xl font-bold">{status.pending}</div>
        </div>
        <div className="bg-white p-6 rounded-xl border border-neutral-200">
          <div className="text-sm text-neutral-500 mb-1">Remaining</div>
          <div className="text-3xl font-bold">{status.remaining}</div>
        </div>
        <div className="bg-white p-6 rounded-xl border border-neutral-200 flex flex-col items-center justify-center text-center">
          <Lock className="w-6 h-6 text-neutral-400 mb-2" />
          <div className="text-sm font-medium text-neutral-900">Review Gate</div>
          <div className="text-xs text-neutral-500">{status.review_status}</div>
        </div>
      </div>

      <div className="bg-white p-6 rounded-xl border border-neutral-200">
        <h3 className="text-lg font-semibold mb-4">Historical Reference</h3>
        <p className="text-sm text-neutral-600 mb-4">
          The frozen Phase 6 benchmark achieved 61.91% accuracy for the {status.target} target. 
          This is a historical experiment, not live performance, and does not guarantee future results.
        </p>
      </div>
    </div>
  );
};

export default Research;
