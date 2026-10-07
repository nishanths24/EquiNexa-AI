/**
 * @vitest-environment jsdom
 */
import { render } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { V2AdvancedChart, ChartData } from '../V2AdvancedChart';

// Mock lightweight-charts to avoid DOM/Canvas issues in JSDOM
vi.mock('lightweight-charts', () => ({
  createChart: vi.fn(() => ({
    addCandlestickSeries: vi.fn(() => ({
      setData: vi.fn(),
    })),
    applyOptions: vi.fn(),
    remove: vi.fn(),
  })),
}));

describe('V2AdvancedChart (Phase 5 Chart Test)', () => {
  it('should render the chart container correctly', () => {
    const mockData: ChartData[] = [
      { time: '2026-10-01', open: 100, high: 110, low: 90, close: 105 },
      { time: '2026-10-02', open: 105, high: 115, low: 100, close: 110 },
    ];

    const { getByTestId } = render(<V2AdvancedChart data={mockData} />);
    
    const container = getByTestId('v2-advanced-chart');
    expect(container).toBeDefined();
    
    // Assert responsiveness classes
    expect(container.className).toContain('w-full');
    expect(container.className).toContain('h-full');
  });
});
