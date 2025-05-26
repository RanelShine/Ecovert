// apiClient.ts
export const apiClient = () => {
  const token = localStorage.getItem('authToken');
  return fetchWrapper(token);
};

function fetchWrapper(token: string | null) {
  return async (url: string, options: RequestInit = {}) => {
    const headers = {
      ...options.headers,
      'Content-Type': 'application/json',
      ...(token ? { 'Authorization': `Bearer ${token}` } : {})
    };

    return fetch(url, {
      ...options,
      headers,
    });
  };
}
