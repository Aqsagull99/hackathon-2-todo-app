"use client";

import { useState, useEffect } from "react";

interface FilterBarProps {
  status: string;
  priority: string | null;
  dueDateRange: string;
  onStatusChange: (status: string) => void;
  onPriorityChange: (priority: string | null) => void;
  onDueDateChange: (range: string) => void;
  onClear: () => void;
}

export function FilterBar({
  status,
  priority,
  dueDateRange,
  onStatusChange,
  onPriorityChange,
  onDueDateChange,
  onClear,
}: FilterBarProps) {
  return (
    <div className="flex flex-wrap items-center gap-2">
      {/* Status Filter */}
      <select
        value={status}
        onChange={(e) => onStatusChange(e.target.value)}
        className="px-4 py-2 rounded-lg bg-white/5 border border-pink-500/20
          text-white text-sm focus:outline-none focus:ring-2 focus:ring-pink-500"
      >
        <option value="all">All Tasks</option>
        <option value="pending">Pending</option>
        <option value="completed">Completed</option>
      </select>

      {/* Priority Filter */}
      <select
        value={priority || ""}
        onChange={(e) => onPriorityChange(e.target.value || null)}
        className="px-4 py-2 rounded-lg bg-white/5 border border-pink-500/20
          text-white text-sm focus:outline-none focus:ring-2 focus:ring-pink-500"
      >
        <option value="">All Priorities</option>
        <option value="high">High</option>
        <option value="medium">Medium</option>
        <option value="low">Low</option>
      </select>

      {/* Due Date Filter */}
      <select
        value={dueDateRange}
        onChange={(e) => onDueDateChange(e.target.value)}
        className="px-4 py-2 rounded-lg bg-white/5 border border-pink-500/20
          text-white text-sm focus:outline-none focus:ring-2 focus:ring-pink-500"
      >
        <option value="all">All Dates</option>
        <option value="today">Today</option>
        <option value="thisWeek">This Week</option>
        <option value="thisMonth">This Month</option>
        <option value="overdue">Overdue</option>
      </select>

      {/* Clear Filters */}
      <button
        onClick={onClear}
        className="px-4 py-2 rounded-lg bg-pink-500 text-white
          text-sm font-medium hover:bg-pink-600 transition-colors"
      >
        Clear
      </button>
    </div>
  );
}
