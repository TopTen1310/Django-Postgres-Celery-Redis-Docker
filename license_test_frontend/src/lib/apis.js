const API_URL = process.env.REACT_APP_API_URL;

export const ApiService = async (endpoint, method = 'GET', data = null, headers = {}) => {
  const config = {
    method: method,
    headers: {
      'Content-Type': 'application/json',
      ...headers
    }
  };

  if (data) {
    config.body = JSON.stringify(data);
  }

  try {
    const response = await fetch(`${API_URL}${endpoint}`, config);
    if (!response.ok) {
      throw new Error(`API request failed with status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error(`Failed to fetch from the endpoint: ${endpoint}. Error: ${error.message}`);
    throw error;
  }
};