/**
 * @vitest-environment jsdom
 */
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { render, screen, fireEvent, waitFor, cleanup } from '@testing-library/react';
import Profile from '../../src/pages/Profile';
import { supabase } from '../../src/lib/supabase';

describe('Profile Email Authentication Component Test', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
    window.alert = vi.fn();
  });

  afterEach(() => {
    cleanup();
  });

  it('verifies that Phone OTP UI is completely removed and Email/Password is the only login method', () => {
    render(<Profile />);

    // Email & Password elements must be present
    expect(screen.getByText('Sign In to EquiNexa AI')).toBeDefined();
    expect(screen.getByText('Email Address')).toBeDefined();
    expect(screen.getByText('Password')).toBeDefined();
    expect(screen.getByRole('button', { name: /Sign In/i })).toBeDefined();

    // Verify Phone OTP UI is completely absent
    expect(screen.queryByText(/Phone \(OTP\)/i)).toBeNull();
    expect(screen.queryByPlaceholderText('+91 98765 43210')).toBeNull();
    expect(screen.queryByText(/Send OTP/i)).toBeNull();
    expect(screen.queryByText(/One-Time Password/i)).toBeNull();
  });

  it('submits email and password to Supabase client and displays inline error without window.alert on failure', async () => {
    const signInSpy = vi.spyOn(supabase.auth, 'signInWithPassword').mockResolvedValueOnce({
      data: { user: null, session: null },
      error: { message: 'Invalid login credentials', name: 'AuthApiError', status: 400 },
    } as any);

    render(<Profile />);

    const emailInput = screen.getByPlaceholderText('name@company.com');
    const passwordInput = screen.getByPlaceholderText('••••••••');
    const submitBtn = screen.getByRole('button', { name: /Sign In/i });

    fireEvent.change(emailInput, { target: { value: 'trader@equinexa.ai' } });
    fireEvent.change(passwordInput, { target: { value: 'wrongpassword' } });
    fireEvent.click(submitBtn);

    expect(signInSpy).toHaveBeenCalledWith({
      email: 'trader@equinexa.ai',
      password: 'wrongpassword',
    });

    await waitFor(() => {
      const alert = screen.getByRole('alert');
      expect(alert.textContent).toContain('Invalid email or password');
    });

    // Verify window.alert was never called
    expect(window.alert).not.toHaveBeenCalled();
  });

  it('displays inline network connection error gracefully when request fails to fetch', async () => {
    vi.spyOn(supabase.auth, 'signInWithPassword').mockRejectedValueOnce(new TypeError('Failed to fetch'));

    render(<Profile />);

    const emailInput = screen.getByPlaceholderText('name@company.com');
    const passwordInput = screen.getByPlaceholderText('••••••••');
    const submitBtn = screen.getByRole('button', { name: /Sign In/i });

    fireEvent.change(emailInput, { target: { value: 'trader@equinexa.ai' } });
    fireEvent.change(passwordInput, { target: { value: 'secret123' } });
    fireEvent.click(submitBtn);

    await waitFor(() => {
      const alert = screen.getByRole('alert');
      expect(alert.textContent).toContain('Unable to connect to the authentication server');
    });

    expect(window.alert).not.toHaveBeenCalled();
  });
});
