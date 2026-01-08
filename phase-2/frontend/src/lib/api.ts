/**
 * API client for backend communication with extended features
 */
import type {
  Task,
  TaskCreate,
  TaskUpdate,
  TaskListResponse,
  TaskExtendedCreate,
  TaskExtendedUpdate,
  TaskListResponseExtended,
  Tag,
  TagCreate,
  TagUpdate,
  TagListResponse,
  Reminder,
  ReminderCreate,
  RecurringCompleteResponse,
} from "@/types";

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




  // ============================================================================
  // Task Endpoints (Extended with search/filter/sort)
  // ============================================================================

  async getTasks(
    _userId: string,
    options: {
      search?: string;
      status?: string;
      priority?: string;
      due_date_from?: string;
      due_date_to?: string;
      tag_ids?: string;
      sort_by?: string;
      sort_order?: string;
      page?: number;
      page_size?: number;
    } = {}
  ): Promise<TaskListResponseExtended> {
    const params = new URLSearchParams();
    if (options.search) params.set("search", options.search);
    if (options.status) params.set("status", options.status);
    if (options.priority) params.set("priority", options.priority);
    if (options.due_date_from) params.set("due_date_from", options.due_date_from);
    if (options.due_date_to) params.set("due_date_to", options.due_date_to);
    if (options.tag_ids) params.set("tag_ids", options.tag_ids);
    if (options.sort_by) params.set("sort_by", options.sort_by);
    if (options.sort_order) params.set("sort_order", options.sort_order);
    if (options.page) params.set("page", String(options.page));
    if (options.page_size) params.set("page_size", String(options.page_size));

    const queryString = params.toString();
    const endpoint = `/api/tasks${queryString ? `?${queryString}` : ""}`;
    return this.request<TaskListResponseExtended>(endpoint);
  }

  async getTask(userId: string, taskId: number): Promise<Task> {
    return this.request<Task>(`/api/${userId}/tasks/${taskId}`);
  }

  async createTask(
    _userId: string,
    task: TaskExtendedCreate
  ): Promise<Task> {
    return this.request<Task>(`/api/tasks`, {
      method: "POST",
      body: JSON.stringify(task),
    });
  }

  async updateTask(
    userId: string,
    taskId: number,
    task: TaskExtendedUpdate
  ): Promise<Task> {
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

  async toggleTask(
    userId: string,
    taskId: number
  ): Promise<RecurringCompleteResponse> {
    return this.request<RecurringCompleteResponse>(
      `/api/${userId}/tasks/${taskId}/complete`,
      {
        method: "PATCH",
      }
    );
  }

  async skipTask(userId: string, taskId: number): Promise<RecurringCompleteResponse> {
    return this.request<RecurringCompleteResponse>(
      `/api/${userId}/tasks/${taskId}/skip`,
      {
        method: "POST",
      }
    );
  }

  async cancelRecurrence(userId: string, taskId: number): Promise<Task> {
    return this.request<Task>(`/api/${userId}/tasks/${taskId}/recurrence`, {
      method: "DELETE",
    });
  }

  // ============================================================================
  // Tag Endpoints
  // ============================================================================

  async getTags(userId: string): Promise<TagListResponse> {
    return this.request<TagListResponse>(`/api/${userId}/tags`);
  }

  async createTag(
    userId: string,
    data: TagCreate
  ): Promise<Tag> {
    return this.request<Tag>(`/api/${userId}/tags`, {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  async updateTag(
    userId: string,
    tagId: number,
    data: TagUpdate
  ): Promise<Tag> {
    return this.request<Tag>(`/api/${userId}/tags/${tagId}`, {
      method: "PATCH",
      body: JSON.stringify(data),
    });
  }

  async deleteTag(userId: string, tagId: number): Promise<{ message: string; affected_task_ids: number[] }> {
    return this.request<{ message: string; affected_task_ids: number[] }>(
      `/api/${userId}/tags/${tagId}`,
      {
        method: "DELETE",
      }
    );
  }

  // ============================================================================
  // Reminder Endpoints
  // ============================================================================

  async getReminder(userId: string, taskId: number): Promise<Reminder> {
    return this.request<Reminder>(`/api/${userId}/tasks/${taskId}/reminder`);
  }

  async createReminder(
    userId: string,
    taskId: number,
    dueTime: string
  ): Promise<Reminder> {
    return this.request<Reminder>(`/api/${userId}/tasks/${taskId}/reminder`, {
      method: "POST",
      body: JSON.stringify({ due_time: dueTime }),
    });
  }

  async snoozeReminder(
    userId: string,
    reminderId: number,
    minutes: number
  ): Promise<Reminder> {
    return this.request<Reminder>(`/api/${userId}/reminders/${reminderId}/snooze`, {
      method: "POST",
      body: JSON.stringify({ minutes }),
    });
  }

  async dismissReminder(userId: string, reminderId: number): Promise<void> {
    return this.request<void>(`/api/${userId}/reminders/${reminderId}`, {
      method: "DELETE",
    });
  }
}

export const api = new ApiClient();
