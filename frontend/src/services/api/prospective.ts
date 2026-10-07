import { fetchClient } from './client';

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

export const fetchProspectiveStatus = async (): Promise<ProspectiveStatus> => {
  return await fetchClient('/api/v1/research/status');
};
