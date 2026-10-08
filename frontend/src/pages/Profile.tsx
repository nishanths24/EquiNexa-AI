import { useState, useEffect } from 'react';
import { Mail, Phone, Lock, User, Shield, LogOut, ArrowRight, ShieldCheck } from 'lucide-react';
import { supabase } from '../lib/supabase';

const Profile = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [authMethod, setAuthMethod] = useState<'email' | 'phone'>('email');
  const [isOtpSent, setIsOtpSent] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [phone, setPhone] = useState('');
  const [otp, setOtp] = useState('');
  const [loading, setLoading] = useState(false);
  const [session, setSession] = useState<any>(null);

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
      setIsAuthenticated(!!session);
    });

    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session);
      setIsAuthenticated(!!session);
    });

    return () => subscription.unsubscribe();
  }, []);

  const handleAuthSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    if (authMethod === 'email') {
      const { error } = await supabase.auth.signInWithPassword({ email, password });
      if (error) alert(error.message);
    } else {
      if (!isOtpSent) {
        const { error } = await supabase.auth.signInWithOtp({ phone });
        if (error) alert(error.message);
        else setIsOtpSent(true);
      } else {
        const { error } = await supabase.auth.verifyOtp({ phone, token: otp, type: 'sms' });
        if (error) alert(error.message);
      }
    }
    setLoading(false);
  };

  const handleLogout = async () => {
    await supabase.auth.signOut();
  };

  if (isAuthenticated) {
    return (
      <div className="flex flex-col h-full bg-black-bg text-text-primary p-6 max-w-4xl mx-auto w-full">
        <h1 className="text-2xl font-bold mb-6 flex items-center">
          <User className="w-6 h-6 mr-2 text-blue-500" /> User Profile
        </h1>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="md:col-span-1 space-y-6">
            <div className="bg-card-bg border border-border-subtle rounded-lg p-6 flex flex-col items-center text-center">
              <div className="w-24 h-24 bg-blue-900/30 rounded-full flex items-center justify-center border-2 border-blue-500/50 mb-4">
                <User className="w-10 h-10 text-blue-500" />
              </div>
              <h2 className="font-bold text-lg">Platform Trader</h2>
              <p className="text-sm text-text-muted mt-1">{session?.user?.email || session?.user?.phone || 'user@equinexa.ai'}</p>
              <div className="mt-4 px-3 py-1 bg-green-900/30 text-market-up border border-green-900/50 rounded-full text-xs font-medium flex items-center">
                <ShieldCheck className="w-3 h-3 mr-1" /> Account Verified
              </div>
            </div>
            
            <button 
              onClick={handleLogout}
              className="w-full py-2.5 bg-card-bg border border-border-subtle hover:bg-red-950/30 hover:border-red-900/50 hover:text-red-400 rounded-lg font-medium transition-colors flex items-center justify-center"
            >
              <LogOut className="w-4 h-4 mr-2" /> Sign Out
            </button>
          </div>

          <div className="md:col-span-2 space-y-6">
            <div className="bg-card-bg border border-border-subtle rounded-lg p-6">
              <h3 className="text-sm font-semibold text-text-secondary uppercase tracking-wider mb-4 border-b border-border-subtle pb-2">
                Account Settings
              </h3>
              <div className="space-y-4">
                <div>
                  <label className="text-xs text-text-muted block mb-1">Email Address</label>
                  <div className="p-2.5 bg-black-bg border border-border-subtle rounded font-mono text-sm text-text-secondary cursor-not-allowed">
                    {session?.user?.email || 'N/A'}
                  </div>
                </div>
                <div>
                  <label className="text-xs text-text-muted block mb-1">Phone Number</label>
                  <div className="p-2.5 bg-black-bg border border-border-subtle rounded font-mono text-sm text-text-secondary cursor-not-allowed">
                    {session?.user?.phone || 'N/A'}
                  </div>
                </div>
                <div>
                  <label className="text-xs text-text-muted block mb-1">Database Provider</label>
                  <div className="p-2.5 bg-black-bg border border-border-subtle rounded font-mono text-sm text-text-secondary cursor-not-allowed flex items-center">
                    <Shield className="w-4 h-4 mr-2 text-blue-500" />
                    Supabase PostgreSQL (Connected)
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full bg-black-bg text-text-primary p-6 items-center justify-center">
      <div className="w-full max-w-md bg-card-bg border border-border-subtle rounded-xl p-8 shadow-2xl">
        <div className="text-center mb-8">
          <Shield className="w-12 h-12 text-blue-500 mx-auto mb-3" />
          <h1 className="text-2xl font-bold">Sign In to EquiNexa AI</h1>
          <p className="text-sm text-text-muted mt-2">Secure access powered by Supabase Auth</p>
        </div>

        <div className="flex bg-black-bg p-1 rounded-lg mb-6 border border-border-subtle">
          <button 
            type="button"
            onClick={() => { setAuthMethod('email'); setIsOtpSent(false); }}
            className={`flex-1 py-2 text-sm font-medium rounded-md transition-colors ${authMethod === 'email' ? 'bg-card-bg text-text-primary shadow' : 'text-text-muted hover:text-text-primary'}`}
          >
            Email & Password
          </button>
          <button 
            type="button"
            onClick={() => { setAuthMethod('phone'); setIsOtpSent(false); }}
            className={`flex-1 py-2 text-sm font-medium rounded-md transition-colors ${authMethod === 'phone' ? 'bg-card-bg text-text-primary shadow' : 'text-text-muted hover:text-text-primary'}`}
          >
            Phone (OTP)
          </button>
        </div>

        <form onSubmit={handleAuthSubmit} className="space-y-4">
          {authMethod === 'email' ? (
            <>
              <div>
                <label className="text-xs font-semibold text-text-secondary block mb-1.5">Email Address</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Mail className="w-4 h-4 text-text-muted" />
                  </div>
                  <input 
                    type="email" 
                    required 
                    placeholder="name@company.com" 
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full pl-10 pr-4 py-2.5 bg-black-bg border border-border-subtle rounded-lg text-sm focus:outline-none focus:ring-1 focus:ring-blue-500" 
                  />
                </div>
              </div>
              <div>
                <label className="text-xs font-semibold text-text-secondary block mb-1.5 flex justify-between">
                  Password
                  <span className="text-blue-500 hover:underline cursor-pointer">Forgot?</span>
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Lock className="w-4 h-4 text-text-muted" />
                  </div>
                  <input 
                    type="password" 
                    required 
                    placeholder="••••••••" 
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full pl-10 pr-4 py-2.5 bg-black-bg border border-border-subtle rounded-lg text-sm focus:outline-none focus:ring-1 focus:ring-blue-500" 
                  />
                </div>
              </div>
            </>
          ) : (
            <>
              <div>
                <label className="text-xs font-semibold text-text-secondary block mb-1.5">Phone Number</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Phone className="w-4 h-4 text-text-muted" />
                  </div>
                  <input 
                    type="tel" 
                    disabled={isOtpSent} 
                    required 
                    placeholder="+91 98765 43210" 
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
                    className="w-full pl-10 pr-4 py-2.5 bg-black-bg border border-border-subtle rounded-lg text-sm focus:outline-none focus:ring-1 focus:ring-blue-500 disabled:opacity-50" 
                  />
                </div>
              </div>
              {isOtpSent && (
                <div>
                  <label className="text-xs font-semibold text-text-secondary block mb-1.5">One-Time Password (OTP)</label>
                  <div className="relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <Lock className="w-4 h-4 text-text-muted" />
                    </div>
                    <input 
                      type="text" 
                      required 
                      placeholder="Enter 6-digit OTP" 
                      value={otp}
                      onChange={(e) => setOtp(e.target.value)}
                      className="w-full pl-10 pr-4 py-2.5 bg-black-bg border border-border-subtle rounded-lg text-sm tracking-widest focus:outline-none focus:ring-1 focus:ring-blue-500" 
                    />
                  </div>
                </div>
              )}
            </>
          )}

          <button 
            type="submit" 
            disabled={loading}
            className="w-full py-2.5 mt-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold transition-colors flex items-center justify-center disabled:opacity-50"
          >
            {loading ? 'Processing...' : (authMethod === 'phone' && !isOtpSent ? 'Send OTP' : 'Sign In')} <ArrowRight className="w-4 h-4 ml-2" />
          </button>
        </form>
        
        <p className="text-xs text-text-muted text-center mt-6">
          By signing in, you agree to our Terms of Service and Privacy Policy.
        </p>
      </div>
    </div>
  );
};

export default Profile;
