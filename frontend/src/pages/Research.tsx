import { useEffect, useState } from 'react';
import { fetchProspectiveStatus, type ProspectiveStatus } from '../services/api/prospective';
import { fetchClient } from '../services/api/client';
import ReactMarkdown from 'react-markdown';
import { AlertCircle, Lock, Search, FileText } from 'lucide-react';

interface ResearchResult {
  ticker: string;
  query: string;
  report: string;
  citations: string[];
  timestamp: string;
  disclaimer: string;
}

const Research = () => {
  const [status, setStatus] = useState<ProspectiveStatus | null>(null);
  const [loading, setLoading] = useState(true);
  
  const [ticker, setTicker] = useState('');
  const [query, setQuery] = useState('');
  const [researching, setResearching] = useState(false);
  const [researchError, setResearchError] = useState<string | null>(null);
  const [result, setResult] = useState<ResearchResult | null>(null);

  useEffect(() => {
    fetchProspectiveStatus().then(data => {
      setStatus(data);
      setLoading(false);
    }).catch(() => {
      setLoading(false);
    });
  }, []);

  const handleResearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!ticker || !query) return;
    
    setResearching(true);
    setResearchError(null);
    setResult(null);
    
    try {
      const data = await fetchClient('/api/v1/research/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ticker, query })
      });
      setResult(data);
    } catch (err: any) {
      setResearchError(err.message || 'An error occurred during research.');
    } finally {
      setResearching(false);
    }
  };

  if (loading) return <div className="p-8 text-text-secondary">Loading prospective engine status...</div>;
  if (!status) return <div className="p-8 text-market-down">Error loading status. Ensure backend is running.</div>;

  return (
    <div className="space-y-6 max-w-5xl">
      <div>
        <h1 className="text-2xl font-bold text-text-primary">Research & Experiments</h1>
        <p className="text-text-secondary mt-1">Prospective Accumulation Status</p>
      </div>

      <div className="bg-card-bg border border-border-subtle rounded-lg p-4 flex items-start">
        <AlertCircle className="w-5 h-5 text-text-primary mt-0.5 mr-3 flex-shrink-0" />
        <div>
          <h4 className="text-sm font-semibold text-text-primary">Prospective evaluation in progress — no performance conclusion yet.</h4>
          <p className="text-sm text-text-secondary mt-1">The model is frozen at version {status.model_version}. We are awaiting {status.required} legitimate observations before opening the review gate.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-card-bg p-6 rounded-xl border border-border-subtle">
          <div className="text-sm text-text-muted mb-1">Evaluated</div>
          <div className="text-3xl font-bold text-text-primary">{status.evaluated}</div>
        </div>
        <div className="bg-card-bg p-6 rounded-xl border border-border-subtle">
          <div className="text-sm text-text-muted mb-1">Pending</div>
          <div className="text-3xl font-bold text-text-primary">{status.pending}</div>
        </div>
        <div className="bg-card-bg p-6 rounded-xl border border-border-subtle">
          <div className="text-sm text-text-muted mb-1">Remaining</div>
          <div className="text-3xl font-bold text-text-primary">{status.remaining}</div>
        </div>
        <div className="bg-card-bg p-6 rounded-xl border border-border-subtle flex flex-col items-center justify-center text-center">
          <Lock className="w-6 h-6 text-text-muted mb-2" />
          <div className="text-sm font-medium text-text-primary">Review Gate</div>
          <div className="text-xs text-text-secondary">{status.review_status}</div>
        </div>
      </div>

      <div className="bg-card-bg p-6 rounded-xl border border-border-subtle">
        <h3 className="text-lg font-semibold mb-4 text-text-primary">Historical Reference</h3>
        <p className="text-sm text-text-secondary mb-4">
          The frozen Phase 6 benchmark achieved 61.91% accuracy for the {status.target} target. 
          This is a historical experiment, not live performance, and does not guarantee future results.
        </p>
      </div>
      
      <div className="mt-12">
        <h2 className="text-xl font-bold text-text-primary mb-4">AI Research Assistant</h2>
        <div className="bg-card-bg border border-border-subtle rounded-xl p-6">
          <form onSubmit={handleResearch} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="md:col-span-1">
                <label className="block text-sm font-medium text-text-secondary mb-1">Ticker</label>
                <input 
                  type="text" 
                  value={ticker}
                  onChange={(e) => setTicker(e.target.value)}
                  placeholder="e.g. INFY.NS"
                  required
                  className="w-full bg-black-bg border border-border-subtle rounded-md px-3 py-2 text-text-primary placeholder:text-text-muted focus:outline-none focus:ring-1 focus:ring-text-secondary"
                />
              </div>
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-text-secondary mb-1">Research Query</label>
                <div className="flex">
                  <input 
                    type="text" 
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Ask about recent news, sentiment, or financials..."
                    required
                    className="flex-1 bg-black-bg border border-border-subtle rounded-l-md px-3 py-2 text-text-primary placeholder:text-text-muted focus:outline-none focus:ring-1 focus:ring-text-secondary"
                  />
                  <button 
                    type="submit"
                    disabled={researching}
                    className="bg-text-primary text-black-bg px-4 py-2 rounded-r-md font-medium hover:bg-white transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
                  >
                    {researching ? (
                      <div className="w-4 h-4 border-2 border-black-bg border-t-transparent rounded-full animate-spin"></div>
                    ) : (
                      <Search className="w-4 h-4" />
                    )}
                  </button>
                </div>
              </div>
            </div>
          </form>

          {researchError && (
            <div className="mt-6 bg-red-950/30 border border-market-down/50 rounded-lg p-4 flex items-start text-market-down">
              <AlertCircle className="w-5 h-5 mr-3 flex-shrink-0 mt-0.5" />
              <div>
                <h4 className="font-medium text-sm">Research Failed</h4>
                <p className="text-sm mt-1">{researchError}</p>
              </div>
            </div>
          )}

          {result && (
            <div className="mt-8 space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
              <div className="bg-black-bg border border-border-subtle rounded-lg p-6">
                <div className="flex items-center mb-4 pb-4 border-b border-border-subtle">
                  <FileText className="w-5 h-5 text-text-secondary mr-2" />
                  <h3 className="text-lg font-medium text-text-primary">Research Report: {result.ticker}</h3>
                </div>
                
                <div className="text-text-primary text-sm leading-relaxed whitespace-pre-wrap max-w-none">
                  <ReactMarkdown
                    components={{
                      h1: ({...props}) => <h1 className="text-2xl font-bold mt-6 mb-3" {...props} />,
                      h2: ({...props}) => <h2 className="text-xl font-bold mt-5 mb-3" {...props} />,
                      h3: ({...props}) => <h3 className="text-lg font-semibold mt-4 mb-2" {...props} />,
                      p: ({...props}) => <p className="mb-4" {...props} />,
                      ul: ({...props}) => <ul className="list-disc list-inside mb-4" {...props} />,
                      ol: ({...props}) => <ol className="list-decimal list-inside mb-4" {...props} />,
                      li: ({...props}) => <li className="mb-1" {...props} />,
                      a: ({...props}) => <a className="text-blue-400 hover:underline" target="_blank" rel="noopener noreferrer" {...props} />,
                      strong: ({...props}) => <strong className="font-bold text-white" {...props} />,
                    }}
                  >
                    {result.report}
                  </ReactMarkdown>
                </div>
                
                <div className="mt-6 pt-4 border-t border-border-subtle">
                  <h4 className="text-xs font-semibold text-text-secondary uppercase tracking-wider mb-2">Sources & Citations</h4>
                  <ul className="list-disc list-inside text-xs text-text-muted">
                    {result.citations.map((c, i) => <li key={i}>{c}</li>)}
                  </ul>
                  <p className="text-xs text-text-muted mt-2">Generated at: {new Date(result.timestamp).toLocaleString()}</p>
                </div>
                
                <div className="mt-4 pt-4 border-t border-border-subtle flex items-start">
                   <AlertCircle className="w-4 h-4 text-text-muted mt-0.5 mr-2" />
                   <p className="text-xs text-text-muted">
                     {result.disclaimer}
                   </p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Research;
