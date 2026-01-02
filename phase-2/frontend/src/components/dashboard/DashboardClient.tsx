"use client";

import { useState } from "react";
import Sidebar from "@/components/layout/Sidebar";
import { TaskList } from "@/components/tasks/TaskList";

interface DashboardClientProps {
  userId: string;
  accessToken: string;
  userName: string | null;
}

export function DashboardClient({ userId, accessToken, userName }: DashboardClientProps) {
  const [currentFilter, setCurrentFilter] = useState<"all" | "pending" | "completed">("all");

  return (
    <div className="min-h-screen bg-[var(--background)] flex">
      {/* Sidebar */}
      <Sidebar currentFilter={currentFilter} onFilterChange={setCurrentFilter} />

      {/* Main Content */}
      <div className="flex-1">
        {/* Header */}
        <div className="border-b border-[var(--border)] bg-[var(--card)] shadow-sm">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <h1 className="text-3xl font-bold text-[var(--foreground)]">
              Welcome, {userName || "User"}!
            </h1>
            <p className="text-[var(--muted-foreground)] mt-1">
              Manage your tasks and stay productive.
            </p>
          </div>
        </div>

        {/* Task List */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <TaskList userId={userId} accessToken={accessToken} initialFilter={currentFilter} />
        </div>
      </div>
    </div>
  );
}
