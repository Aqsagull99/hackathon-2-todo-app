"use client";

import React from 'react';
import { ListTodo, CheckCircle2, List } from 'lucide-react';
import { cn } from "@/lib/utils";

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
    <div className={cn("w-64 bg-[rgba(255,110,199,0.12)] border-r border-[rgba(255,110,199,0.35)] backdrop-blur-24 flex flex-col", className)}>
      <div className="p-6 border-b border-[rgba(255,110,199,0.35)]">
        <h2 className="text-xl font-bold text-white">
          Todo<span className="text-[#db2777]">Pink</span>
        </h2>
        <p className="text-xs text-[rgba(255,255,255,0.5)] mt-1">Task Management</p>
      </div>

      <nav className="flex-1 px-3 py-4 space-y-1">
        {filterOptions.map(({ value, label, icon: Icon }) => {
          const isActive = currentFilter === value;
          return (
            <button
              key={value}
              onClick={() => onFilterChange?.(value)}
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
        <div className="text-center text-xs text-[rgba(255,255,255,0.5)]">
          <p>TodoPink v1.0</p>
          <p className="mt-1">Stay Organized</p>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;