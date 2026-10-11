/**
 * @vitest-environment jsdom
 */
import { describe, it, expect } from 'vitest';

describe('Auth Error Formatting and Logic', () => {
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

  it('formats invalid login credentials into helpful user message', () => {
    const result = formatAuthError({ message: 'Invalid login credentials' });
    expect(result).toBe('Invalid email or password. Please verify your credentials and try again.');
  });

  it('formats unconfirmed email into actionable user guidance', () => {
    const result = formatAuthError({ message: 'Email not confirmed' });
    expect(result).toBe('Email address has not been confirmed yet. Please verify your email inbox.');
  });

  it('formats network connection failure gracefully', () => {
    const result = formatAuthError(new TypeError('Failed to fetch'));
    expect(result).toContain('Unable to connect to the authentication server');
  });

  it('formats duplicate user signup error into clear message', () => {
    const result = formatAuthError({ message: 'User already registered' });
    expect(result).toContain('An account with this email address already exists');
  });
});
