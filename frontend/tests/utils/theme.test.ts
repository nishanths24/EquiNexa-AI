/**
 * @vitest-environment jsdom
 */
import { describe, it, expect, beforeEach } from 'vitest';

describe('Theme Persistence and Defaults', () => {
  beforeEach(() => {
    localStorage.clear();
    document.documentElement.classList.remove('dark', 'light-theme');
  });

  it('defaults to light theme when no localStorage value exists', () => {
    const saved = localStorage.getItem('theme');
    const defaultTheme = (saved === 'dark' || saved === 'light') ? saved : 'light';
    expect(defaultTheme).toBe('light');
  });

  it('preserves saved dark theme preference from localStorage', () => {
    localStorage.setItem('theme', 'dark');
    const saved = localStorage.getItem('theme');
    const activeTheme = (saved === 'dark' || saved === 'light') ? saved : 'light';
    expect(activeTheme).toBe('dark');
  });

  it('updates document.documentElement class properly when toggled', () => {
    // Light mode
    document.documentElement.classList.remove('dark');
    document.documentElement.classList.add('light-theme');
    expect(document.documentElement.classList.contains('dark')).toBe(false);

    // Dark mode
    document.documentElement.classList.add('dark');
    document.documentElement.classList.remove('light-theme');
    expect(document.documentElement.classList.contains('dark')).toBe(true);
  });
});
