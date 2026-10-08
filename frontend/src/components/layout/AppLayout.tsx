import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom';
import { Activity, LayoutDashboard, LineChart, Beaker, Image as ImageIcon, Settings, Search, FileText, DollarSign, Globe, Filter, Star, Bell, Briefcase, User, Shield, Menu, X } from 'lucide-react';
import { useState, useEffect, useRef } from 'react';
import { searchMarkets, type SearchResult } from '../../services/api/markets';

const AppLayout = () => {
  const location = useLocation();
  const navigate = useNavigate();
  
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [searching, setSearching] = useState(false);
  const [searchOpen, setSearchOpen] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  
  const searchRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (searchRef.current && !searchRef.current.contains(event.target as Node)) {
        setSearchOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  useEffect(() => {
    const debounceTimer = setTimeout(async () => {
      if (searchQuery.trim().length >= 2) {
        setSearching(true);
        try {
          const results = await searchMarkets(searchQuery);
          setSearchResults(results);
          setSearchOpen(true);
        } catch (e) {
          console.error(e);
        } finally {
          setSearching(false);
        }
      } else {
        setSearchResults([]);
        setSearchOpen(false);
      }
    }, 400);

    return () => clearTimeout(debounceTimer);
  }, [searchQuery]);

  const handleSelectSymbol = (symbol: string) => {
    setSearchOpen(false);
    setSearchQuery('');
    navigate(`/analysis?ticker=${encodeURIComponent(symbol)}`);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && searchQuery.trim()) {
      setSearchOpen(false);
      navigate(`/analysis?ticker=${encodeURIComponent(searchQuery.trim())}`);
    }
  };

  const navItems = [
    { name: 'Dashboard', path: '/', icon: LayoutDashboard },
    { name: 'Markets', path: '/markets', icon: Activity },
    { name: 'Stock Analysis', path: '/analysis', icon: LineChart },
    { name: 'Chart Workspace', path: '/chart', icon: ImageIcon },
    { name: 'AI Analyst', path: '/ai', icon: Beaker },
    { name: 'News', path: '/news', icon: FileText },
    { name: 'Forex', path: '/forex', icon: DollarSign },
    { name: 'Macro', path: '/macro', icon: Globe },
    { name: 'Screener', path: '/screener', icon: Filter },
    { name: 'Watchlist', path: '/watchlist', icon: Star },
    { name: 'Alerts', path: '/alerts', icon: Bell },
    { name: 'Portfolio', path: '/portfolio', icon: Briefcase },
    { name: 'Profile', path: '/profile', icon: User },
    { name: 'Settings', path: '/settings', icon: Settings },
    { name: 'Admin', path: '/admin', icon: Shield },
  ];

  return (
    <div className="min-h-screen flex bg-black-bg text-text-primary selection:bg-border-subtle selection:text-text-primary overflow-hidden">
      {/* Sidebar */}
      {sidebarOpen && (
      <aside className="w-64 bg-sidebar-bg border-r border-border-subtle hidden md:flex flex-col shrink-0 h-screen overflow-y-auto">
        <div className="h-16 flex items-center px-6 border-b border-border-subtle shrink-0">
          <Activity className="w-6 h-6 text-text-primary mr-2" />
          <span className="font-bold text-xl tracking-tight text-text-primary">EquiNexa AI</span>
        </div>
        <nav className="p-4 space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const active = location.pathname === item.path;
            return (
              <Link
                key={item.name}
                to={item.path}
                onClick={() => setMobileMenuOpen(false)}
                className={`flex items-center px-4 py-3 rounded-lg transition-colors ${
                  active 
                    ? 'bg-hover-bg text-text-primary font-medium' 
                    : 'text-text-secondary hover:bg-hover-bg hover:text-text-primary'
                }`}
              >
                <Icon className="w-5 h-5 mr-3" />
                {item.name}
              </Link>
            );
          })}
        </nav>
      </aside>
      )}

      {/* Mobile Sidebar Overlay */}
      {mobileMenuOpen && (
        <div className="fixed inset-0 z-40 flex md:hidden">
          <div className="fixed inset-0 bg-black-bg/80 backdrop-blur-sm" onClick={() => setMobileMenuOpen(false)}></div>
          <aside className="relative flex-1 flex flex-col max-w-xs w-full bg-sidebar-bg border-r border-border-subtle z-50 overflow-y-auto">
            <div className="h-16 flex items-center justify-between px-6 border-b border-border-subtle">
              <div className="flex items-center">
                <Activity className="w-6 h-6 text-text-primary mr-2" />
                <span className="font-bold text-xl tracking-tight text-text-primary">EquiNexa AI</span>
              </div>
              <button onClick={() => setMobileMenuOpen(false)} className="p-2 text-text-secondary hover:text-text-primary">
                <X className="w-6 h-6" />
              </button>
            </div>
            <nav className="p-4 space-y-1">
              {navItems.map((item) => {
                const Icon = item.icon;
                const active = location.pathname === item.path;
                return (
                  <Link
                    key={item.name}
                    to={item.path}
                    onClick={() => setMobileMenuOpen(false)}
                    className={`flex items-center px-4 py-3 rounded-lg transition-colors ${
                      active 
                        ? 'bg-hover-bg text-text-primary font-medium' 
                        : 'text-text-secondary hover:bg-hover-bg hover:text-text-primary'
                    }`}
                  >
                    <Icon className="w-5 h-5 mr-3" />
                    {item.name}
                  </Link>
                );
              })}
            </nav>
          </aside>
        </div>
      )}

      {/* Main Content */}
      <div className="flex-1 flex flex-col w-full h-screen overflow-hidden">
        <header className="h-16 bg-header-bg border-b border-border-subtle flex items-center justify-between px-4 md:px-6 shrink-0">
          <div className="flex items-center">
            {/* Mobile Toggle */}
            <button className="md:hidden p-2 mr-2 text-text-secondary hover:text-text-primary" onClick={() => setMobileMenuOpen(true)}>
              <Menu className="w-6 h-6" />
            </button>
            {/* Desktop Toggle */}
            <button className="hidden md:block p-2 mr-4 text-text-secondary hover:text-text-primary transition-colors" onClick={() => setSidebarOpen(!sidebarOpen)}>
              <Menu className="w-5 h-5" />
            </button>
            <div className="text-sm font-medium text-text-secondary hidden sm:block">Market Session: <span className="text-market-up">Open</span></div>
          </div>
          <div className="flex items-center space-x-2 md:space-x-4">
             {/* Global Search */}
             <div className="relative" ref={searchRef}>
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                   {searching ? (
                     <div className="w-4 h-4 border-2 border-text-muted border-t-transparent rounded-full animate-spin"></div>
                   ) : (
                     <Search className="w-4 h-4 text-text-muted" />
                   )}
                </div>
                <input 
                  type="text" 
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  onKeyDown={handleKeyDown}
                  onFocus={() => { if (searchResults.length > 0) setSearchOpen(true); }}
                  placeholder="Search ticker or company..." 
                  className="pl-10 pr-4 py-2 w-64 bg-card-bg border border-border-subtle rounded-md text-sm text-text-primary placeholder:text-text-muted focus:outline-none focus:ring-1 focus:ring-text-secondary transition-shadow"
                />
                
                {searchOpen && searchResults.length > 0 && (
                  <div className="absolute top-full left-0 mt-1 w-full bg-card-bg border border-border-subtle rounded-md shadow-lg max-h-96 overflow-y-auto z-50">
                    {searchResults.map((result) => (
                      <button
                        key={result.symbol}
                        onClick={() => handleSelectSymbol(result.symbol)}
                        className="w-full text-left px-4 py-3 border-b border-border-subtle hover:bg-hover-bg transition-colors last:border-b-0 flex flex-col"
                      >
                        <div className="flex justify-between items-start">
                          <span className="font-semibold text-text-primary">{result.symbol}</span>
                          <span className="text-xs text-text-muted bg-border-subtle px-1 rounded">{result.exchange}</span>
                        </div>
                        <span className="text-xs text-text-secondary truncate block mt-0.5">{result.name}</span>
                      </button>
                    ))}
                  </div>
                )}
             </div>
              <button onClick={() => navigate('/settings')} className="p-2 rounded-full hover:bg-hover-bg transition-colors" aria-label="Settings">
                <Settings className="w-5 h-5 text-text-secondary" />
              </button>
          </div>
        </header>
        <main className="flex-1 p-4 md:p-8 overflow-y-auto">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default AppLayout;
