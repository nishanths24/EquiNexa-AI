
import { Outlet, Link, useLocation } from 'react-router-dom';
import { Activity, LayoutDashboard, LineChart, Beaker } from 'lucide-react';

const AppLayout = () => {
  const location = useLocation();

  const navItems = [
    { name: 'Overview', path: '/', icon: LayoutDashboard },
    { name: 'Stock Analysis', path: '/analysis', icon: LineChart },
    { name: 'Research & Experiments', path: '/research', icon: Beaker },
  ];

  return (
    <div className="min-h-screen flex bg-neutral-50 text-neutral-900">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-neutral-200 hidden md:block">
        <div className="h-16 flex items-center px-6 border-b border-neutral-200">
          <Activity className="w-6 h-6 text-brand-600 mr-2" />
          <span className="font-bold text-xl tracking-tight">EquiNexa AI</span>
        </div>
        <nav className="p-4 space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const active = location.pathname === item.path;
            return (
              <Link
                key={item.name}
                to={item.path}
                className={`flex items-center px-4 py-3 rounded-lg transition-colors ${
                  active 
                    ? 'bg-brand-50 text-brand-600 font-medium' 
                    : 'text-neutral-600 hover:bg-neutral-50'
                }`}
              >
                <Icon className="w-5 h-5 mr-3" />
                {item.name}
              </Link>
            );
          })}
        </nav>
      </aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        <header className="h-16 bg-white border-b border-neutral-200 flex items-center justify-between px-8">
          <div className="text-sm font-medium text-neutral-500">Market Session: <span className="text-green-600">Open</span></div>
          <div className="flex items-center space-x-4">
             {/* Global Search Placeholder */}
             <div className="relative">
                <input 
                  type="text" 
                  placeholder="Search ticker..." 
                  className="pl-4 pr-10 py-2 border border-neutral-200 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
                />
             </div>
          </div>
        </header>
        <main className="flex-1 p-8 overflow-auto">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default AppLayout;
