/**
 * Task Filters Component - Phase V
 * Provides filtering and sorting controls for task list
 * [Task]: T023
 */

import React from 'react';

interface TaskFiltersProps {
  onFilterChange: (filters: TaskFilters) => void;
  currentFilters: TaskFilters;
}

export interface TaskFilters {
  status?: 'all' | 'pending' | 'completed';
  priority?: 'high' | 'medium' | 'low' | null;
  searchQuery?: string;
  sortBy?: 'created_at' | 'due_date' | 'priority' | 'title';
  sortOrder?: 'asc' | 'desc';
}

export default function TaskFilters({ onFilterChange, currentFilters }: TaskFiltersProps) {
  return (
    <div className="flex gap-4 p-4 bg-black/30 rounded-lg">
      {/* Status Filter */}
      <select
        value={currentFilters.status || 'all'}
        onChange={(e) => onFilterChange({ ...currentFilters, status: e.target.value as any })}
        className="px-3 py-2 bg-black/50 border border-pink-500/30 rounded-lg text-white"
      >
        <option value="all">All Tasks</option>
        <option value="pending">Pending</option>
        <option value="completed">Completed</option>
      </select>

      {/* Priority Filter */}
      <select
        value={currentFilters.priority || ''}
        onChange={(e) => onFilterChange({ ...currentFilters, priority: e.target.value as any || null })}
        className="px-3 py-2 bg-black/50 border border-pink-500/30 rounded-lg text-white"
      >
        <option value="">All Priorities</option>
        <option value="high">🔴 High</option>
        <option value="medium">🟡 Medium</option>
        <option value="low">🟢 Low</option>
      </select>

      {/* Sort By */}
      <select
        value={currentFilters.sortBy || 'created_at'}
        onChange={(e) => onFilterChange({ ...currentFilters, sortBy: e.target.value as any })}
        className="px-3 py-2 bg-black/50 border border-pink-500/30 rounded-lg text-white"
      >
        <option value="created_at">Recently Created</option>
        <option value="due_date">Due Date</option>
        <option value="priority">Priority</option>
        <option value="title">Title</option>
      </select>

      {/* Search */}
      <input
        type="text"
        placeholder="Search tasks..."
        value={currentFilters.searchQuery || ''}
        onChange={(e) => onFilterChange({ ...currentFilters, searchQuery: e.target.value })}
        className="px-3 py-2 bg-black/50 border border-pink-500/30 rounded-lg text-white flex-1"
      />
    </div>
  );
}
