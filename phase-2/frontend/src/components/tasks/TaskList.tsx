"use client";

import { useState, useEffect, useCallback } from "react";
import type { Task, TaskCreate, TaskUpdate } from "@/types";
import { api } from "@/lib/api";
import { TaskItem } from "./TaskItem";
import { TaskForm } from "./TaskForm";
import { Card, CardHeader, CardContent } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";

interface TaskListProps {
  userId: string;
  accessToken: string;
}

export function TaskList({ userId, accessToken }: TaskListProps) {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");
  const [filter, setFilter] = useState<"all" | "pending" | "completed">("all");
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [showForm, setShowForm] = useState(false);

  // Set token for API client
  useEffect(() => {
    api.setToken(accessToken);
  }, [accessToken]);

  // Fetch tasks
  const fetchTasks = useCallback(async () => {
    setIsLoading(true);
    setError("");
    try {
      const response = await api.getTasks(userId, {
        status: filter === "all" ? undefined : filter,
        limit: 100,
      });
      setTasks(response.tasks);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch tasks");
    } finally {
      setIsLoading(false);
    }
  }, [userId, filter]);

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  // Create task
  const handleCreate = async (data: TaskCreate) => {
    const newTask = await api.createTask(userId, data);
    setTasks((prev) => [newTask, ...prev]);
    setShowForm(false);
  };

  // Update task
  const handleUpdate = async (data: TaskUpdate) => {
    if (!editingTask) return;
    const updatedTask = await api.updateTask(userId, editingTask.id, data);
    setTasks((prev) =>
      prev.map((t) => (t.id === updatedTask.id ? updatedTask : t))
    );
    setEditingTask(null);
  };

  // Toggle task
  const handleToggle = async (taskId: number) => {
    const updatedTask = await api.toggleTask(userId, taskId);
    setTasks((prev) =>
      prev.map((t) => (t.id === updatedTask.id ? updatedTask : t))
    );
  };

  // Delete task
  const handleDelete = async (taskId: number) => {
    await api.deleteTask(userId, taskId);
    setTasks((prev) => prev.filter((t) => t.id !== taskId));
  };

  const pendingCount = tasks.filter((t) => !t.completed).length;
  const completedCount = tasks.filter((t) => t.completed).length;

  return (
    <div className="space-y-6">
      {/* Stats */}
      <div className="grid grid-cols-3 gap-4">
        <Card className="p-4 text-center bg-white border-[var(--accent)]">
          <p className="text-3xl font-bold text-[var(--primary)]">{tasks.length}</p>
          <p className="text-sm text-[var(--muted-foreground)]">Total Tasks</p>
        </Card>
        <Card className="p-4 text-center bg-white border-[var(--accent)]">
          <p className="text-3xl font-bold text-[var(--primary)]">{pendingCount}</p>
          <p className="text-sm text-[var(--muted-foreground)]">Pending</p>
        </Card>
        <Card className="p-4 text-center bg-white border-[var(--accent)]">
          <p className="text-3xl font-bold text-[var(--primary)]">{completedCount}</p>
          <p className="text-sm text-[var(--muted-foreground)]">Completed</p>
        </Card>
      </div>

      {/* Add Task Button / Form */}
      <Card className="bg-white border-[var(--accent)]">
        <CardHeader>
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold text-[var(--foreground)]">
              {showForm ? "Add New Task" : editingTask ? "Edit Task" : "My Tasks"}
            </h2>
            {!showForm && !editingTask && (
              <Button onClick={() => setShowForm(true)}>+ Add Task</Button>
            )}
          </div>
        </CardHeader>
        <CardContent>
          {(showForm || editingTask) && (
            <TaskForm
              task={editingTask}
              onSubmit={async (data) => {
                if (editingTask) {
                  await handleUpdate(data as TaskUpdate);
                } else {
                  await handleCreate(data as TaskCreate);
                }
              }}
              onCancel={() => {
                setShowForm(false);
                setEditingTask(null);
              }}
            />
          )}

          {!showForm && !editingTask && (
            <>
              {/* Filter tabs */}
              <div className="flex gap-2 mb-4">
                {(["all", "pending", "completed"] as const).map((f) => (
                  <button
                    key={f}
                    onClick={() => setFilter(f)}
                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-[var(--primary)] focus:ring-offset-2 ${
                      filter === f
                        ? "bg-[var(--primary)] text-white"
                        : "bg-[var(--secondary)] text-[var(--secondary-foreground)] hover:bg-[var(--accent)]"
                    }`}
                    aria-label={`Filter by ${f} tasks`}
                    aria-pressed={filter === f}
                  >
                    {f.charAt(0).toUpperCase() + f.slice(1)}
                  </button>
                ))}
              </div>

              {/* Task list */}
              {isLoading ? (
                <div className="py-16 text-center text-[var(--muted-foreground)]" role="status" aria-live="polite">
                  <svg
                    className="animate-spin h-8 w-8 mx-auto text-[var(--primary)] mb-2"
                    fill="none"
                    viewBox="0 0 24 24"
                    aria-hidden="true"
                  >
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                    />
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    />
                  </svg>
                  Loading tasks...
                </div>
              ) : error ? (
                <div className="py-16 text-center text-red-600" role="alert" aria-live="assertive">
                  <p>{error}</p>
                </div>
              ) : tasks.length === 0 ? (
                <div className="py-16 flex flex-col items-center justify-center text-center space-y-6">
                  <div
                    className="w-20 h-20 rounded-full bg-[var(--secondary)] flex items-center justify-center"
                    aria-hidden="true"
                  >
                    <svg
                      className="w-10 h-10 text-[var(--primary)]"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
                      />
                    </svg>
                  </div>
                  <div className="space-y-2">
                    <h3 className="text-2xl font-semibold text-[var(--foreground)]">
                      No tasks yet
                    </h3>
                    <p className="text-[var(--muted-foreground)] max-w-md">
                      Get started by creating your first task and stay organized.
                    </p>
                  </div>
                  <Button
                    size="lg"
                    onClick={() => setShowForm(true)}
                    className="px-8 py-3 text-base"
                  >
                    + Create Your First Task
                  </Button>
                </div>
              ) : (
                <div className="divide-y divide-[var(--border)]" role="list" aria-label="Task list">
                  {tasks.map((task) => (
                    <TaskItem
                      key={task.id}
                      task={task}
                      onToggle={handleToggle}
                      onDelete={handleDelete}
                      onEdit={setEditingTask}
                    />
                  ))}
                </div>
              )}
            </>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
