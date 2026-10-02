import { describe, it, expect, vi, beforeEach } from 'vitest';
import { fetchProspectiveStatus } from '../../src/services/api/prospective';

describe('Prospective API Client', () => {
  beforeEach(() => {
    vi.stubGlobal('fetch', vi.fn());
  });

  it('fetches status successfully and prevents mock fallback', async () => {
    const mockResponse = {
      model_version: '1.0.0',
      evaluated: 0,
      target: '5-day return > 2%',
    };

    vi.mocked(fetch).mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
    } as Response);

    const data = await fetchProspectiveStatus();
    expect(data.model_version).toBe('1.0.0');
    expect(data.evaluated).toBe(0);
    // Explicitly check that we did NOT fall back to a fake dataset
    expect(fetch).toHaveBeenCalledWith(expect.stringContaining('/api/v1/research/status'));
  });

  it('throws an error correctly on API failure', async () => {
    vi.mocked(fetch).mockResolvedValueOnce({
      ok: false,
    } as Response);

    await expect(fetchProspectiveStatus()).rejects.toThrow('Failed to fetch prospective status');
  });
});
