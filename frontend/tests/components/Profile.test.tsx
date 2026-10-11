/**
 * @vitest-environment jsdom
 */
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { render, screen, fireEvent, waitFor, cleanup } from '@testing-library/react';
import Profile from '../../src/pages/Profile';

describe('Profile Authentication Component Test', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
    window.alert = vi.fn();
  });

  afterEach(() => {
    cleanup();
  });

  it('renders sign in options and switches between Email and Phone tabs', () => {
    render(<Profile />);

    expect(screen.getByText('Sign In to EquiNexa AI')).toBeDefined();
    expect(screen.getByText('Email Address')).toBeDefined();
    expect(screen.getByText('Password')).toBeDefined();

    // Switch to Phone tab
    const phoneTab = screen.getByRole('button', { name: /Phone \(OTP\)/i });
    fireEvent.click(phoneTab);

    expect(screen.getByText('Phone Number')).toBeDefined();
    expect(screen.getByText(/Include country code/i)).toBeDefined();
    expect(screen.getByRole('button', { name: /Send OTP/i })).toBeDefined();
  });

  it('displays inline error and does not call window.alert on invalid phone number', async () => {
    render(<Profile />);

    // Switch to Phone tab
    fireEvent.click(screen.getByRole('button', { name: /Phone \(OTP\)/i }));

    const phoneInput = screen.getByPlaceholderText('+91 98765 43210');
    fireEvent.change(phoneInput, { target: { value: '123' } });

    const submitBtn = screen.getByRole('button', { name: /Send OTP/i });
    fireEvent.click(submitBtn);

    await waitFor(() => {
      expect(screen.getByText(/Please enter a valid phone number in international format/i)).toBeDefined();
    });

    // Verify window.alert was NOT called
    expect(window.alert).not.toHaveBeenCalled();
  });
});
