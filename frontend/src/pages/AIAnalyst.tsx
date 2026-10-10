import { useState } from 'react';
import { AlertCircle, Upload, X, Search } from 'lucide-react';
import { API_BASE } from '../services/api/client';

const AIAnalyst = () => {
  const [ticker, setTicker] = useState('RELIANCE.NS');
  const [mode, setMode] = useState<'live' | 'image'>('live');
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [report, setReport] = useState<any>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      if (file.size > 5 * 1024 * 1024) {
        setErrorMsg("Image exceeds 5MB limit.");
        return;
      }
      setImageFile(file);
      setImagePreview(URL.createObjectURL(file));
      setErrorMsg(null);
      setReport(null);
    }
  };

  const removeImage = () => {
    setImageFile(null);
    setImagePreview(null);
    setReport(null);
  };

  const runAnalysis = async () => {
    if (mode === 'image' && !imageFile) {
        setErrorMsg("Please upload an image first.");
        return;
    }
    
    setIsAnalyzing(true);
    setErrorMsg(null);
    setReport(null);
    
    try {
      const baseUrl = API_BASE;
      
      let res;
      if (mode === 'live') {
          res = await fetch(`${baseUrl}/api/v1/research/query`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ticker, query: "Provide a detailed bullish/bearish market analysis." })
          });
      } else {
          const formData = new FormData();
          formData.append('file', imageFile!);
          if (ticker) formData.append('ticker', ticker);
          
          res = await fetch(`${baseUrl}/api/v1/vision/analyze`, {
            method: 'POST',
            body: formData
          });
      }
      
      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        const msg = errData.detail?.message || errData.detail || `HTTP error ${res.status}`;
        throw new Error(typeof msg === 'string' ? msg : JSON.stringify(msg));
      }
      
      const data = await res.json();
      setReport(data);
    } catch (e: any) {
      console.error(e);
      setErrorMsg(e.message || "An error occurred during analysis.");
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="min-h-[calc(100vh-64px)] bg-eq-bg text-eq-text overflow-y-auto flex justify-center items-center p-4 lg:p-8">
      <div className="w-full max-w-[1250px] flex flex-col md:flex-row gap-8 items-stretch">
        
        {/* Left Column: Controls */}
        <div className="w-full md:w-[380px] flex-shrink-0 flex flex-col">
          <div className="p-6 border border-eq-border bg-eq-surface rounded-lg shadow-sm flex flex-col h-full">
            <h1 className="text-xl font-bold text-eq-purple mb-6">EquiNexa AI Analyst</h1>
            
            <div className="flex flex-col space-y-2 mb-6">
                <button 
                  onClick={() => { setMode('live'); setReport(null); setErrorMsg(null); }}
                  className={`px-4 py-2 rounded text-sm font-medium transition-colors text-left ${mode === 'live' ? 'bg-eq-purple text-white' : 'bg-eq-surface-elevated text-eq-text-secondary hover:text-eq-text'}`}
                >
                    Live Market Analysis
                </button>
                <button 
                  onClick={() => { setMode('image'); setReport(null); setErrorMsg(null); }}
                  className={`px-4 py-2 rounded text-sm font-medium transition-colors text-left ${mode === 'image' ? 'bg-eq-purple text-white' : 'bg-eq-surface-elevated text-eq-text-secondary hover:text-eq-text'}`}
                >
                    Analyze Chart Image
                </button>
            </div>
            
            <div className="flex flex-col space-y-5 flex-1">
                <div>
                    <label className="block text-xs text-eq-text-secondary uppercase mb-1.5 font-medium">Instrument Symbol</label>
                    <div className="relative">
                        <Search className="absolute left-3 top-2.5 w-4 h-4 text-eq-text-muted" />
                        <input 
                            type="text" 
                            value={ticker}
                            onChange={e => setTicker(e.target.value.toUpperCase())}
                            placeholder="e.g. RELIANCE.NS"
                            className="w-full bg-eq-surface-elevated border border-eq-border rounded pl-9 pr-4 py-2 text-sm focus:outline-none focus:border-eq-purple transition-colors"
                        />
                    </div>
                </div>
                
                {mode === 'image' && (
                    <div>
                        <label className="block text-xs text-eq-text-secondary uppercase mb-1.5 font-medium">Chart Screenshot</label>
                        {imagePreview ? (
                            <div className="relative w-full border border-eq-border rounded overflow-hidden">
                                <img src={imagePreview} alt="Preview" className="w-full h-auto object-contain" />
                                <button onClick={removeImage} className="absolute top-2 right-2 p-1 bg-black/60 hover:bg-black/80 rounded-full text-white transition-colors">
                                    <X className="w-4 h-4" />
                                </button>
                            </div>
                        ) : (
                            <label className="flex flex-col items-center justify-center w-full h-32 border-2 border-dashed border-eq-border rounded cursor-pointer hover:border-eq-purple transition-colors bg-eq-surface-elevated">
                                <Upload className="w-6 h-6 text-eq-text-muted mb-2" />
                                <span className="text-sm text-eq-text-secondary">Upload Image</span>
                                <span className="text-[10px] text-eq-text-muted mt-1 uppercase">PNG, JPG, WebP &lt;5MB</span>
                                <input type="file" accept="image/png, image/jpeg, image/jpg, image/webp" className="hidden" onChange={handleImageUpload} />
                            </label>
                        )}
                    </div>
                )}
            </div>

            <button 
                onClick={runAnalysis}
                disabled={isAnalyzing || (mode === 'image' && !imageFile)}
                className="w-full mt-6 py-2.5 bg-eq-purple hover:bg-eq-purple-hover disabled:opacity-50 disabled:cursor-not-allowed text-white rounded font-medium transition-colors"
            >
                {isAnalyzing ? "Analyzing..." : "Analyze"}
            </button>
          </div>
        </div>

        {/* Right Column: Results */}
        <div className="w-full flex-1 flex flex-col">
          <div className={`p-6 border border-eq-border bg-eq-surface rounded-lg shadow-sm flex-1 ${!report && !errorMsg && !isAnalyzing ? 'flex items-center justify-center' : ''}`}>
            
            {errorMsg && (
                <div className="p-4 border border-eq-red bg-eq-red/10 rounded flex items-start flex-col">
                    <div className="flex items-center mb-3">
                        <AlertCircle className="w-5 h-5 text-eq-red mr-2 flex-shrink-0" />
                        <h3 className="font-semibold text-eq-red">Analysis Failed</h3>
                    </div>
                    <p className="text-sm text-eq-text mb-4">{errorMsg}</p>
                    <button onClick={runAnalysis} className="px-4 py-1.5 bg-eq-surface border border-eq-border hover:border-eq-text transition-colors rounded text-sm font-medium">
                        Retry
                    </button>
                </div>
            )}
            
            {isAnalyzing && (
                <div className="flex flex-col items-center justify-center h-full py-12">
                    <div className="w-10 h-10 border-4 border-eq-border border-t-eq-purple rounded-full animate-spin mb-4"></div>
                    <p className="text-eq-text-secondary font-medium animate-pulse">Running AI Analysis...</p>
                </div>
            )}
            
            {!isAnalyzing && !report && !errorMsg && (
                <div className="text-center max-w-sm">
                    <div className="w-16 h-16 bg-eq-surface-elevated rounded-full flex items-center justify-center mx-auto mb-4">
                        <Search className="w-8 h-8 text-eq-purple/50" />
                    </div>
                    <h3 className="text-lg font-medium text-eq-text mb-2">Ready to Analyze</h3>
                    <p className="text-sm text-eq-text-secondary">
                        Enter an instrument symbol or upload a chart screenshot to receive detailed market direction and setup insights.
                    </p>
                </div>
            )}

            {report && !isAnalyzing && (
                <div className="space-y-6">
                    {report.has_sufficient_evidence === false && (
                        <div className="p-4 border border-eq-orange bg-eq-orange/10 rounded text-eq-orange text-sm">
                            <strong>Warning:</strong> The image does not contain sufficient clear evidence to form a reliable analysis. Estimates below may be highly uncertain.
                        </div>
                    )}
                    
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        {/* Market Direction */}
                        {report.market_direction && (
                            <div className="bg-eq-surface-elevated border border-eq-border rounded p-4">
                                <h3 className="text-[11px] text-eq-text-secondary uppercase mb-2 tracking-wider font-semibold">Market Direction</h3>
                                <div className={`text-lg font-bold mb-2 capitalize ${report.market_direction.bias === 'bullish' ? 'text-eq-green' : report.market_direction.bias === 'bearish' ? 'text-eq-red' : 'text-eq-orange'}`}>
                                    {report.market_direction.bias}
                                </div>
                                <p className="text-sm text-eq-text mb-2 line-clamp-3" title={report.market_direction.evidence}>{report.market_direction.evidence}</p>
                                <div className="text-[11px] text-eq-text-secondary">
                                    <span className="font-medium">Confidence:</span> {report.market_direction.confidence}
                                </div>
                            </div>
                        )}
                        
                        {/* Trade Setup */}
                        {report.trade_setup && (
                            <div className="bg-eq-surface-elevated border border-eq-border rounded p-4">
                                <h3 className="text-[11px] text-eq-text-secondary uppercase mb-3 tracking-wider font-semibold">Trade Setup</h3>
                                <div className="space-y-2 text-sm">
                                    <div className="flex justify-between border-b border-eq-border pb-1">
                                        <span className="text-eq-text-secondary">Entry</span>
                                        <span className="font-medium text-right max-w-[60%] truncate" title={report.trade_setup.entry_zone}>{report.trade_setup.entry_zone}</span>
                                    </div>
                                    <div className="flex justify-between border-b border-eq-border pb-1">
                                        <span className="text-eq-text-secondary">Targets</span>
                                        <span className="text-eq-green font-medium text-right max-w-[60%] truncate" title={Array.isArray(report.trade_setup.targets) ? report.trade_setup.targets.join(', ') : report.trade_setup.targets}>
                                            {Array.isArray(report.trade_setup.targets) ? report.trade_setup.targets.join(', ') : report.trade_setup.targets}
                                        </span>
                                    </div>
                                    <div className="flex justify-between border-b border-eq-border pb-1">
                                        <span className="text-eq-text-secondary">Stop Loss</span>
                                        <span className="text-eq-red font-medium text-right max-w-[60%] truncate" title={report.trade_setup.stop_loss}>{report.trade_setup.stop_loss}</span>
                                    </div>
                                    <div className="flex justify-between pb-1">
                                        <span className="text-eq-text-secondary">R/R</span>
                                        <span className="font-medium">{report.trade_setup.risk_reward}</span>
                                    </div>
                                </div>
                            </div>
                        )}
                        
                        {/* Risk Assessment */}
                        {report.risk_assessment && (
                            <div className="bg-eq-surface-elevated border border-eq-border rounded p-4 sm:col-span-2">
                                <h3 className="text-[11px] text-eq-text-secondary uppercase mb-3 tracking-wider font-semibold">Risk Assessment</h3>
                                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm">
                                    <div>
                                        <span className="text-eq-text-secondary block text-xs mb-0.5">Volatility & Uncertainty</span>
                                        <p>{report.risk_assessment.volatility}</p>
                                    </div>
                                    <div>
                                        <span className="text-eq-text-secondary block text-xs mb-0.5">Key Levels</span>
                                        <p>{report.risk_assessment.key_levels}</p>
                                    </div>
                                </div>
                            </div>
                        )}
                        
                        {/* News Summary */}
                        {report.news_summary && (
                            <div className="bg-eq-surface-elevated border border-eq-border rounded p-4 sm:col-span-2">
                                <h3 className="text-[11px] text-eq-text-secondary uppercase mb-2 tracking-wider font-semibold">Recent Catalysts</h3>
                                <p className="text-sm text-eq-text leading-relaxed whitespace-pre-line">
                                    {report.news_summary}
                                </p>
                            </div>
                        )}
                        
                        {/* Patterns */}
                        {report.patterns && report.patterns.length > 0 && (
                            <div className="bg-eq-surface-elevated border border-eq-border rounded p-4 sm:col-span-2">
                                <h3 className="text-[11px] text-eq-text-secondary uppercase mb-2 tracking-wider font-semibold">Detected Patterns</h3>
                                <div className="flex flex-wrap gap-2">
                                    {report.patterns.map((p: string, i: number) => (
                                        <span key={i} className="px-2 py-1 bg-eq-surface border border-eq-border rounded text-[11px] font-medium text-eq-text-secondary">
                                            {p}
                                        </span>
                                    ))}
                                </div>
                            </div>
                        )}
                    </div>
                    
                    {report.disclaimer && (
                        <div className="p-3 border border-eq-orange-muted bg-[rgba(234,88,12,0.05)] rounded flex items-start">
                            <AlertCircle className="w-4 h-4 text-eq-orange mr-2 flex-shrink-0 mt-0.5" />
                            <p className="text-[11px] text-eq-text-secondary leading-tight">
                                <strong className="text-eq-orange mr-1">DISCLAIMER:</strong>
                                {report.disclaimer}
                            </p>
                        </div>
                    )}
                </div>
            )}
          </div>
        </div>
        
      </div>
    </div>
  );
};

export default AIAnalyst;
