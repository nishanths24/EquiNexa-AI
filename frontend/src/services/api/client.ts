const API_BASE = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

export class ApiError extends Error {
  public status: number;
  public data: any;

  constructor(status: number, message: string, data?: any) {
    super(message);
    this.status = status;
    this.data = data;
    this.name = 'ApiError';
  }
}

export const fetchClient = async (endpoint: string, options: RequestInit = {}) => {
  const url = `${API_BASE}${endpoint.startsWith('/') ? endpoint : `/${endpoint}`}`;
  
  try {
    const response = await fetch(url, options);
    
    // Parse JSON if possible
    let data;
    const contentType = response.headers?.get ? response.headers.get('content-type') : null;
    if (contentType && contentType.includes('application/json')) {
      data = await response.json().catch(() => null);
    } else {
      data = await response.text().catch(() => null);
    }

    if (!response.ok) {
      let errorMessage = 'API Request Failed';
      if (data?.detail) {
        errorMessage = typeof data.detail === 'string' ? data.detail : JSON.stringify(data.detail);
      } else if (data?.message) {
        errorMessage = typeof data.message === 'string' ? data.message : JSON.stringify(data.message);
      } else if (typeof data === 'string') {
        errorMessage = data;
      } else if (data && typeof data === 'object') {
        errorMessage = JSON.stringify(data);
      }
      throw new ApiError(response.status, errorMessage, data);
    }

    return data;
  } catch (err: any) {
    if (err instanceof ApiError) {
      throw err;
    }
    // Network errors (CORS, offline, timeout)
    throw new Error(`Failed to fetch from backend: ${err.message}`);
  }
};
