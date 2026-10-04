
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import AppLayout from './components/layout/AppLayout';
import Overview from './pages/Overview';
import Research from './pages/Research';
import StockAnalysis from './pages/StockAnalysis';
import ChartVision from './pages/ChartVision';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<AppLayout />}>
          <Route index element={<Overview />} />
          <Route path="analysis" element={<StockAnalysis />} />
          <Route path="vision" element={<ChartVision />} />
          <Route path="research" element={<Research />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
