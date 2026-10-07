import { useState, useRef } from 'react';
import { UploadCloud, AlertTriangle, X, CheckCircle, BarChart2 } from 'lucide-react';
import { analyzeChartImage, type VisionAnalysisResponse } from '../services/api/vision';

const ChartVision = () => {
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [ticker, setTicker] = useState('');
  const [timeframe, setTimeframe] = useState('1d');
  
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState<VisionAnalysisResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      processFile(e.target.files[0]);
    }
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      processFile(e.dataTransfer.files[0]);
    }
  };

  const processFile = (selectedFile: File) => {
    setError(null);
    setResult(null);
    
    // Client-side validation
    const validTypes = ['image/jpeg', 'image/png', 'image/webp'];
    if (!validTypes.includes(selectedFile.type)) {
      setError('Please upload a valid PNG, JPEG, or WebP image.');
      return;
    }
    
    if (selectedFile.size > 5 * 1024 * 1024) {
      setError('Image exceeds 5MB limit.');
      return;
    }

    setFile(selectedFile);
    setPreviewUrl(URL.createObjectURL(selectedFile));
  };

  const removeImage = () => {
    setFile(null);
    setPreviewUrl(null);
    setResult(null);
    setError(null);
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  const handleAnalyze = async () => {
    if (!file) return;
    
    setAnalyzing(true);
    setError(null);
    setResult(null);
    
    try {
      const data = await analyzeChartImage(file, ticker, timeframe);
      setResult(data);
    } catch (err: any) {
      setError(err.message || 'An unexpected error occurred during analysis.');
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <div className="max-w-4xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-text-primary">AI Chart Vision</h1>
        <p className="text-text-secondary mt-1">Upload a candlestick chart for AI-powered pattern recognition and technical interpretation.</p>
      </div>

      <div className="bg-card-bg border border-border-subtle rounded-xl p-6 shadow-sm">
        <h2 className="text-lg font-medium text-text-primary mb-4">New Analysis</h2>
        
        {!file ? (
          <div 
            className="border-2 border-dashed border-border-subtle rounded-lg p-12 flex flex-col items-center justify-center text-center cursor-pointer hover:bg-hover-bg transition-colors"
            onDragOver={(e) => e.preventDefault()}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
          >
            <UploadCloud className="w-12 h-12 text-text-muted mb-4" />
            <h3 className="text-text-primary font-medium">Drag & drop your chart here</h3>
            <p className="text-sm text-text-muted mt-1 mb-4">Supports PNG, JPEG, WebP (max 5MB)</p>
            <button className="px-4 py-2 bg-text-primary text-black-bg font-medium rounded-md hover:bg-white transition-colors">
              Choose chart image
            </button>
            <input 
              type="file" 
              ref={fileInputRef} 
              className="hidden" 
              accept="image/png, image/jpeg, image/webp" 
              onChange={handleFileChange} 
            />
          </div>
        ) : (
          <div className="space-y-6">
            <div className="relative border border-border-subtle rounded-lg overflow-hidden bg-black-bg">
              <button 
                onClick={removeImage}
                className="absolute top-2 right-2 p-1 bg-black/50 text-white rounded-full hover:bg-black transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
              <img src={previewUrl!} alt="Chart Preview" className="max-h-96 w-full object-contain" />
            </div>
            
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-1">Ticker (Optional)</label>
                <input 
                  type="text" 
                  value={ticker}
                  onChange={(e) => setTicker(e.target.value)}
                  placeholder="e.g. AAPL"
                  className="w-full bg-black-bg border border-border-subtle rounded-md px-3 py-2 text-text-primary placeholder:text-text-muted focus:outline-none focus:ring-1 focus:ring-text-secondary"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-1">Timeframe</label>
                <select 
                  value={timeframe}
                  onChange={(e) => setTimeframe(e.target.value)}
                  className="w-full bg-black-bg border border-border-subtle rounded-md px-3 py-2 text-text-primary focus:outline-none focus:ring-1 focus:ring-text-secondary"
                >
                  <option value="1m">1 Minute</option>
                  <option value="5m">5 Minutes</option>
                  <option value="15m">15 Minutes</option>
                  <option value="1h">1 Hour</option>
                  <option value="4h">4 Hours</option>
                  <option value="1d">1 Day</option>
                  <option value="1w">1 Week</option>
                </select>
              </div>
            </div>

            <div className="flex justify-end">
              <button 
                onClick={handleAnalyze}
                disabled={analyzing}
                className="px-6 py-2 bg-text-primary text-black-bg font-medium rounded-md hover:bg-white transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
              >
                {analyzing ? (
                  <>
                    <div className="w-4 h-4 border-2 border-black-bg border-t-transparent rounded-full animate-spin mr-2"></div>
                    Analyzing...
                  </>
                ) : (
                  <>
                    <BarChart2 className="w-4 h-4 mr-2" />
                    Analyze Chart
                  </>
                )}
              </button>
            </div>
          </div>
        )}

        {error && (
          <div className="mt-6 bg-red-950/30 border border-market-down/50 rounded-lg p-4 flex items-start text-market-down">
            <AlertTriangle className="w-5 h-5 mr-3 flex-shrink-0 mt-0.5" />
            <div>
              <h4 className="font-medium text-sm">Analysis Unavailable</h4>
              <p className="text-sm mt-1 text-red-400">{error}</p>
            </div>
          </div>
        )}

        {result && (
          <div className="mt-8 space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <h3 className="text-lg font-medium text-text-primary border-b border-border-subtle pb-2">Analysis Report</h3>
            
            {!result.has_sufficient_evidence && (
              <div className="bg-yellow-950/30 border border-yellow-700/50 rounded-lg p-4 text-yellow-500 text-sm">
                Insufficient visual evidence or unclear candles detected. Patterns and levels may be highly inaccurate.
              </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-black-bg border border-border-subtle rounded-lg p-4">
                <h4 className="text-sm text-text-muted mb-3 uppercase tracking-wider">Observed Chart Structure</h4>
                <div className="space-y-4">
                  <div>
                    <span className="text-text-secondary text-sm">Detected Trend</span>
                    <p className="text-text-primary font-medium capitalize mt-1">{result.detected_trend}</p>
                  </div>
                  <div>
                    <span className="text-text-secondary text-sm">Support Levels</span>
                    <div className="flex flex-wrap gap-2 mt-1">
                      {result.support_levels.length > 0 ? result.support_levels.map((lvl, i) => (
                        <span key={i} className="px-2 py-1 bg-border-subtle text-text-primary text-xs rounded">
                          {String(lvl).toLowerCase().includes('unavailable') || String(lvl).toLowerCase().includes('unclear') ? lvl : `$${lvl}`}
                        </span>
                      )) : <span className="text-text-muted text-sm">None clear</span>}
                    </div>
                  </div>
                  <div>
                    <span className="text-text-secondary text-sm">Resistance Levels</span>
                    <div className="flex flex-wrap gap-2 mt-1">
                      {result.resistance_levels.length > 0 ? result.resistance_levels.map((lvl, i) => (
                        <span key={i} className="px-2 py-1 bg-border-subtle text-text-primary text-xs rounded">
                          {String(lvl).toLowerCase().includes('unavailable') || String(lvl).toLowerCase().includes('unclear') ? lvl : `$${lvl}`}
                        </span>
                      )) : <span className="text-text-muted text-sm">None clear</span>}
                    </div>
                  </div>
                </div>
              </div>

              <div className="bg-black-bg border border-border-subtle rounded-lg p-4">
                <h4 className="text-sm text-text-muted mb-3 uppercase tracking-wider">Detected Patterns</h4>
                {result.patterns.length > 0 ? (
                  <ul className="space-y-2">
                    {result.patterns.map((p, i) => (
                      <li key={i} className="flex items-center text-text-primary text-sm">
                        <CheckCircle className="w-4 h-4 text-market-up mr-2" />
                        {p}
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-text-muted text-sm">No distinct candlestick or chart formations detected.</p>
                )}
              </div>
            </div>

            <div className="bg-black-bg border border-border-subtle rounded-lg p-4">
              <h4 className="text-sm text-text-muted mb-3 uppercase tracking-wider">Interpretation & Scenarios</h4>
              <p className="text-text-primary text-sm leading-relaxed whitespace-pre-wrap">
                {result.reasoning}
              </p>
              
              <div className="mt-4 pt-4 border-t border-border-subtle flex items-start">
                 <AlertTriangle className="w-4 h-4 text-text-muted mt-0.5 mr-2" />
                 <p className="text-xs text-text-muted">
                   This technical research is derived entirely from visual estimation of the uploaded image. It is not personalized financial advice and does not guarantee future price movement.
                 </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ChartVision;
