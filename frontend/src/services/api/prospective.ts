export interface ProspectiveStatus {
  model_version: string;
  target: string;
  evaluated: number;
  pending: number;
  required: number;
  remaining: number;
  total_logged: number;
  rejected_duplicates: number;
  integrity_violations: number;
  oldest_pending: string;
  latest_prediction: string;
  review_status: string;
}

const API_BASE = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

export const fetchProspectiveStatus = async (): Promise<ProspectiveStatus> => {
  const response = await fetch(`${API_BASE}/api/v1/research/status`);
  if (!response.ok) {
    throw new Error('Failed to fetch prospective status');
  }
  return response.json();
};
