import { useState, useEffect } from 'react';
import { Mail, Phone, Lock, User, Shield, LogOut, ArrowRight, ShieldCheck, AlertCircle, CheckCircle2, RotateCw } from 'lucide-react';
import { supabase, isSupabaseConfigured } from '../lib/supabase';

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

  const formatAuthError = (err: any, context: 'email' | 'otp_send' | 'otp_verify'): string => {
    const raw = (err?.message || err?.error_description || String(err || '')).toLowerCase();
    
    if (raw.includes('failed to fetch') || raw.includes('networkerror') || raw.includes('fetch')) {
      return "Unable to connect to the authentication server. Please check your network connection or verify that the Supabase environment is reachable.";
    }

    if (context === 'email') {
      if (raw.includes('invalid login credentials') || raw.includes('invalid_credentials')) {
        return "Invalid email or password. Please verify your credentials and try again.";
      }
      if (raw.includes('email not confirmed')) {
        return "Email address has not been confirmed yet. Please verify your email inbox.";
      }
    }

    if (context === 'otp_send') {
      if (raw.includes('unsupported phone provider') || raw.includes('phone_provider_disabled') || raw.includes('sms provider')) {
        return "SMS/Phone authentication is currently disabled in this Supabase project. To enable it, configure an SMS provider in Supabase Dashboard (Authentication > Providers > Phone). In the meantime, please sign in with Email & Password.";
      }
      if (raw.includes('rate_limit') || raw.includes('too many') || raw.includes('security purposes')) {
        return "Too many SMS requests sent. Please wait a few minutes before requesting another verification code.";
      }
      if (raw.includes('invalid phone') || raw.includes('unsupported')) {
        return "Please enter a valid international phone number (e.g. +91 98765 43210).";
      }
    }

    if (context === 'otp_verify') {
      if (raw.includes('token has expired') || raw.includes('otp_expired')) {
        return "The verification code has expired. Please request a new code.";
      }
      if (raw.includes('invalid token') || raw.includes('invalid_grant') || raw.includes('token is invalid')) {
        return "Incorrect verification code. Please check the 6-digit code and try again.";
      }
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

    setLoading(true);

    try {
      if (authMethod === 'email') {
        const { error } = await supabase.auth.signInWithPassword({
          email: email.trim(),
          password,
        });

        if (error) {
          setErrorMsg(formatAuthError(error, 'email'));
        }
      } else {
        // Phone OTP Flow
        const cleanPhone = phone.replace(/[\s-]/g, '');

        if (!isOtpSent) {
          // Validation: Ensure valid phone format with country code
          if (!cleanPhone.startsWith('+') || cleanPhone.length < 8) {
            setErrorMsg("Please enter a valid phone number in international format starting with + (e.g. +91 98765 43210).");
            setLoading(false);
            return;
          }

          const { error } = await supabase.auth.signInWithOtp({
            phone: cleanPhone,
          });

          if (error) {
            setErrorMsg(formatAuthError(error, 'otp_send'));
          } else {
            setIsOtpSent(true);
            setSuccessMsg(`Verification code sent to ${cleanPhone}. Please enter the 6-digit code below.`);
          }
        } else {
          // OTP Verification Step
          const cleanOtp = otp.trim();
          if (cleanOtp.length < 6) {
            setErrorMsg("Please enter the complete 6-digit verification code.");
            setLoading(false);
            return;
          }

          const { error } = await supabase.auth.verifyOtp({
            phone: cleanPhone,
            token: cleanOtp,
            type: 'sms',
          });

          if (error) {
            setErrorMsg(formatAuthError(error, 'otp_verify'));
          } else {
            setOtp('');
          }
        }
      }
    } catch (err: any) {
      setErrorMsg(formatAuthError(err, authMethod === 'email' ? 'email' : (isOtpSent ? 'otp_verify' : 'otp_send')));
    } finally {
      setLoading(false);
    }
  };

  const handleResendOtp = async () => {
    setErrorMsg(null);
    setSuccessMsg(null);
    setLoading(true);

    try {
      const cleanPhone = phone.replace(/[\s-]/g, '');
      const { error } = await supabase.auth.signInWithOtp({ phone: cleanPhone });
      if (error) {
        setErrorMsg(formatAuthError(error, 'otp_send'));
      } else {
        setSuccessMsg(`New verification code sent to ${cleanPhone}.`);
      }
    } catch (err: any) {
      setErrorMsg(formatAuthError(err, 'otp_send'));
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = async () => {
    setErrorMsg(null);
    setSuccessMsg(null);
    await supabase.auth.signOut();
  };

  if (isAuthenticated) {
    return (
      <div className="flex flex-col h-full bg-black-bg text-text-primary p-6 max-w-4xl mx-auto w-full">
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
              <p className="text-sm text-text-muted mt-1">{session?.user?.email || session?.user?.phone || 'user@equinexa.ai'}</p>
              <div className="mt-4 px-3 py-1 bg-green-900/30 text-market-up border border-green-900/50 rounded-full text-xs font-medium flex items-center">
                <ShieldCheck className="w-3 h-3 mr-1" /> Account Verified
              </div>
            </div>
            
            <button 
              onClick={handleLogout}
              className="w-full py-2.5 bg-card-bg border border-border-subtle hover:bg-red-950/30 hover:border-red-900/50 hover:text-red-400 rounded-lg font-medium transition-colors flex items-center justify-center cursor-pointer"
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
    <div className="flex flex-col h-full bg-black-bg text-text-primary p-6 items-center justify-center">
      <div className="w-full max-w-md bg-card-bg border border-border-subtle rounded-xl p-8 shadow-2xl">
        <div className="text-center mb-8">
          <Shield className="w-12 h-12 text-eq-purple mx-auto mb-3" />
          <h1 className="text-2xl font-bold">Sign In to EquiNexa AI</h1>
          <p className="text-sm text-text-muted mt-2">Secure access powered by Supabase Auth</p>
        </div>

        {/* Tab Selection */}
        <div className="flex bg-black-bg p-1 rounded-lg mb-6 border border-border-subtle">
          <button 
            type="button"
            onClick={() => { setAuthMethod('email'); setIsOtpSent(false); setErrorMsg(null); setSuccessMsg(null); }}
            className={`flex-1 py-2 text-sm font-medium rounded-md transition-colors cursor-pointer ${authMethod === 'email' ? 'bg-card-bg text-text-primary shadow' : 'text-text-muted hover:text-text-primary'}`}
          >
            Email & Password
          </button>
          <button 
            type="button"
            onClick={() => { setAuthMethod('phone'); setIsOtpSent(false); setErrorMsg(null); setSuccessMsg(null); }}
            className={`flex-1 py-2 text-sm font-medium rounded-md transition-colors cursor-pointer ${authMethod === 'phone' ? 'bg-card-bg text-text-primary shadow' : 'text-text-muted hover:text-text-primary'}`}
          >
            Phone (OTP)
          </button>
        </div>

        {/* Inline Alerts */}
        {errorMsg && (
          <div className="mb-4 p-3 bg-red-950/30 border border-red-900/50 rounded-lg text-sm text-red-300 flex items-start gap-2.5">
            <AlertCircle className="w-4 h-4 text-red-400 mt-0.5 shrink-0" />
            <div className="flex-1 leading-snug">{errorMsg}</div>
          </div>
        )}

        {successMsg && (
          <div className="mb-4 p-3 bg-green-950/30 border border-green-900/50 rounded-lg text-sm text-green-300 flex items-start gap-2.5">
            <CheckCircle2 className="w-4 h-4 text-green-400 mt-0.5 shrink-0" />
            <div className="flex-1 leading-snug">{successMsg}</div>
          </div>
        )}

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
                    className="w-full pl-10 pr-4 py-2.5 bg-black-bg border border-border-subtle rounded-lg text-sm focus:outline-none focus:ring-1 focus:ring-eq-purple text-text-primary" 
                  />
                </div>
              </div>
              <div>
                <label className="text-xs font-semibold text-text-secondary block mb-1.5 flex justify-between">
                  Password
                  <span className="text-eq-purple hover:underline cursor-pointer">Forgot?</span>
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
                    className="w-full pl-10 pr-4 py-2.5 bg-black-bg border border-border-subtle rounded-lg text-sm focus:outline-none focus:ring-1 focus:ring-eq-purple text-text-primary" 
                  />
                </div>
              </div>
            </>
          ) : (
            <>
              <div>
                <div className="flex justify-between items-center mb-1.5">
                  <label className="text-xs font-semibold text-text-secondary">Phone Number</label>
                  {isOtpSent && (
                    <button
                      type="button"
                      onClick={() => { setIsOtpSent(false); setOtp(''); setErrorMsg(null); setSuccessMsg(null); }}
                      className="text-xs text-eq-purple hover:underline cursor-pointer"
                    >
                      Change Number
                    </button>
                  )}
                </div>
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
                    className="w-full pl-10 pr-4 py-2.5 bg-black-bg border border-border-subtle rounded-lg text-sm focus:outline-none focus:ring-1 focus:ring-eq-purple disabled:opacity-60 text-text-primary" 
                  />
                </div>
                {!isOtpSent && (
                  <span className="text-[11px] text-text-muted mt-1 block">Include country code (e.g., +91 for India, +1 for US).</span>
                )}
              </div>

              {isOtpSent && (
                <div>
                  <div className="flex justify-between items-center mb-1.5">
                    <label className="text-xs font-semibold text-text-secondary">One-Time Password (OTP)</label>
                    <button
                      type="button"
                      disabled={loading}
                      onClick={handleResendOtp}
                      className="text-xs text-eq-purple hover:underline flex items-center gap-1 cursor-pointer disabled:opacity-50"
                    >
                      <RotateCw className="w-3 h-3" /> Resend Code
                    </button>
                  </div>
                  <div className="relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <Lock className="w-4 h-4 text-text-muted" />
                    </div>
                    <input 
                      type="text" 
                      required 
                      maxLength={6}
                      autoFocus
                      placeholder="Enter 6-digit OTP" 
                      value={otp}
                      onChange={(e) => setOtp(e.target.value.replace(/\D/g, ''))}
                      className="w-full pl-10 pr-4 py-2.5 bg-black-bg border border-border-subtle rounded-lg text-sm tracking-widest focus:outline-none focus:ring-1 focus:ring-eq-purple text-text-primary font-mono text-center" 
                    />
                  </div>
                </div>
              )}
            </>
          )}

          <button 
            type="submit" 
            disabled={loading}
            className="w-full py-2.5 mt-2 bg-eq-purple hover:bg-eq-purple-hover text-white rounded-lg font-semibold transition-colors flex items-center justify-center disabled:opacity-60 cursor-pointer"
          >
            {loading ? (
              <span className="flex items-center gap-2">
                <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                {authMethod === 'email' ? 'Signing In...' : (!isOtpSent ? 'Sending OTP...' : 'Verifying OTP...')}
              </span>
            ) : (
              <span className="flex items-center">
                {authMethod === 'phone' && !isOtpSent ? 'Send OTP' : (authMethod === 'phone' && isOtpSent ? 'Verify & Sign In' : 'Sign In')}
                <ArrowRight className="w-4 h-4 ml-2" />
              </span>
            )}
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
