import type { TaskPriority } from "@/types";
import { useState } from "react";

interface PrioritySelectorProps {
  value: TaskPriority;
  onChange: (priority: TaskPriority) => void;
}

export function PrioritySelector({ value, onChange }: PrioritySelectorProps) {
  const [isOpen, setIsOpen] = useState(false);

  const priorities: { value: TaskPriority; label: string; color: string }[] = [
    { value: "high", label: "High", color: "bg-red-500" },
    { value: "medium", label: "Medium", color: "bg-pink-500" },
    { value: "low", label: "Low", color: "bg-gray-500" },
  ];

  const selectedPriority = priorities.find((p) => p.value === value);

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className={`inline-flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-medium
          ${selectedPriority?.color || "bg-pink-500"} text-white
          hover:opacity-90 transition-opacity`}
      >
        <span>{selectedPriority?.label || "Medium"}</span>
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
            d="M19 9l-7 7-7-7"
          />
        </svg>
      </button>

      {isOpen && (
        <div className="absolute top-full left-0 mt-2 z-50 bg-black/90 backdrop-blur-sm
          border border-pink-500/30 rounded-lg shadow-xl overflow-hidden">
          {priorities.map((priority) => (
            <button
              key={priority.value}
              onClick={() => {
                onChange(priority.value);
                setIsOpen(false);
              }}
              className={`w-full text-left px-4 py-2 text-sm font-medium
                hover:bg-pink-500/20 transition-colors
                ${value === priority.value ? "bg-pink-500/10" : ""}`}
            >
              <div className="flex items-center gap-2">
                <span
                  className={`w-2 h-2 rounded-full ${priority.color}`}
                />
                {priority.label}
              </div>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
