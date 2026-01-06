// API client that properly handles JWT tokens from Better Auth
import { useSession } from 'better-auth/react';

// Function to get the JWT token from Better Auth
export const getJwtToken = async () => {
  // If you're using the React hook
  const session = await fetch('/api/auth/session').then(res => res.json());
  return session?.token || session?.accessToken;
};

// Main API client function
export const apiClient = async (endpoint, options = {}) => {
  // Get the JWT token
  let token;

  // Try to get token from various sources
  try {
    // Attempt 1: Get from localStorage (if stored there)
    token = localStorage.getItem('better-auth-session-token');

    // Attempt 2: Get from session API if not in localStorage
    if (!token) {
      const sessionResponse = await fetch('/api/auth/session');
      if (sessionResponse.ok) {
        const session = await sessionResponse.json();
        token = session?.token || session?.accessToken || session?.data?.token;
      }
    }
  } catch (error) {
    console.warn('Could not get session from frontend:', error);
  }

  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  // Add Authorization header if token exists
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  } else {
    console.warn('No JWT token found for API request. This may cause authentication errors.');
  }

  const response = await fetch(`http://localhost:8000${endpoint}`, {
    ...options,
    headers,
  });

  return response;
};

// Specific function for creating tasks
export const createTask = async (userId, taskData) => {
  try {
    const response = await apiClient(`/api/${userId}/tasks`, {
      method: 'POST',
      body: JSON.stringify(taskData),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error creating task:', error);
    throw error;
  }
};

// Specific function for getting tasks
export const getTasks = async (userId) => {
  try {
    const response = await apiClient(`/api/${userId}/tasks`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error getting tasks:', error);
    throw error;
  }
};