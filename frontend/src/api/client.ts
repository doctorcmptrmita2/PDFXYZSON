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
    // Check if backend health endpoint is reachable
    const healthUrl = API_BASE_URL.replace('/api', '/health');
    try {
      const healthResponse = await fetch(healthUrl, { 
        method: 'GET',
        mode: 'cors',
        credentials: 'include',
      });
      if (healthResponse.ok) {
        // Backend is reachable, but specific endpoint failed - likely CORS or endpoint issue
        throw new Error(
          `Backend çalışıyor ancak endpoint'e erişilemiyor:\n` +
          `Endpoint: ${API_BASE_URL}${endpoint}\n` +
          `Health Check: ${healthUrl} ✓\n` +
          `Lütfen endpoint URL'ini ve CORS ayarlarını kontrol edin.\n` +
          `Tarayıcı konsolunu (F12) kontrol edin.`
        );
      }
    } catch (healthError) {
      // Backend is not reachable at all
      throw new Error(
        `Backend'e bağlanılamıyor. Lütfen backend'in çalıştığından emin olun:\n` +
        `1. Backend terminalinde: cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8001\n` +
        `2. Tarayıcıda test edin: http://localhost:8001/health\n` +
        `3. API URL: ${API_BASE_URL}${endpoint}\n` +
        `4. Health Check URL: ${healthUrl}\n` +
        `5. Tarayıcı konsolunu (F12) kontrol edin.`
      );
    }
  }
  throw error;
}

export async function apiGet<T>(endpoint: string): Promise<T> {
  try {
    const url = `${API_BASE_URL}${endpoint}`;
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      mode: 'cors',
      credentials: 'include',
    });
    
    if (!response.ok) {
      console.error(`API Error [${response.status}]: ${url}`, response);
    }
    
    return handleResponse<T>(response);
  } catch (error) {
    console.error('Fetch error:', error, 'Endpoint:', endpoint);
    return handleFetchError(error, endpoint);
  }
}

export async function apiPost<T>(
  endpoint: string,
  body?: FormData | object
): Promise<T> {
  const options: RequestInit = {
    method: 'POST',
    mode: 'cors',
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
    const url = `${API_BASE_URL}${endpoint}`;
    const response = await fetch(url, options);
    return handleResponse<T>(response);
  } catch (error) {
    console.error('Fetch error:', error, 'Endpoint:', endpoint);
    return handleFetchError(error, endpoint);
  }
}

export async function apiPut<T>(
  endpoint: string,
  body: object
): Promise<T> {
  try {
    const url = `${API_BASE_URL}${endpoint}`;
    const response = await fetch(url, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
      mode: 'cors',
      credentials: 'include',
    });
    
    if (!response.ok) {
      console.error(`API Error [${response.status}]: ${url}`, response);
    }
    
    return handleResponse<T>(response);
  } catch (error) {
    console.error('Fetch error:', error, 'Endpoint:', endpoint);
    return handleFetchError(error, endpoint);
  }
}

export async function apiGetBlob(endpoint: string): Promise<Blob> {
  try {
    const url = `${API_BASE_URL}${endpoint}`;
    const response = await fetch(url, {
      mode: 'cors',
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
    console.error('Fetch error:', error, 'Endpoint:', endpoint);
    return handleFetchError(error, endpoint);
  }
}
