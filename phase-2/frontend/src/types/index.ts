/**
 * TypeScript type definitions for a Todo App
 */

export type TaskPriority = 'high' | 'medium' | 'low';

export type RecurrencePattern = 'daily' | 'weekly' | 'monthly';

export type ReminderStatus = 'pending' | 'sent' | 'snoozed' | 'dismissed';

export interface Tag {
  id: number;
  user_id: string;
  name: string;
  color: string;
  created_at: string;
  updated_at: string;
}

export interface Reminder {
  id: number;
  task_id: number;
  due_time: string;
  status: ReminderStatus;
  snoozed_until: string | null;
  created_at: string;
  updated_at: string;
}

export interface Task {
  id: number;
  user_id: string;
  title: string;
  description: string | null;
  completed: boolean;
  priority: TaskPriority;
  due_date: string | null;
  due_date_tz: string | null;
  recurrence_pattern: RecurrencePattern | null;
  recurrence_parent_id: number | null;
  reminder?: string | null;
  created_at: string;
  updated_at: string;
  completed_at: string | null;
  tags: Tag[];
}

export interface TaskCreate {
  title: string;
  description?: string | null;
}

export interface TaskUpdate {
  title?: string;
  description?: string | null;
  completed?: boolean;
}

export interface TaskExtendedCreate {
  title: string;
  description?: string | null;
  priority: TaskPriority;
  due_date?: string;
  due_date_tz?: string;
  recurrence_pattern?: RecurrencePattern;
  tag_ids?: number[];
}

export interface TaskExtendedUpdate {
  title?: string;
  description?: string | null;
  completed?: boolean;
  priority?: TaskPriority;
  due_date?: string;
  due_date_tz?: string;
  recurrence_pattern?: RecurrencePattern;
  tag_ids?: number[];
}

export interface TaskListResponse {
  tasks: Task[];
  total: number;
  skip: number;
  limit: number;
}

export interface TaskListResponseExtended {
  tasks: Task[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface TagCreate {
  name: string;
  color?: string;
}

export interface TagUpdate {
  name?: string;
  color?: string;
}

export interface TagListResponse {
  tags: Tag[];
  total: number;
}

export interface ReminderCreate {
  due_time: string;
}

export interface RecurringCompleteResponse {
  completed_task: Task;
  new_instance: Task | null;
}

export interface User {
  id: string;
  email: string;
  name: string;
  image?: string | null;
  createdAt: Date;
  updatedAt: Date;
}

export interface Session {
  user: User;
  session: {
    id: string;
    userId: string;
    expiresAt: Date;
  };
}

export interface ChatRequest {
  conversation_id?: string;
  message: string;
}

export interface ToolCall {
  tool: string;
  parameters: Record<string, any>;
  result: Record<string, any>;
}

export interface ChatResponse {
  conversation_id: string;
  response: string;
  tool_calls: ToolCall[];
}
