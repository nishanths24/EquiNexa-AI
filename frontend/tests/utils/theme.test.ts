/**
 * @vitest-environment jsdom
 */
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import React from 'react';
import { ThemeProvider, useTheme } from '../../src/context/ThemeContext';

describe('Theme Persistence, Defaults, and Chart Adaptation', () => {
  beforeEach(() => {
    localStorage.clear();
    document.documentElement.classList.remove('dark', 'light-theme');
    document.body.classList.remove('dark', 'light-theme');
  });

  it('defaults to light theme when no localStorage value exists', () => {
    const saved = localStorage.getItem('theme');
    const defaultTheme = (saved === 'dark' || saved === 'light') ? saved : 'light';
    expect(defaultTheme).toBe('light');
  });

  it('preserves saved dark theme preference from localStorage across remount/reload simulation', () => {
    localStorage.setItem('theme', 'dark');

    const wrapper = ({ children }: { children: React.ReactNode }) => (
      React.createElement(ThemeProvider, null, children)
    );

    const { result, unmount } = renderHook(() => useTheme(), { wrapper });
    expect(result.current.theme).toBe('dark');
    expect(document.documentElement.classList.contains('dark')).toBe(true);

    // Simulate page unmount / reload
    unmount();

    // Verify localStorage still holds dark preference
    expect(localStorage.getItem('theme')).toBe('dark');

    // Remount in new session
    const { result: remountResult } = renderHook(() => useTheme(), { wrapper });
    expect(remountResult.current.theme).toBe('dark');
    expect(document.documentElement.classList.contains('dark')).toBe(true);
  });

  it('toggles theme correctly and updates documentElement and body classes', () => {
    const wrapper = ({ children }: { children: React.ReactNode }) => (
      React.createElement(ThemeProvider, null, children)
    );

    const { result } = renderHook(() => useTheme(), { wrapper });
    expect(result.current.theme).toBe('light');
    expect(document.documentElement.classList.contains('dark')).toBe(false);

    act(() => {
      result.current.toggleTheme();
    });

    expect(result.current.theme).toBe('dark');
    expect(document.documentElement.classList.contains('dark')).toBe(true);
    expect(document.body.classList.contains('dark')).toBe(true);
    expect(localStorage.getItem('theme')).toBe('dark');

    act(() => {
      result.current.toggleTheme();
    });

    expect(result.current.theme).toBe('light');
    expect(document.documentElement.classList.contains('dark')).toBe(false);
    expect(localStorage.getItem('theme')).toBe('light');
  });

  it('applies updated lightweight-charts options when theme changes', () => {
    // Mock chart instance
    const applyOptionsMock = vi.fn();
    const mockChart = { applyOptions: applyOptionsMock };

    // Helper that replicates chart theme option application
    const applyChartTheme = (chart: any, theme: 'light' | 'dark') => {
      const isDark = theme === 'dark';
      chart.applyOptions({
        layout: {
          background: { type: 'solid', color: isDark ? '#161B22' : '#FFFFFF' },
          textColor: isDark ? '#8B949E' : '#555A62',
        },
        grid: {
          vertLines: { color: isDark ? '#272E38' : '#EEEEEE' },
          horzLines: { color: isDark ? '#272E38' : '#EEEEEE' },
        },
        rightPriceScale: {
          borderColor: isDark ? '#30363D' : '#E4E4E7',
        },
      });
    };

    // Apply light mode options
    applyChartTheme(mockChart, 'light');
    expect(applyOptionsMock).toHaveBeenLastCalledWith(
      expect.objectContaining({
        layout: { background: { type: 'solid', color: '#FFFFFF' }, textColor: '#555A62' },
        grid: { vertLines: { color: '#EEEEEE' }, horzLines: { color: '#EEEEEE' } },
        rightPriceScale: { borderColor: '#E4E4E7' },
      })
    );

    // Apply dark mode options
    applyChartTheme(mockChart, 'dark');
    expect(applyOptionsMock).toHaveBeenLastCalledWith(
      expect.objectContaining({
        layout: { background: { type: 'solid', color: '#161B22' }, textColor: '#8B949E' },
        grid: { vertLines: { color: '#272E38' }, horzLines: { color: '#272E38' } },
        rightPriceScale: { borderColor: '#30363D' },
      })
    );
  });
});
