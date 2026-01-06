"use client";

import { useState } from "react";

interface DateTimePickerProps {
  value: string | null;
  onChange: (value: string | null) => void;
}

export function DateTimePicker({ value, onChange }: DateTimePickerProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedDate, setSelectedDate] = useState(value ? new Date(value).toISOString().slice(0, 10) : "");
  const [selectedTime, setSelectedTime] = useState(value ? new Date(value).toISOString().slice(11, 16) : "09:00");

  const handleApply = () => {
    if (selectedDate && selectedTime) {
      const combined = `${selectedDate}T${selectedTime}`;
      onChange(combined);
      setIsOpen(false);
    }
  };

  const handleClear = () => {
    onChange(null);
    setIsOpen(false);
  };

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className={`flex items-center gap-2 px-4 py-2 rounded-lg bg-white/5
          border border-pink-500/30 text-white text-sm font-medium
          hover:bg-white/10 transition-colors ${value ? "border-pink-500" : ""}`}
      >
        <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M8 7V3a2 2 0 0 012 2v4a2 2 0 0 012-2 0 00-2.24-4.6 4.6-4.6 0 012 00l4 4a2 2 0 0 002 0zm6 7a2 2 0 0 012 2v4a2 2 0 0 012-2 0 012-2 0 00-2.24-4.6 4.6-4.6 0 002-2.24l4 4a2 2 0 0 012 0 012-2 0 00-2 2 2.24-4.6 4.6-4.6 0 012 002zm-2 2a2 2 0 0 112 2v4a2 2 0 0 112-2 0 012-2.24-4.6 4.6-4.6 0 012 00l4 4a2 2 0 0 012 0 012-2 0 00-2 2.24-4.6 4.6-4.6 0 012 00z"
          />
        </svg>
        {value ? (
          <span className="text-sm text-white">
            {new Date(value).toLocaleDateString("en-US", {
              month: "short",
              day: "numeric",
              year: "numeric",
            })} {new Date(value).toLocaleTimeString("en-US", {
              hour: "2-digit",
              minute: "2-digit",
              hour12: true,
            })}
          </span>
        ) : (
          <span className="text-sm text-gray-400">Set due date</span>
        )}

        {value && (
          <button
            onClick={handleClear}
            className="ml-2 text-gray-400 hover:text-white transition-colors"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        )}
      </button>

      {isOpen && (
        <div className="absolute top-full right-0 mt-2 z-50 bg-black/95 backdrop-blur-sm
          border border-pink-500/30 rounded-lg shadow-xl overflow-hidden p-4">
          <div className="space-y-4">
            <div>
              <label className="block text-xs text-white mb-2">Date</label>
              <input
                type="date"
                value={selectedDate}
                onChange={(e) => setSelectedDate(e.target.value)}
                className="w-full px-3 py-2 rounded-lg bg-black/30 border border-pink-500/30
                  text-white text-sm focus:outline-none focus:ring-2 focus:ring-pink-500"
              />
            </div>

            <div>
              <label className="block text-xs text-white mb-2">Time</label>
              <input
                type="time"
                value={selectedTime}
                onChange={(e) => setSelectedTime(e.target.value)}
                className="w-full px-3 py-2 rounded-lg bg-black/30 border border-pink-500/30
                  text-white text-sm focus:outline-none focus:ring-2 focus:ring-pink-500"
              />
            </div>

            <div className="flex gap-2">
              <button
                onClick={handleApply}
                className="flex-1 px-4 py-2 rounded-lg bg-pink-500 text-white
                  text-sm font-medium hover:bg-pink-600 transition-colors"
              >
                Apply
              </button>
              <button
                onClick={handleClear}
                className="flex-1 px-4 py-2 rounded-lg bg-gray-600 text-white
                  text-sm font-medium hover:bg-gray-700 transition-colors"
              >
                Clear
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
