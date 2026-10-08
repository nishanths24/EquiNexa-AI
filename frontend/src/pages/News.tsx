import { useState } from 'react';
import { Search, ExternalLink, Clock, TrendingUp, TrendingDown, Minus, Filter, AlertTriangle, FileText } from 'lucide-react';

// Mock data to illustrate the V2 UI
const MOCK_CATEGORIES = [
  "All", "Indian Markets", "Global Markets", "Company News", "Corporate Actions", 
  "Central Banks", "Economy", "Geopolitics", "Commodities", "Technology"
];

const MOCK_NEWS = [
  {
    id: 1,
    headline: "RBI Maintains Repo Rate at 6.5%, Shifts Stance to Neutral",
    summary: "The Reserve Bank of India kept the policy repo rate unchanged at 6.5% for the tenth consecutive meeting, signaling a potential shift towards easing in upcoming quarters.",
    source: "Central Bank Wire",
    published_at: "10 mins ago",
    sentiment: 0.2, // Positive
    importance: "HIGH",
    symbols: ["NIFTY", "BANKNIFTY"],
    category: "Central Banks"
  },
  {
    id: 2,
    headline: "TCS Q2 Results: Net Profit Rises 8% to ₹11,342 Crore",
    summary: "Tata Consultancy Services reported an 8% year-on-year growth in net profit, beating street estimates driven by strong performance in the BFSI sector.",
    source: "Financial Express",
    published_at: "1 hr ago",
    sentiment: 0.8,
    importance: "HIGH",
    symbols: ["TCS.NS"],
    category: "Earnings"
  },
  {
    id: 3,
    headline: "Oil Prices Surge 4% Amid Geopolitical Tensions in Middle East",
    summary: "Brent crude prices spiked above $80 a barrel as supply concerns mount due to escalating conflict, pushing energy stocks higher globally.",
    source: "Global Energy News",
    published_at: "2 hrs ago",
    sentiment: -0.6,
    importance: "HIGH",
    symbols: ["BRENT", "ONGC.NS"],
    category: "Commodities"
  },
  {
    id: 4,
    headline: "Tech Sector Faces Regulatory Headwinds in EU Over AI Rules",
    summary: "Major tech firms may face increased scrutiny as the EU rolls out stringent compliance checks for generative AI models starting next month.",
    source: "Tech Policy Insider",
    published_at: "4 hrs ago",
    sentiment: -0.3,
    importance: "MEDIUM",
    symbols: ["MSFT", "GOOGL"],
    category: "Technology"
  },
  {
    id: 5,
    headline: "Market Update: Nifty Consolidated After Reaching New All-Time High",
    summary: "The Nifty 50 index traded in a narrow range today, consolidating recent gains as investors await key inflation data from the US later this week.",
    source: "EquiNexa Market Desk",
    published_at: "5 hrs ago",
    sentiment: 0.0,
    importance: "LOW",
    symbols: ["NIFTY"],
    category: "Indian Markets"
  }
];

