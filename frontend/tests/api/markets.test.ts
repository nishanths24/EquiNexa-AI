import { vi, describe, it, expect, beforeEach } from 'vitest';
import { fetchHistory } from '../../src/services/api/markets';

// Mock the client
vi.mock('../../src/services/api/client', () => ({
  fetchClient: vi.fn()
}));

import { fetchClient } from '../../src/services/api/client';

describe('markets API client', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('fetchHistory maps arguments to URL correctly', async () => {
    vi.mocked(fetchClient).mockResolvedValue({ status: 'OK', data: [] });
    await fetchHistory('^NSEI', 'YTD', '1d');
    expect(fetchClient).toHaveBeenCalledWith('/api/v1/markets/history?ticker=%5ENSEI&period=YTD&interval=1d');
  });

  it('fetchHistory handles error states correctly', async () => {
    vi.mocked(fetchClient).mockResolvedValue({ status: 'ERROR', reason: 'Unknown range preset' });
    await expect(fetchHistory('^NSEI', 'UNKNOWN', '1d')).rejects.toThrow('Unknown range preset');
  });
});
