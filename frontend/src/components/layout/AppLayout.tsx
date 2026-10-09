import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom';
import { Activity, LineChart, Beaker, Image as ImageIcon, Settings, Search, FileText, Globe, Filter, Star, Bell, ChevronDown, Home, User } from 'lucide-react';
import { useState, useEffect, useRef } from 'react';
import { searchMarkets, type SearchResult } from '../../services/api/markets';
import { supabase } from '../../lib/supabase';

const AppLayout = () => {
  const location = useLocation();
  const navigate = useNavigate();
  
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [searching, setSearching] = useState(false);
  const [searchOpen, setSearchOpen] = useState(false);
  const [toolsOpen, setToolsOpen] = useState(false);
  const [user, setUser] = useState<any>(null);
  
  const searchRef = useRef<HTMLDivElement>(null);
  const toolsRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user || null);
    });

    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user || null);
    });

    const handleClickOutside = (event: MouseEvent) => {
      if (searchRef.current && !searchRef.current.contains(event.target as Node)) {
        setSearchOpen(false);
      }
      if (toolsRef.current && !toolsRef.current.contains(event.target as Node)) {
        setToolsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      subscription.unsubscribe();
    };
  }, []);

  const getInitials = (userData: any) => {
    if (!userData) return '';
    const name = userData.user_metadata?.full_name || userData.email || '';
    if (!name) return 'U';
    return name.substring(0, 2).toUpperCase();
  };

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
    { name: 'Markets', path: '/markets', icon: Activity },
    { name: 'Stock Analysis', path: '/analysis', icon: LineChart },
    { name: 'AI Analyst', path: '/ai', icon: Beaker },
  ];

  const toolItems = [
    { name: 'Chart Workspace', path: '/chart', icon: ImageIcon },
    { name: 'Watchlist', path: '/watchlist', icon: Star },
    { name: 'Alerts', path: '/alerts', icon: Bell },
    { name: 'Screener', path: '/screener', icon: Filter },
    { name: 'News', path: '/news', icon: FileText },
    { name: 'Macro', path: '/macro', icon: Globe },
  ];

  return (
    <div className="min-h-screen flex flex-col bg-eq-bg text-eq-text overflow-hidden w-full min-w-0">
      {/* Top Header Navigation */}
      <header className="h-16 bg-header-bg border-b border-border-subtle flex items-center justify-between px-4 md:px-6 shrink-0 z-40">
        <div className="flex items-center space-x-4">
          <Link to="/" className="flex items-center hover:opacity-80 transition-opacity">
            <Activity className="w-6 h-6 text-eq-purple mr-2" />
            <span className="font-semibold text-xl tracking-tight text-eq-text hidden sm:block">EquiNexa AI</span>
          </Link>
          
          {/* Global Search */}
          <div className="relative ml-2 sm:ml-4" ref={searchRef}>
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
              placeholder="Search for Anything [Ctrl + S]" 
              className="pl-10 pr-4 py-2 w-48 sm:w-64 lg:w-80 bg-eq-surface-card border border-eq-border rounded text-sm text-eq-text placeholder:text-eq-text-muted focus:outline-none focus:ring-1 focus:ring-eq-purple transition-shadow"
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
        </div>

        {/* Center/Right Navigation Links */}
        <div className="flex items-center space-x-1 lg:space-x-6">
          <Link to="/" className={`hidden lg:flex p-2 transition-colors ${location.pathname === '/' ? 'text-eq-purple' : 'text-eq-text-secondary hover:text-eq-text'}`}>
            <Home className="w-5 h-5" />
          </Link>
          
          <nav className="hidden md:flex items-center space-x-6 h-full">
            {navItems.map((item) => {
              const active = location.pathname === item.path;
              return (
                <Link
                  key={item.name}
                  to={item.path}
                  className={`relative flex items-center h-16 text-sm font-medium transition-colors ${
                    active 
                      ? 'text-eq-purple' 
                      : 'text-eq-text-secondary hover:text-eq-text'
                  }`}
                >
                  {item.name}
                  {active && <span className="absolute bottom-0 left-0 w-full h-0.5 bg-eq-purple"></span>}
                </Link>
              );
            })}
            
            {/* Tools Dropdown */}
            <div className="relative flex items-center h-full" ref={toolsRef}>
              <button 
                onClick={() => setToolsOpen(!toolsOpen)}
                className={`flex items-center text-sm font-medium transition-colors h-16 ${
                  toolsOpen ? 'text-eq-text' : 'text-eq-text-secondary hover:text-eq-text'
                }`}
              >
                Tools <ChevronDown className="w-4 h-4 ml-1" />
              </button>
              
              {toolsOpen && (
                <div className="absolute top-14 right-0 mt-1 w-48 bg-eq-surface border border-eq-border rounded shadow-lg py-1 z-50">
                  {toolItems.map((item) => (
                    <Link
                      key={item.name}
                      to={item.path}
                      onClick={() => setToolsOpen(false)}
                      className="flex items-center px-4 py-2 text-sm text-eq-text-secondary hover:bg-eq-surface-elevated hover:text-eq-text transition-colors"
                    >
                      {item.name}
                    </Link>
                  ))}
                </div>
              )}
            </div>
          </nav>

          <div className="flex items-center space-x-2 pl-2 lg:pl-6 border-l border-eq-border ml-2 lg:ml-6">
            <button className="p-2 transition-colors text-eq-text-secondary hover:text-eq-text" aria-label="Notifications">
              <Bell className="w-5 h-5" />
            </button>
            <button onClick={() => navigate('/settings')} className="p-2 transition-colors text-eq-text-secondary hover:text-eq-text" aria-label="Settings">
              <Settings className="w-5 h-5" />
            </button>
            {user ? (
              <button onClick={() => navigate('/profile')} className="ml-2 w-8 h-8 rounded-full bg-eq-purple flex items-center justify-center text-[12px] font-semibold text-white hover:bg-eq-purple-hover transition-colors">
                {getInitials(user)}
              </button>
            ) : (
              <button onClick={() => navigate('/profile')} className="ml-2 p-2 transition-colors text-eq-text-secondary hover:text-eq-text" aria-label="Login">
                <User className="w-5 h-5" />
              </button>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto">
        <Outlet />
      </main>
    </div>
  );
};

export default AppLayout;
