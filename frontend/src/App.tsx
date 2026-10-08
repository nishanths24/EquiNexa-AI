import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import AppLayout from './components/layout/AppLayout';

// Pages
import Dashboard from './pages/Dashboard';
import Markets from './pages/Markets';
import StockAnalysis from './pages/StockAnalysis';
import ChartWorkspace from './pages/ChartWorkspace';
import AIAnalyst from './pages/AIAnalyst';
import News from './pages/News';
import Forex from './pages/Forex';
import Macro from './pages/Macro';
import Screener from './pages/Screener';
import Watchlist from './pages/Watchlist';
import Alerts from './pages/Alerts';
import Portfolio from './pages/Portfolio';
import Profile from './pages/Profile';
import Settings from './pages/Settings';
import Admin from './pages/Admin';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<AppLayout />}>
          <Route index element={<Dashboard />} />
          <Route path="markets" element={<Markets />} />
          <Route path="analysis" element={<StockAnalysis />} />
          <Route path="chart" element={<ChartWorkspace />} />
          <Route path="ai" element={<AIAnalyst />} />
          <Route path="news" element={<News />} />
          <Route path="forex" element={<Forex />} />
          <Route path="macro" element={<Macro />} />
          <Route path="screener" element={<Screener />} />
          <Route path="watchlist" element={<Watchlist />} />
          <Route path="alerts" element={<Alerts />} />
          <Route path="portfolio" element={<Portfolio />} />
          <Route path="profile" element={<Profile />} />
          <Route path="settings" element={<Settings />} />
          <Route path="admin" element={<Admin />} />
          
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
