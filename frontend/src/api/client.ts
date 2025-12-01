const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001/api';

export interface ApiError {
  detail: string;
}

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    let errorMessage = `HTTP error! status: ${response.status}`;
    try {
      const errorData: ApiError = await response.json();
      errorMessage = errorData.detail || errorMessage;
    } catch {
      // If response is not JSON, use status text
      errorMessage = response.statusText || errorMessage;
    }
    throw new Error(errorMessage);
  }

  return response.json();
}

async function handleFetchError(error: unknown, endpoint: string): Promise<never> {
  if (error instanceof TypeError && error.message.includes('fetch')) {
    throw new Error(
      `Backend'e bağlanılamıyor. Lütfen backend'in çalıştığından emin olun:\n` +
      `1. Backend terminalinde: cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8001\n` +
      `2. Tarayıcıda test edin: http://localhost:8001/health\n` +
      `3. API URL: ${API_BASE_URL}${endpoint}`
    );
  }
  throw error;
}

export async function apiGet<T>(endpoint: string): Promise<T> {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
    });
    return handleResponse<T>(response);
  } catch (error) {
    return handleFetchError(error, endpoint);
  }
}

export async function apiPost<T>(
  endpoint: string,
  body?: FormData | object
): Promise<T> {
  const options: RequestInit = {
    method: 'POST',
    credentials: 'include',
  };

  if (body instanceof FormData) {
    options.body = body;
  } else if (body) {
    options.headers = {
      'Content-Type': 'application/json',
    };
    options.body = JSON.stringify(body);
  }

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
    return handleResponse<T>(response);
  } catch (error) {
    return handleFetchError(error, endpoint);
  }
}

export async function apiPut<T>(
  endpoint: string,
  body: object
): Promise<T> {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
      credentials: 'include',
    });
    return handleResponse<T>(response);
  } catch (error) {
    return handleFetchError(error, endpoint);
  }
}

export async function apiGetBlob(endpoint: string): Promise<Blob> {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      credentials: 'include',
    });
    if (!response.ok) {
      let errorMessage = `HTTP error! status: ${response.status}`;
      try {
        const errorData: ApiError = await response.json();
        errorMessage = errorData.detail || errorMessage;
      } catch {
        errorMessage = response.statusText || errorMessage;
      }
      throw new Error(errorMessage);
    }
    return response.blob();
  } catch (error) {
    return handleFetchError(error, endpoint);
  }
}

