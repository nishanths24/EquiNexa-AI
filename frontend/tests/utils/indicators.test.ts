import { describe, it, expect } from 'vitest';
import {
  calculateSMA,
  calculateEMA,
  calculateRSI,
  calculateMACD,
  calculateBollingerBands,
  calculateATR,
  type OHLCV
} from '../../src/utils/indicators';

const mockData: OHLCV[] = Array.from({ length: 50 }, (_, i) => ({
  time: `2023-01-${String((i % 30) + 1).padStart(2, '0')}`,
  open: 100 + i,
  high: 105 + i,
  low: 95 + i,
  close: 102 + i,
  volume: 1000 + i * 10
}));

describe('Technical Indicators', () => {
  it('calculateSMA handles empty and small arrays', () => {
    expect(calculateSMA([], 10)).toEqual([]);
    expect(calculateSMA(mockData.slice(0, 5), 10)).toEqual([]);
  });

  it('calculateSMA computes correct values', () => {
    const sma = calculateSMA(mockData, 5);
    expect(sma.length).toBe(46);
    // For 5 period SMA on steadily increasing data, value should be average of last 5
    // i=4 (values: 102, 103, 104, 105, 106) -> avg = 104
    expect(sma[0].value).toBe(104);
  });

  it('calculateEMA handles insufficient data', () => {
    expect(calculateEMA(mockData.slice(0, 5), 10)).toEqual([]);
  });

  it('calculateRSI computes RSI values properly', () => {
    const rsi = calculateRSI(mockData, 14);
    expect(rsi.length).toBe(36);
    // In our strictly increasing mock data, RSI should be 100
    expect(rsi[0].value).toBe(100);
  });

  it('calculateBollingerBands returns correct structure', () => {
    const bb = calculateBollingerBands(mockData, 20, 2);
    expect(bb.length).toBe(31);
    expect(bb[0].middle).toBeDefined();
    expect(bb[0].upper).toBeGreaterThan(bb[0].middle);
    expect(bb[0].lower).toBeLessThan(bb[0].middle);
  });

  it('calculateMACD returns correct structure', () => {
    const macd = calculateMACD(mockData, 12, 26, 9);
    // should have some values
    expect(macd.length).toBeGreaterThan(0);
    expect(macd[0].macd).toBeDefined();
    expect(macd[0].signal).toBeDefined();
    expect(macd[0].histogram).toBeDefined();
  });

  it('calculateATR returns correct structure', () => {
    const atr = calculateATR(mockData, 14);
    expect(atr.length).toBe(36);
    // True range is constant in our mock data: High - Low = 10
    expect(atr[0].value).toBeCloseTo(10, 1);
  });
});