const News = () => {
  const [activeCategory, setActiveCategory] = useState("All");
  const [searchQuery, setSearchQuery] = useState("");

  const filteredNews = MOCK_NEWS.filter(article => {
    const matchesCategory = activeCategory === "All" || article.category === activeCategory;
    const matchesSearch = article.headline.toLowerCase().includes(searchQuery.toLowerCase()) || 
                          article.symbols.some(s => s.toLowerCase().includes(searchQuery.toLowerCase()));
    return matchesCategory && matchesSearch;
  });

  const getSentimentIcon = (score: number) => {
    if (score > 0.1) return <TrendingUp className="w-4 h-4 text-market-up" />;
    if (score < -0.1) return <TrendingDown className="w-4 h-4 text-market-down" />;
    return <Minus className="w-4 h-4 text-text-muted" />;
  };

  const getSentimentColor = (score: number) => {
    if (score > 0.1) return "text-eq-green bg-transparent border-transparent";
    if (score < -0.1) return "text-eq-red bg-transparent border-transparent";
    return "text-eq-text-secondary bg-transparent border-transparent";
  };

  const getImportanceBadge = (importance: string) => {
    if (importance === "HIGH") {
      return (
        <span className="flex items-center text-[11px] font-medium text-[#D6453D] bg-[#FFF5F4] px-1.5 py-0.5 rounded border border-[#D6453D]">
          <AlertTriangle className="w-3 h-3 mr-1" />
          HIGH IMPACT
        </span>
      );
    }
    return null;
  };

  return (
    <div className="flex flex-col h-full bg-black-bg text-text-primary p-6 max-w-7xl mx-auto w-full space-y-6">
      
      {/* Header section */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-semibold text-eq-text">News Terminal</h1>
          <p className="text-[13px] text-eq-text-secondary mt-1">Real-time global market news, sentiment analysis, and corporate actions.</p>
        </div>
        
        <div className="relative w-full md:w-72">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Search className="w-4 h-4 text-text-muted" />
          </div>
          <input 
            type="text" 
            placeholder="Search news or symbols..." 
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2 bg-card-bg border border-border-subtle rounded-md text-sm text-text-primary placeholder:text-text-muted focus:outline-none focus:ring-1 focus:ring-text-secondary transition-shadow"
          />
        </div>
      </div>

      {/* Categories Bar */}
      <div className="flex flex-row md:flex-wrap items-center overflow-x-auto md:overflow-x-visible pb-2 md:pb-0 space-x-2 md:space-x-0 md:gap-2 scrollbar-hide w-full min-w-0">
        <div className="flex items-center text-eq-text-muted shrink-0 md:mr-2">
          <Filter className="w-4 h-4 mr-1" />
          <span className="text-[13px] font-medium">Filter:</span>
        </div>
        {MOCK_CATEGORIES.map(category => (
          <button
            key={category}
            onClick={() => setActiveCategory(category)}
            className={`whitespace-nowrap px-3 py-1 rounded text-[13px] font-medium transition-colors border ${
              activeCategory === category 
                ? 'bg-eq-purple text-white border-eq-purple' 
                : 'bg-transparent text-eq-text-secondary border-eq-border hover:bg-eq-surface-elevated hover:text-eq-text'
            }`}
          >
            {category}
          </button>
        ))}
      </div>

      {/* Main News Feed layout */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 flex-1 min-h-0">
        
        {/* News List */}
        <div className="lg:col-span-3 flex flex-col space-y-4 overflow-y-auto pr-2 pb-10">
          
          <div className="flex items-center justify-between mb-2">
            <h2 className="text-[14px] font-semibold flex items-center text-eq-text">
              <span className="flex h-1.5 w-1.5 mr-2 rounded-full bg-eq-green"></span>
              Live Feed
            </h2>
            <span className="text-xs text-text-muted">Showing {filteredNews.length} articles</span>
          </div>

          {filteredNews.length === 0 ? (
            <div className="bg-card-bg border border-border-subtle rounded-lg p-10 flex flex-col items-center justify-center text-center">
              <FileText className="w-12 h-12 text-border-subtle mb-4" />
              <p className="text-text-secondary font-medium">No articles found</p>
              <p className="text-sm text-text-muted mt-1">Try adjusting your filters or search query.</p>
            </div>
          ) : (
            filteredNews.map(article => (
              <div key={article.id} className="bg-eq-surface-card border border-eq-border rounded p-4 hover:border-eq-purple/40 transition-colors cursor-pointer group">
                <div className="flex justify-between items-start mb-3">
                  <div className="flex items-center space-x-3 text-[12px]">
                    <span className="font-semibold text-eq-text-secondary">{article.source}</span>
                    <span className="text-eq-text-muted flex items-center">
                      <Clock className="w-3 h-3 mr-1" />
                      {article.published_at}
                    </span>
                  </div>
                  {getImportanceBadge(article.importance)}
                </div>
                
                <h3 className="text-[16px] font-semibold text-eq-text mb-2 group-hover:text-eq-purple transition-colors">
                  {article.headline}
                </h3>
                
                <p className="text-[14px] text-eq-text-secondary mb-4 line-clamp-2 leading-relaxed">
                  {article.summary}
                </p>
                
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    {article.symbols.map(sym => (
                      <span key={sym} className="px-1.5 py-0.5 bg-eq-surface-elevated border border-eq-border rounded text-[11px] text-eq-text-secondary">
                        {sym}
                      </span>
                    ))}
                  </div>
                  
                  <div className="flex items-center space-x-4">
                    <div className={`flex items-center space-x-1 px-2 py-1 rounded border text-[12px] font-medium ${getSentimentColor(article.sentiment)}`}>
                      {getSentimentIcon(article.sentiment)}
                      <span>
                        {article.sentiment > 0.1 ? 'Positive' : article.sentiment < -0.1 ? 'Negative' : 'Neutral'}
                      </span>
                    </div>
                    <button className="text-text-muted hover:text-text-primary transition-colors">
                      <ExternalLink className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>

        {/* Sidebar Analytics */}
        <div className="hidden lg:flex flex-col space-y-6">
          <div className="bg-card-bg border border-border-subtle rounded-lg p-5">
            <h3 className="text-sm font-semibold text-text-secondary uppercase tracking-wider mb-4">Market Sentiment</h3>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span>Bullish</span>
                  <span className="text-market-up font-mono">62%</span>
                </div>
                <div className="w-full bg-border-subtle rounded-full h-1.5">
                  <div className="bg-market-up h-1.5 rounded-full" style={{ width: '62%' }}></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span>Bearish</span>
                  <span className="text-market-down font-mono">24%</span>
                </div>
                <div className="w-full bg-border-subtle rounded-full h-1.5">
                  <div className="bg-market-down h-1.5 rounded-full" style={{ width: '24%' }}></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span>Neutral</span>
                  <span className="text-text-muted font-mono">14%</span>
                </div>
                <div className="w-full bg-border-subtle rounded-full h-1.5">
                  <div className="bg-text-muted h-1.5 rounded-full" style={{ width: '14%' }}></div>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-card-bg border border-border-subtle rounded-lg p-5 flex-1">
            <h3 className="text-sm font-semibold text-text-secondary uppercase tracking-wider mb-4">Trending Symbols</h3>
            <div className="space-y-3">
              {['TCS.NS', 'RELIANCE.NS', 'NIFTY', 'HDFCBANK.NS', 'INFY.NS'].map((sym, idx) => (
                <div key={sym} className="flex items-center justify-between p-2 rounded hover:bg-hover-bg cursor-pointer transition-colors">
                  <span className="font-mono text-sm text-text-primary">{sym}</span>
                  <div className="flex items-center space-x-2">
                    <span className="text-xs text-text-muted">{15 - idx * 2} mentions</span>
                    {idx % 2 === 0 ? <TrendingUp className="w-3 h-3 text-market-up" /> : <TrendingDown className="w-3 h-3 text-market-down" />}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
        
      </div>
    </div>
  );
};

export default News;
