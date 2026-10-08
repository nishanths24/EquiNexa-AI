import { useState, useEffect } from 'react';
import { Settings as SettingsIcon, Sun, Moon, LogOut, LogIn, Monitor, Shield } from 'lucide-react';
import { supabase } from '../lib/supabase';
import { useNavigate } from 'react-router-dom';

const Settings = () => {
  const [theme, setTheme] = useState<'dark' | 'light'>('dark');
  const [session, setSession] = useState<any>(null);
  const navigate = useNavigate();

  useEffect(() => {
    // Check initial theme
    const isLight = document.documentElement.classList.contains('light-theme');
    setTheme(isLight ? 'light' : 'dark');

    // Check Supabase session
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
    });

    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session);
    });

    return () => subscription.unsubscribe();
  }, []);

  const toggleTheme = () => {
    const newTheme = theme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
    if (newTheme === 'light') {
      document.documentElement.classList.add('light-theme');
      localStorage.setItem('theme', 'light');
    } else {
      document.documentElement.classList.remove('light-theme');
      localStorage.setItem('theme', 'dark');
    }
  };

  const handleLogout = async () => {
    await supabase.auth.signOut();
  };

  return (
    <div className="flex flex-col h-full bg-black-bg text-text-primary p-4 lg:p-6 max-w-4xl mx-auto w-full space-y-6">
      
      {/* Header */}
      <div className="flex items-center border-b border-border-subtle pb-4">
        <SettingsIcon className="w-6 h-6 mr-3 text-blue-500" />
        <h1 className="text-2xl font-bold">Platform Settings</h1>
      </div>

      <div className="space-y-6">
        
        {/* Appearance Settings */}
        <div className="bg-card-bg border border-border-subtle rounded-lg p-5">
          <h2 className="text-lg font-semibold mb-4 flex items-center">
            <Monitor className="w-5 h-5 mr-2 text-text-muted" /> Appearance
          </h2>
          <div className="flex items-center justify-between p-4 bg-black-bg border border-border-subtle rounded-lg">
            <div>
              <div className="font-medium text-text-primary">Theme Preference</div>
              <div className="text-sm text-text-muted">Toggle between Dark and Light mode.</div>
            </div>
            <button 
              onClick={toggleTheme}
              className="flex items-center px-4 py-2 bg-card-bg border border-border-subtle hover:bg-hover-bg rounded-md font-medium transition-colors"
            >
              {theme === 'dark' ? (
                <><Sun className="w-4 h-4 mr-2" /> Light Mode</>
              ) : (
                <><Moon className="w-4 h-4 mr-2" /> Dark Mode</>
              )}
            </button>
          </div>
        </div>

        {/* Account & Security Settings */}
        <div className="bg-card-bg border border-border-subtle rounded-lg p-5">
          <h2 className="text-lg font-semibold mb-4 flex items-center">
            <Shield className="w-5 h-5 mr-2 text-text-muted" /> Account & Security
          </h2>
          
          <div className="flex flex-col space-y-4">
            <div className="flex items-center justify-between p-4 bg-black-bg border border-border-subtle rounded-lg">
              <div>
                <div className="font-medium text-text-primary">Authentication Status</div>
                <div className="text-sm text-text-muted">
                  {session ? `Logged in as ${session.user.email || session.user.phone}` : 'Currently acting as a guest.'}
                </div>
              </div>
              
              {session ? (
                <button 
                  onClick={handleLogout}
                  className="flex items-center px-4 py-2 bg-red-900/20 text-red-400 border border-red-900/50 hover:bg-red-900/40 rounded-md font-medium transition-colors"
                >
                  <LogOut className="w-4 h-4 mr-2" /> Sign Out
                </button>
              ) : (
                <button 
                  onClick={() => navigate('/profile')}
                  className="flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-md font-medium transition-colors"
                >
                  <LogIn className="w-4 h-4 mr-2" /> Sign In
                </button>
              )}
            </div>
          </div>
        </div>
        
      </div>
    </div>
  );
};

export default Settings;
