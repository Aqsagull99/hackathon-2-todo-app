"use client";

import type { RecurrencePattern } from "@/types";
import { useState } from "react";

interface RecurringConfigProps {
  value: RecurrencePattern | null;
  onChange: (pattern: RecurrencePattern | null) => void;
}

export function RecurringConfig({ value, onChange }: RecurringConfigProps) {
  const [isOpen, setIsOpen] = useState(false);

  const patterns = [
    { value: null as RecurrencePattern | null, label: "Does not repeat" },
    { value: "daily", label: "Daily" },
    { value: "weekly", label: "Weekly" },
    { value: "monthly", label: "Monthly" },
  ];

  const selectedPattern = patterns.find((p) => p.value === value);

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-4 py-2 rounded-lg
          bg-white/5 border border-pink-500/30
          text-white hover:bg-white/10 transition-colors"
      >
        <svg
          className="w-4 h-4 text-gray-400"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M4 4v5h.582m0 0a2 2 0 012-2v7a2 2 0 01-2-2 2 0 012v-3a2 2 0 01-2-2-2 0 00-2h5.172a2 2 0 00 2-2 0 0-2h3.614a2 2 0 00 2 2 0 00H12z"
          />
        </svg>
        <span className="text-sm">
          {selectedPattern?.label || "Does not repeat"}
        </span>
        <svg
          className="w-4 h-4 text-gray-400"
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
        <div className="absolute top-full left-0 mt-2 z-50
          w-48 bg-black/90 backdrop-blur-sm
          border border-pink-500/30 rounded-lg shadow-xl overflow-hidden">
          {patterns.map((pattern) => (
            <button
              key={pattern.value || "none"}
              onClick={() => {
                onChange(pattern.value);
                setIsOpen(false);
              }}
              className={`w-full text-left px-4 py-2 text-sm font-medium
                hover:bg-pink-500/20 transition-colors
                ${value === pattern.value ? "bg-pink-500/10" : ""}`}
            >
              {pattern.label}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
