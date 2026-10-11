import { useState, useEffect } from 'react';
import { Settings as SettingsIcon, Sun, Moon, LogOut, LogIn, Monitor, Shield } from 'lucide-react';
import { supabase } from '../lib/supabase';
import { useNavigate } from 'react-router-dom';
import { useTheme } from '../context/ThemeContext';

const Settings = () => {
  const { theme, toggleTheme } = useTheme();
  const [session, setSession] = useState<any>(null);
  const navigate = useNavigate();

  useEffect(() => {
    // Check Supabase session
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
    });

    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session);
    });

    return () => subscription.unsubscribe();
  }, []);

  const handleLogout = async () => {
    await supabase.auth.signOut();
  };

  return (
    <div className="flex flex-col h-full bg-eq-bg text-eq-text p-4 lg:p-6 max-w-4xl mx-auto w-full space-y-6">
      
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
          <div className="flex items-center justify-between p-4 bg-eq-surface-card border border-border-subtle rounded-lg">
            <div>
              <div className="font-medium text-text-primary">Theme Preference</div>
              <div className="text-sm text-text-muted" data-testid="active-theme">
                Active: <span className="font-semibold text-text-primary">{theme === 'dark' ? 'Dark Mode' : 'Light Mode'}</span>
              </div>
            </div>
            <button 
              onClick={toggleTheme}
              aria-label={theme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
              className="flex items-center px-4 py-2 bg-card-bg border border-border-subtle hover:bg-hover-bg rounded-md font-medium transition-colors cursor-pointer"
            >
              {theme === 'dark' ? (
                <><Sun className="w-4 h-4 mr-2 text-yellow-400" /> Switch to Light Mode</>
              ) : (
                <><Moon className="w-4 h-4 mr-2 text-eq-purple" /> Switch to Dark Mode</>
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
            <div className="flex items-center justify-between p-4 bg-eq-surface-card border border-border-subtle rounded-lg">
              <div>
                <div className="font-medium text-text-primary">Authentication Status</div>
                <div className="text-sm text-text-muted">
                  {session ? `Logged in as ${session.user.email || 'user@equinexa.ai'}` : 'Currently acting as a guest.'}
                </div>
              </div>
              
              {session ? (
                <button 
                  onClick={handleLogout}
                  className="flex items-center px-4 py-2 bg-red-900/20 text-red-400 border border-red-900/50 hover:bg-red-900/40 rounded-md font-medium transition-colors cursor-pointer"
                >
                  <LogOut className="w-4 h-4 mr-2" /> Sign Out
                </button>
              ) : (
                <button 
                  onClick={() => navigate('/profile')}
                  className="flex items-center px-4 py-2 bg-eq-purple hover:bg-eq-purple-hover text-white rounded-md font-medium transition-colors cursor-pointer"
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
