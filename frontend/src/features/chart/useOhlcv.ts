import { useState, useEffect } from 'react';

export interface OhlcvData {
  time: string | number;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
  is_complete: boolean;
}

export function useOhlcv(ticker: string, period: string, interval: string) {
  const [data, setData] = useState<OhlcvData[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [metadata, setMetadata] = useState<any>(null);

  useEffect(() => {
    let active = true;
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      setData([]);
      setMetadata(null);
      try {
        const res = await fetch(`/api/v1/markets/history?ticker=${encodeURIComponent(ticker)}&period=${period}&interval=${interval}`);
        const json = await res.json().catch(() => null);
        if (!res.ok) {
          const detailMsg = json?.detail?.message || (typeof json?.detail === 'string' ? json.detail : null) || json?.reason || `HTTP error ${res.status}`;
          throw new Error(typeof detailMsg === 'string' ? detailMsg : JSON.stringify(detailMsg));
        }
        if (!json || json.status !== "OK") {
          throw new Error(json?.reason || "Provider error");
        }
        if (active) {
          // Format timestamps for lightweight charts: yyyy-mm-dd string or unix timestamp
          const formatted = json.data.map((d: any) => {
            // lightweight-charts needs seconds if unix
            let timeVal: any = d.time;
            if (typeof timeVal === 'string' && timeVal.includes("T")) {
              timeVal = new Date(timeVal).getTime() / 1000;
            }
            return {
              ...d,
              time: timeVal as number,
            };
          });
          setData(formatted);
          setMetadata(json.metadata);
        }
      } catch (err: any) {
        if (active) {
          setData([]);
          setError(err.message);
        }
      } finally {
        if (active) setLoading(false);
      }
    };

    if (ticker) {
      fetchData();
    }

    return () => { active = false; };
  }, [ticker, period, interval]);

  return { data, loading, error, metadata };
}
