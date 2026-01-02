"use client";

import React from 'react';
import { ListTodo, CheckCircle2, List } from 'lucide-react';

interface SidebarProps {
  className?: string;
  currentFilter?: "all" | "pending" | "completed";
  onFilterChange?: (filter: "all" | "pending" | "completed") => void;
}

const Sidebar: React.FC<SidebarProps> = ({
  className = '',
  currentFilter = "all",
  onFilterChange
}) => {
  const filterOptions = [
    { value: "all" as const, label: "All Tasks", icon: List },
    { value: "pending" as const, label: "Active Tasks", icon: ListTodo },
    { value: "completed" as const, label: "Completed", icon: CheckCircle2 },
  ];

  return (
    <div className={`w-64 bg-[var(--card)] border-r border-[var(--border)] flex flex-col ${className}`}>
      <div className="p-6 border-b border-[var(--border)]">
        <h2 className="text-xl font-bold text-[var(--foreground)]">
          Todo<span className="text-[var(--primary)]">Pink</span>
        </h2>
        <p className="text-xs text-[var(--muted-foreground)] mt-1">Task Management</p>
      </div>

      <nav className="flex-1 px-3 py-4 space-y-1">
        {filterOptions.map(({ value, label, icon: Icon }) => {
          const isActive = currentFilter === value;
          return (
            <button
              key={value}
              onClick={() => onFilterChange?.(value)}
              className={`w-full group flex items-center px-4 py-3 text-sm font-medium rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-[var(--primary)] focus:ring-offset-2 ${
                isActive
                  ? "bg-[var(--primary)] text-[var(--primary-foreground)]"
                  : "text-[var(--foreground)] hover:bg-[var(--secondary)]"
              }`}
              aria-label={`Filter: ${label}`}
              aria-pressed={isActive}
            >
              <Icon className="mr-3 h-5 w-5" />
              {label}
            </button>
          );
        })}
      </nav>

      <div className="p-4 border-t border-[var(--border)] bg-[var(--secondary)]">
        <div className="text-center text-xs text-[var(--muted-foreground)]">
          <p>TodoPink v1.0</p>
          <p className="mt-1">Stay Organized</p>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;