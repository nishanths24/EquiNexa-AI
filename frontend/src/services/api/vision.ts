import { fetchClient } from './client';

export interface VisionAnalysisResponse {
  has_sufficient_evidence: boolean;
  support_levels: number[];
  resistance_levels: number[];
  detected_trend: string;
  patterns: string[];
  reasoning: string;
}

export const analyzeChartImage = async (file: File, ticker?: string, timeframe?: string): Promise<VisionAnalysisResponse> => {
  const formData = new FormData();
  formData.append('file', file);
  if (ticker) formData.append('ticker', ticker);
  if (timeframe) formData.append('timeframe', timeframe);

  return await fetchClient('/api/v1/vision/analyze', {
    method: 'POST',
    body: formData,
  });
};
