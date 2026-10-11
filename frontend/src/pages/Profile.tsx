import { useState, useEffect } from 'react';
import { Mail, Lock, User, Shield, LogOut, ArrowRight, ShieldCheck, AlertCircle, CheckCircle2 } from 'lucide-react';
import { supabase, isSupabaseConfigured } from '../lib/supabase';

const Profile = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [authMode, setAuthMode] = useState<'signin' | 'signup' | 'reset'>('signin');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [session, setSession] = useState<any>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

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

  const formatAuthError = (err: any): string => {
    const raw = (err?.message || err?.error_description || String(err || '')).toLowerCase();
    
    if (raw.includes('failed to fetch') || raw.includes('networkerror') || raw.includes('fetch')) {
      return "Unable to connect to the authentication server. Please check your network connection or verify that the Supabase environment is reachable.";
    }

    if (raw.includes('invalid login credentials') || raw.includes('invalid_credentials')) {
      return "Invalid email or password. Please verify your credentials and try again.";
    }

    if (raw.includes('email not confirmed')) {
      return "Email address has not been confirmed yet. Please verify your email inbox.";
    }

    if (raw.includes('user already registered') || raw.includes('already exists')) {
      return "An account with this email address already exists. Please sign in instead.";
    }

    if (raw.includes('password should be at least')) {
      return "Password must be at least 6 characters long.";
    }

    return err?.message || "An authentication error occurred. Please try again.";
  };

  const handleAuthSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg(null);
    setSuccessMsg(null);

    if (!isSupabaseConfigured) {
      setErrorMsg("Authentication service configuration is missing. Please ensure VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY are set in your environment variables.");
      return;
    }

    if (!email.trim()) {
      setErrorMsg("Please enter a valid email address.");
      return;
    }

    setLoading(true);

    try {
      if (authMode === 'reset') {
        const { error } = await supabase.auth.resetPasswordForEmail(email.trim(), {
          redirectTo: window.location.origin + '/profile',
        });
        if (error) {
          setErrorMsg(formatAuthError(error));
        } else {
          setSuccessMsg(`Password reset instructions have been sent to ${email.trim()}. Please check your inbox.`);
        }
      } else if (authMode === 'signup') {
        if (!password || password.length < 6) {
          setErrorMsg("Password must be at least 6 characters long.");
          setLoading(false);
          return;
        }
        const { error, data } = await supabase.auth.signUp({
          email: email.trim(),
          password,
        });
        if (error) {
          setErrorMsg(formatAuthError(error));
        } else if (data.session) {
          setSuccessMsg("Account created successfully!");
        } else {
          setSuccessMsg("Account created! Please check your email inbox to confirm your address before signing in.");
        }
      } else {
        // Sign In with email and password
        const { error } = await supabase.auth.signInWithPassword({
          email: email.trim(),
          password,
        });

        if (error) {
          setErrorMsg(formatAuthError(error));
        }
      }
    } catch (err: any) {
      setErrorMsg(formatAuthError(err));
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = async () => {
    setErrorMsg(null);
    setSuccessMsg(null);
    setLoading(true);
    try {
      await supabase.auth.signOut();
    } finally {
      setLoading(false);
    }
  };

  if (isAuthenticated) {
    return (
      <div className="flex flex-col h-full bg-eq-bg text-eq-text p-6 max-w-4xl mx-auto w-full">
        <h1 className="text-2xl font-bold mb-6 flex items-center">
          <User className="w-6 h-6 mr-2 text-eq-purple" /> User Profile
        </h1>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="md:col-span-1 space-y-6">
            <div className="bg-card-bg border border-border-subtle rounded-lg p-6 flex flex-col items-center text-center">
              <div className="w-24 h-24 bg-eq-purple/10 rounded-full flex items-center justify-center border-2 border-eq-purple/30 mb-4">
                <User className="w-10 h-10 text-eq-purple" />
              </div>
              <h2 className="font-bold text-lg">Platform Trader</h2>
              <p className="text-sm text-text-muted mt-1">{session?.user?.email || 'user@equinexa.ai'}</p>
              <div className="mt-4 px-3 py-1 bg-green-900/30 text-market-up border border-green-900/50 rounded-full text-xs font-medium flex items-center">
                <ShieldCheck className="w-3 h-3 mr-1" /> Account Verified
              </div>
            </div>
            
            <button 
              onClick={handleLogout}
              disabled={loading}
              className="w-full py-2.5 bg-card-bg border border-border-subtle hover:bg-red-950/30 hover:border-red-900/50 hover:text-red-400 rounded-lg font-medium transition-colors flex items-center justify-center cursor-pointer disabled:opacity-60"
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
                  <div className="p-2.5 bg-eq-surface-card border border-border-subtle rounded font-mono text-sm text-text-secondary cursor-not-allowed">
                    {session?.user?.email || 'N/A'}
                  </div>
                </div>
                <div>
                  <label className="text-xs text-text-muted block mb-1">Database & Auth Provider</label>
                  <div className="p-2.5 bg-eq-surface-card border border-border-subtle rounded font-mono text-sm text-text-secondary cursor-not-allowed flex items-center">
                    <Shield className="w-4 h-4 mr-2 text-eq-purple" />
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
    <div className="flex flex-col h-full bg-eq-bg text-eq-text p-6 items-center justify-center">
      <div className="w-full max-w-md bg-card-bg border border-border-subtle rounded-xl p-8 shadow-2xl">
        <div className="text-center mb-6">
          <Shield className="w-12 h-12 text-eq-purple mx-auto mb-3" />
          <h1 className="text-2xl font-bold">
            {authMode === 'reset' ? 'Reset Password' : (authMode === 'signup' ? 'Create an Account' : 'Sign In to EquiNexa AI')}
          </h1>
          <p className="text-sm text-text-muted mt-2">
            {authMode === 'reset' 
              ? 'Enter your registered email to receive reset instructions' 
              : 'Secure email & password authentication powered by Supabase'}
          </p>
        </div>

        {/* Inline Alerts */}
        {errorMsg && (
          <div role="alert" className="mb-4 p-3 bg-red-950/30 border border-red-900/50 rounded-lg text-sm text-red-300 flex items-start gap-2.5">
            <AlertCircle className="w-4 h-4 text-red-400 mt-0.5 shrink-0" />
            <div className="flex-1 leading-snug">{errorMsg}</div>
          </div>
        )}

        {successMsg && (
          <div role="status" className="mb-4 p-3 bg-green-950/30 border border-green-900/50 rounded-lg text-sm text-green-300 flex items-start gap-2.5">
            <CheckCircle2 className="w-4 h-4 text-green-400 mt-0.5 shrink-0" />
            <div className="flex-1 leading-snug">{successMsg}</div>
          </div>
        )}

        <form onSubmit={handleAuthSubmit} className="space-y-4">
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
                className="w-full pl-10 pr-4 py-2.5 bg-eq-surface-card border border-border-subtle rounded-lg text-sm focus:outline-none focus:ring-1 focus:ring-eq-purple text-text-primary" 
              />
            </div>
          </div>

          {authMode !== 'reset' && (
            <div>
              <label className="text-xs font-semibold text-text-secondary block mb-1.5 flex justify-between">
                <span>Password</span>
                {authMode === 'signin' && (
                  <button
                    type="button"
                    onClick={() => { setAuthMode('reset'); setErrorMsg(null); setSuccessMsg(null); }}
                    className="text-eq-purple hover:underline cursor-pointer text-xs"
                  >
                    Forgot?
                  </button>
                )}
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
                  className="w-full pl-10 pr-4 py-2.5 bg-eq-surface-card border border-border-subtle rounded-lg text-sm focus:outline-none focus:ring-1 focus:ring-eq-purple text-text-primary" 
                />
              </div>
            </div>
          )}

          <button 
            type="submit" 
            disabled={loading}
            className="w-full py-2.5 mt-2 bg-eq-purple hover:bg-eq-purple-hover text-white rounded-lg font-semibold transition-colors flex items-center justify-center disabled:opacity-60 cursor-pointer"
          >
            {loading ? (
              <span className="flex items-center gap-2">
                <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                {authMode === 'reset' ? 'Sending Instructions...' : (authMode === 'signup' ? 'Creating Account...' : 'Signing In...')}
              </span>
            ) : (
              <span className="flex items-center">
                {authMode === 'reset' ? 'Send Reset Link' : (authMode === 'signup' ? 'Create Account' : 'Sign In')}
                <ArrowRight className="w-4 h-4 ml-2" />
              </span>
            )}
          </button>
        </form>

        {/* Mode Switching */}
        <div className="mt-5 text-center text-xs text-text-muted space-y-2">
          {authMode === 'signin' ? (
            <p>
              Don't have an account?{' '}
              <button 
                type="button" 
                onClick={() => { setAuthMode('signup'); setErrorMsg(null); setSuccessMsg(null); }}
                className="text-eq-purple hover:underline font-semibold cursor-pointer"
              >
                Sign up
              </button>
            </p>
          ) : (
            <p>
              Already have an account?{' '}
              <button 
                type="button" 
                onClick={() => { setAuthMode('signin'); setErrorMsg(null); setSuccessMsg(null); }}
                className="text-eq-purple hover:underline font-semibold cursor-pointer"
              >
                Sign in
              </button>
            </p>
          )}

          <p className="pt-2 text-[11px] text-text-muted">
            By accessing EquiNexa AI, you agree to our Terms of Service and Privacy Policy.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Profile;
