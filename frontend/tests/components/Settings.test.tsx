/**
 * @vitest-environment jsdom
 */
import { describe, it, expect, beforeEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Settings from '../../src/pages/Settings';
import { ThemeProvider } from '../../src/context/ThemeContext';

describe('Settings Theme Toggle Component Test', () => {
  beforeEach(() => {
    localStorage.clear();
    document.documentElement.classList.remove('dark', 'light-theme');
  });

  it('renders default Light Mode and switches to Dark Mode on click', () => {
    render(
      <ThemeProvider>
        <BrowserRouter>
          <Settings />
        </BrowserRouter>
      </ThemeProvider>
    );

    // Initial state: Light Mode
    expect(screen.getByText(/Active:/i).textContent).toContain('Light Mode');
    const toggleButton = screen.getByRole('button', { name: /Switch to Dark Mode/i });
    expect(toggleButton).toBeDefined();
    expect(document.documentElement.classList.contains('dark')).toBe(false);

    // Click toggle to switch to Dark Mode
    fireEvent.click(toggleButton);

    expect(screen.getByText(/Active:/i).textContent).toContain('Dark Mode');
    expect(document.documentElement.classList.contains('dark')).toBe(true);
    expect(localStorage.getItem('theme')).toBe('dark');
    expect(screen.getByRole('button', { name: /Switch to Light Mode/i })).toBeDefined();

    // Click toggle again to switch back to Light Mode
    fireEvent.click(screen.getByRole('button', { name: /Switch to Light Mode/i }));

    expect(screen.getByText(/Active:/i).textContent).toContain('Light Mode');
    expect(document.documentElement.classList.contains('dark')).toBe(false);
    expect(localStorage.getItem('theme')).toBe('light');
  });
});
