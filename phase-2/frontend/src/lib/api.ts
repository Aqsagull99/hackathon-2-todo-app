/**
 * API client for backend communication
 */
import type { Task, TaskCreate, TaskUpdate, TaskListResponse } from "@/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

class ApiClient {
  private token: string | null = null;

  setToken(token: string | null) {
    this.token = token;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const headers: HeadersInit = {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    };

    if (this.token) {
      (headers as Record<string, string>)["Authorization"] = `Bearer ${this.token}`;
    }

    const response = await fetch(`${API_URL}${endpoint}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: "An error occurred" }));
      throw new Error(error.detail || `HTTP error! status: ${response.status}`);
    }

    if (response.status === 204) {
      return undefined as T;
    }

    return response.json();
  }

  // Task endpoints
  async getTasks(
    userId: string,
    options: { skip?: number; limit?: number; status?: string } = {}
  ): Promise<TaskListResponse> {
    const params = new URLSearchParams();
    if (options.skip !== undefined) params.set("skip", String(options.skip));
    if (options.limit !== undefined) params.set("limit", String(options.limit));
    if (options.status) params.set("status", options.status);

    const queryString = params.toString();
    const endpoint = `/api/${userId}/tasks${queryString ? `?${queryString}` : ""}`;
    return this.request<TaskListResponse>(endpoint);
  }

  async getTask(userId: string, taskId: number): Promise<Task> {
    return this.request<Task>(`/api/${userId}/tasks/${taskId}`);
  }

  async createTask(userId: string, task: TaskCreate): Promise<Task> {
    return this.request<Task>(`/api/${userId}/tasks`, {
      method: "POST",
      body: JSON.stringify(task),
    });
  }

  async updateTask(userId: string, taskId: number, task: TaskUpdate): Promise<Task> {
    return this.request<Task>(`/api/${userId}/tasks/${taskId}`, {
      method: "PUT",
      body: JSON.stringify(task),
    });
  }

  async deleteTask(userId: string, taskId: number): Promise<void> {
    return this.request<void>(`/api/${userId}/tasks/${taskId}`, {
      method: "DELETE",
    });
  }

  async toggleTask(userId: string, taskId: number): Promise<Task> {
    return this.request<Task>(`/api/${userId}/tasks/${taskId}/complete`, {
      method: "PATCH",
    });
  }
}

export const api = new ApiClient();
