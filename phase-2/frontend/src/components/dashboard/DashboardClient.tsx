"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import {
  ListTodo,
  CheckCircle2,
  List,
  Plus,
  Calendar,
  Clock,
  Tag,
  Flag,
  Bell
} from "lucide-react";
import { api } from "@/lib/api";
import type { Task, TaskCreate, TaskExtendedCreate } from "@/types";
import { cn } from "@/lib/utils";
import { NotificationProvider } from "@/lib/contexts/NotificationContext";

interface DashboardClientProps {
  userId: string;
  accessToken: string;
  userName: string | null;
  initialShowAddTask?: boolean;
}

export function DashboardClient({ userId, accessToken, userName, initialShowAddTask = false }: DashboardClientProps) {
  const [currentFilter, setCurrentFilter] = useState<"all" | "pending" | "completed">("all");
  const [tasks, setTasks] = useState<Task[]>([]);
  const [showAddTask, setShowAddTask] = useState(initialShowAddTask);
  const [newTask, setNewTask] = useState({
    title: "",
    description: "",
    priority: "medium" as "low" | "medium" | "high",
    tags: "",
    dueDate: "",
    recurring: false,
    reminder: false
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Set token for API client
  useEffect(() => {
    api.setToken(accessToken);
  }, [accessToken]);

  // Fetch tasks
  useEffect(() => {
    const fetchTasks = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const response = await api.getTasks(userId, {
          status: currentFilter === "all" ? undefined : currentFilter,
          limit: 100,
        });
        setTasks(response.tasks);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to fetch tasks");
      } finally {
        setIsLoading(false);
      }
    };

    fetchTasks();
  }, [userId, currentFilter, accessToken]);

  const pendingCount = tasks.filter(t => !t.completed).length;
  const completedCount = tasks.filter(t => t.completed).length;

  const handleCreateTask = async () => {
    if (!newTask.title.trim()) {
      setError("Title is required");
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      // Format task data for extended task creation
      const taskData: TaskExtendedCreate = {
        title: newTask.title,
        description: newTask.description || undefined,
        priority: newTask.priority,
        due_date: newTask.dueDate ? new Date(newTask.dueDate).toISOString() : undefined,
        due_date_tz: "UTC", // Default timezone
        tag_ids: [] as number[], // Will need to handle tags separately
        recurrence_pattern: newTask.recurring ? "daily" as const : undefined, // Assuming daily as default if recurring is enabled
      };

      const createdTask = await api.createTask(userId, taskData);
      setTasks(prev => [createdTask, ...prev]);
      setNewTask({
        title: "",
        description: "",
        priority: "medium",
        tags: "",
        dueDate: "",
        recurring: false,
        reminder: false
      });
      setShowAddTask(false);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else if (typeof err === 'string') {
        setError(err);
      } else {
        setError("Failed to create task: " + JSON.stringify(err));
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleCancel = () => {
    setNewTask({
      title: "",
      description: "",
      priority: "medium",
      tags: "",
      dueDate: "",
      recurring: false,
      reminder: false
    });
    setShowAddTask(false);
    setError(null);
  };

  const filterOptions = [
    { value: "all" as const, label: "All Tasks", icon: List },
    { value: "pending" as const, label: "Active Tasks", icon: ListTodo },
    { value: "completed" as const, label: "Completed", icon: CheckCircle2 },
  ];

  return (
    <NotificationProvider userId={userId}>
      <div className="min-h-screen bg-[#0a0a0f] flex">
      {/* Sidebar */}
      <div className="w-64 bg-[rgba(255,110,199,0.12)] border-r border-[rgba(255,110,199,0.35)] backdrop-blur-24 flex flex-col">
        <div className="p-6 border-b border-[rgba(255,110,199,0.35)]">
          <h2 className="text-xl font-bold text-white">
            Todo<span className="text-[#db2777]">Pink</span>
          </h2>
          <p className="text-xs text-white mt-1">Task Management</p>
        </div>

        <nav className="flex-1 px-3 py-4 space-y-1">
          {filterOptions.map(({ value, label, icon: Icon }) => {
            const isActive = currentFilter === value;
            return (
              <button
                key={value}
                onClick={() => setCurrentFilter(value)}
                className={cn(
                  "w-full group flex items-center px-4 py-3 text-sm font-medium rounded-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-[rgba(255,110,199,0.4)] focus:ring-offset-2 focus:ring-offset-[#0a0a0f]",
                  isActive
                    ? "bg-[rgba(255,110,199,0.25)] text-white shadow-lg shadow-[rgba(255,110,199,0.15)]"
                    : "text-[rgba(255,255,255,0.7)] hover:bg-[rgba(255,110,199,0.18)] hover:text-white"
                )}
                aria-label={`Filter: ${label}`}
                aria-pressed={isActive}
              >
                <Icon className={cn("mr-3 h-5 w-5", isActive ? "text-[#db2777]" : "text-[rgba(255,255,255,0.7)]")} />
                {label}
              </button>
            );
          })}
        </nav>

        <div className="p-4 border-t border-[rgba(255,110,199,0.35)] bg-[rgba(255,110,199,0.18)]">
          <div className="text-center text-xs text-white">
            <p>TodoPink v1.0</p>
            <p className="mt-1">Stay Organized</p>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Welcome Section */}
        <div className="p-8 border-b border-[rgba(255,110,199,0.35)] bg-[rgba(255,110,199,0.06)] backdrop-blur-sm">
          <h1 className="text-2xl font-semibold text-white">
            Welcome {userName || "User"}!
          </h1>
          <p className="text-sm text-white mt-1">
            Manage your tasks and stay productive.
          </p>
        </div>

        {/* Main Content Area */}
        <div className="flex-1 p-8">
          <div className="max-w-6xl mx-auto space-y-8">
            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: 0.1 }}
                className="glass rounded-2xl p-6 text-center"
              >
                <div className="w-12 h-12 bg-[rgba(255,110,199,0.1)] rounded-full flex items-center justify-center mx-auto mb-3">
                  <List className="w-6 h-6 text-[#db2777]" />
                </div>
                <p className="text-3xl font-bold text-[#db2777]">{tasks.length}</p>
                <p className="text-sm text-[rgba(255,255,255,0.5)] mt-1">Total Tasks</p>
              </motion.div>

              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: 0.2 }}
                className="glass rounded-2xl p-6 text-center"
              >
                <div className="w-12 h-12 bg-[rgba(255,110,199,0.1)] rounded-full flex items-center justify-center mx-auto mb-3">
                  <ListTodo className="w-6 h-6 text-[#db2777]" />
                </div>
                <p className="text-3xl font-bold text-[#db2777]">{pendingCount}</p>
                <p className="text-sm text-[rgba(255,255,255,0.5)] mt-1">Active Tasks</p>
              </motion.div>

              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: 0.3 }}
                className="glass rounded-2xl p-6 text-center"
              >
                <div className="w-12 h-12 bg-[rgba(255,110,199,0.1)] rounded-full flex items-center justify-center mx-auto mb-3">
                  <CheckCircle2 className="w-6 h-6 text-[#db2777]" />
                </div>
                <p className="text-3xl font-bold text-[#db2777]">{completedCount}</p>
                <p className="text-sm text-[rgba(255,255,255,0.5)] mt-1">Completed</p>
              </motion.div>
            </div>

            {/* Add New Task Panel */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: 0.4 }}
              className="glass rounded-2xl p-6"
            >
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-semibold text-white">
                  {showAddTask ? "Add New Task" : "Quick Add Task"}
                </h2>
                {!showAddTask && (
                  <button
                    onClick={() => setShowAddTask(true)}
                    className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-[rgba(255,110,199,0.9)] to-[rgba(219,39,119,0.9)] text-white rounded-lg hover:from-[rgba(255,110,199,1)] hover:to-[rgba(219,39,119,1)] transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-[rgba(255,110,199,0.4)] focus:ring-offset-2 focus:ring-offset-[#0a0a0f]"
                  >
                    <Plus className="w-4 h-4" />
                    Add Task
                  </button>
                )}
              </div>

              {showAddTask && (
                <div className="space-y-6">
                  {error && (
                    <div className="p-3 bg-red-500/10 border border-red-500/30 rounded-lg text-sm text-red-400">
                      {error}
                    </div>
                  )}

                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-[rgba(255,110,199,0.9)] mb-2">
                        Title *
                      </label>
                      <input
                        type="text"
                        value={newTask.title}
                        onChange={(e) => setNewTask(prev => ({ ...prev, title: e.target.value }))}
                        className="w-full px-4 py-3 rounded-lg text-white placeholder-[rgba(255,255,255,0.4)] bg-[rgba(255,255,255,0.08)] border border-[rgba(255,110,199,0.25)] backdrop-blur-sm focus:outline-none focus:border-[rgba(255,110,199,0.5)] focus:ring-2 focus:ring-[rgba(255,110,199,0.2)]"
                        placeholder="Enter task title"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-[rgba(255,110,199,0.9)] mb-2">
                        Description
                      </label>
                      <textarea
                        value={newTask.description}
                        onChange={(e) => setNewTask(prev => ({ ...prev, description: e.target.value }))}
                        rows={3}
                        className="w-full px-4 py-3 rounded-lg text-white placeholder-[rgba(255,255,255,0.4)] bg-[rgba(255,255,255,0.08)] border border-[rgba(255,110,199,0.25)] backdrop-blur-sm focus:outline-none focus:border-[rgba(255,110,199,0.5)] focus:ring-2 focus:ring-[rgba(255,110,199,0.2)] resize-none"
                        placeholder="Enter task description"
                      />
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-[rgba(255,110,199,0.9)] mb-2">
                          Priority
                        </label>
                        <select
                          value={newTask.priority}
                          onChange={(e) => setNewTask(prev => ({ ...prev, priority: e.target.value as any }))}
                          className="w-full px-4 py-3 rounded-lg text-white bg-[rgba(255,255,255,0.08)] border border-[rgba(255,110,199,0.25)] backdrop-blur-sm focus:outline-none focus:border-[rgba(255,110,199,0.5)] focus:ring-2 focus:ring-[rgba(255,110,199,0.2)]"
                        >
                          <option value="low">Low</option>
                          <option value="medium">Medium</option>
                          <option value="high">High</option>
                        </select>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-[rgba(255,110,199,0.9)] mb-2">
                          Due Date
                        </label>
                        <input
                          type="date"
                          value={newTask.dueDate}
                          onChange={(e) => setNewTask(prev => ({ ...prev, dueDate: e.target.value }))}
                          className="w-full px-4 py-3 rounded-lg text-white bg-[rgba(255,255,255,0.08)] border border-[rgba(255,110,199,0.25)] backdrop-blur-sm focus:outline-none focus:border-[rgba(255,110,199,0.5)] focus:ring-2 focus:ring-[rgba(255,110,199,0.2)]"
                        />
                      </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-[rgba(255,110,199,0.9)] mb-2">
                          Tags
                        </label>
                        <input
                          type="text"
                          value={newTask.tags}
                          onChange={(e) => setNewTask(prev => ({ ...prev, tags: e.target.value }))}
                          className="w-full px-4 py-3 rounded-lg text-white placeholder-[rgba(255,255,255,0.4)] bg-[rgba(255,255,255,0.08)] border border-[rgba(255,110,199,0.25)] backdrop-blur-sm focus:outline-none focus:border-[rgba(255,110,199,0.5)] focus:ring-2 focus:ring-[rgba(255,110,199,0.2)]"
                          placeholder="work, personal, urgent (comma separated)"
                        />
                      </div>

                      <div className="flex items-end gap-4">
                        <div className="flex items-center gap-2">
                          <input
                            type="checkbox"
                            id="recurring"
                            checked={newTask.recurring}
                            onChange={(e) => setNewTask(prev => ({ ...prev, recurring: e.target.checked }))}
                            className="w-4 h-4 rounded border-[rgba(255,110,199,0.35)] bg-[rgba(255,255,255,0.08)] checked:bg-[rgba(255,110,199,0.8)] checked:border-[rgba(255,110,199,0.8)] focus:outline-none focus:ring-2 focus:ring-[rgba(255,110,199,0.4)] focus:ring-offset-2 focus:ring-offset-[#0a0a0f]"
                          />
                          <label htmlFor="recurring" className="text-sm text-[rgba(255,255,255,0.7)]">
                            Recurring
                          </label>
                        </div>

                        <div className="flex items-center gap-2">
                          <input
                            type="checkbox"
                            id="reminder"
                            checked={newTask.reminder}
                            onChange={(e) => setNewTask(prev => ({ ...prev, reminder: e.target.checked }))}
                            className="w-4 h-4 rounded border-[rgba(255,110,199,0.35)] bg-[rgba(255,255,255,0.08)] checked:bg-[rgba(255,110,199,0.8)] checked:border-[rgba(255,110,199,0.8)] focus:outline-none focus:ring-2 focus:ring-[rgba(255,110,199,0.4)] focus:ring-offset-2 focus:ring-offset-[#0a0a0f]"
                          />
                          <label htmlFor="reminder" className="text-sm text-[rgba(255,255,255,0.7)]">
                            Reminder
                          </label>
                        </div>
                      </div>
                    </div>

                    <div className="flex gap-3 pt-2">
                      <button
                        onClick={handleCreateTask}
                        disabled={isLoading}
                        className="flex-1 py-3 px-6 rounded-xl font-semibold text-white bg-gradient-to-r from-[rgba(255,110,199,0.9)] to-[rgba(219,39,119,0.9)] hover:from-[rgba(255,110,199,1)] hover:to-[rgba(219,39,119,1)] focus:outline-none focus:ring-2 focus:ring-[rgba(255,110,199,0.4)] focus:ring-offset-2 focus:ring-offset-[#0a0a0f] active:scale-[0.98] transition-all duration-200 shadow-lg shadow-[rgba(255,110,199,0.3)] disabled:opacity-50 disabled:cursor-not-allowed disabled:active:scale-100"
                      >
                        {isLoading ? (
                          <span className="flex items-center justify-center gap-2">
                            <svg className="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24" aria-hidden="true">
                              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                            </svg>
                            Creating...
                          </span>
                        ) : (
                          "Create Task"
                        )}
                      </button>

                      <button
                        onClick={handleCancel}
                        disabled={isLoading}
                        className="px-6 py-3 rounded-xl font-medium text-[rgba(255,255,255,0.7)] border border-[rgba(255,110,199,0.35)] hover:text-white hover:border-[rgba(255,110,199,0.5)] focus:outline-none focus:ring-2 focus:ring-[rgba(255,110,199,0.4)] focus:ring-offset-2 focus:ring-offset-[#0a0a0f] transition-all duration-200"
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                </div>
              )}

              {!showAddTask && (
                <div className="text-center py-12">
                  <div className="w-16 h-16 bg-[rgba(255,110,199,0.1)] rounded-full flex items-center justify-center mx-auto mb-4">
                    <Plus className="w-8 h-8 text-[rgba(255,255,255,0.5)]" />
                  </div>
                  <p className="text-[rgba(255,255,255,0.5)] mb-4">No task selected</p>
                  <button
                    onClick={() => setShowAddTask(true)}
                    className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-[rgba(255,110,199,0.9)] to-[rgba(219,39,119,0.9)] text-white rounded-lg hover:from-[rgba(255,110,199,1)] hover:to-[rgba(219,39,119,1)] transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-[rgba(255,110,199,0.4)] focus:ring-offset-2 focus:ring-offset-[#0a0a0f]"
                  >
                    <Plus className="w-4 h-4" />
                    Create Your First Task
                  </button>
                </div>
              )}
            </motion.div>
          </div>
        </div>
      </div>
    </div>
    </NotificationProvider>
  );
}