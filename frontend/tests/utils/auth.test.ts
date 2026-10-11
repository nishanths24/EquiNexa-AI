/**
 * @vitest-environment jsdom
 */
import { describe, it, expect } from 'vitest';

describe('Auth Error Formatting and Logic', () => {
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

  it('formats invalid login credentials into helpful user message', () => {
    const result = formatAuthError({ message: 'Invalid login credentials' }, 'email');
    expect(result).toBe('Invalid email or password. Please verify your credentials and try again.');
  });

  it('formats phone provider disabled into actionable Supabase guidance', () => {
    const result = formatAuthError({ message: 'Unsupported phone provider' }, 'otp_send');
    expect(result).toContain('SMS/Phone authentication is currently disabled');
    expect(result).toContain('Supabase Dashboard');
  });

  it('formats expired token error into clear message', () => {
    const result = formatAuthError({ message: 'Token has expired' }, 'otp_verify');
    expect(result).toBe('The verification code has expired. Please request a new code.');
  });

  it('formats network failure gracefully', () => {
    const result = formatAuthError(new TypeError('Failed to fetch'), 'email');
    expect(result).toContain('Unable to connect to the authentication server');
  });
});
