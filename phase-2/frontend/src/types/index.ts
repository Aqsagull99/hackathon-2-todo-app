/**
 * TypeScript type definitions for the Todo App
 */

export interface Task {
  id: number;
  user_id: string;
  title: string;
  description: string | null;
  completed: boolean;
  created_at: string;
  updated_at: string;
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

export interface TaskListResponse {
  tasks: Task[];
  total: number;
  skip: number;
  limit: number;
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
