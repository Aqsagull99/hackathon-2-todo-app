"use client";

import { useState } from "react";

interface SortDropdownProps {
  sortBy: string;
  sortOrder: string;
  onSortChange: (sortBy: string, sortOrder: string) => void;
}

export function SortDropdown({ sortBy, sortOrder, onSortChange }: SortDropdownProps) {
  const [isOpen, setIsOpen] = useState(false);

  const sortOptions = [
    { value: "due_date", label: "Due Date" },
    { value: "priority", label: "Priority" },
    { value: "title", label: "Title" },
    { value: "created_at", label: "Created" },
  ];

  const handleSortChange = (newSortBy: string) => {
    onSortChange(newSortBy, sortOrder);
  };

  const toggleOrder = () => {
    onSortChange(sortBy, sortOrder === "asc" ? "desc" : "asc");
  };

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-4 py-2 rounded-lg
          bg-white/5 border border-pink-500/30
          text-white hover:bg-white/10 transition-colors"
      >
        <span className="text-sm">{sortOptions.find((o) => o.value === sortBy)?.label || "Sort"}</span>
        <svg
          className="w-4 h-4"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d={sortOrder === "asc" ? "M18 15l-6-6-6-6" : "M6 9l6 6 6-6"}
          />
        </svg>
      </button>

      {isOpen && (
        <div className="absolute top-full left-0 mt-2 z-50
          w-48 bg-black/90 backdrop-blur-sm
          border border-pink-500/30 rounded-lg shadow-xl overflow-hidden">
          <div className="py-1">
            {sortOptions.map((option) => (
              <button
                key={option.value}
                onClick={() => {
                  handleSortChange(option.value);
                  setIsOpen(false);
                }}
                className={`w-full text-left px-4 py-2 text-sm font-medium
                  hover:bg-pink-500/20 transition-colors
                  ${sortBy === option.value ? "bg-pink-500/10" : ""}`}
              >
                {option.label}
              </button>
            ))}
          </div>

          <div className="border-t border-pink-500/20 pt-1">
            <button
              onClick={() => {
                toggleOrder();
                setIsOpen(false);
              }}
              className="w-full text-left px-4 py-2 text-sm font-medium
                hover:bg-pink-500/20 transition-colors"
            >
              {sortOrder === "asc" ? "Ascending" : "Descending"}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
