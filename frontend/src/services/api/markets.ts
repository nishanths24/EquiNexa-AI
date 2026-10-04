import { fetchClient } from './client';

export interface MarketIndex {
  name: string;
  symbol: string;
  price: number;
  change: number;
  change_percent: number;
  currency: string;
  timestamp: string;
  status: string;
}

export interface SearchResult {
  symbol: string;
  name: string;
  exchange: string;
  type: string;
}

export interface OHLCV {
  time: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

export const fetchIndices = async (): Promise<MarketIndex[]> => {
  const data = await fetchClient('/api/v1/markets/indices');
  if (data.status === 'OK') {
    return data.indices;
  }
  throw new Error(data.reason || 'Failed to fetch indices');
};

export const searchMarkets = async (query: string): Promise<SearchResult[]> => {
  if (!query) return [];
  const data = await fetchClient(`/api/v1/markets/search?q=${encodeURIComponent(query)}`);
  if (data.status === 'OK') {
    return data.results;
  }
  return [];
};

export const fetchHistory = async (ticker: string, period = '1M', interval = '1d'): Promise<OHLCV[]> => {
  const data = await fetchClient(`/api/v1/markets/history?ticker=${encodeURIComponent(ticker)}&period=${period}&interval=${interval}`);
  if (data.status === 'OK') {
    return data.data;
  }
  throw new Error(data.reason || 'Failed to fetch history');
};
