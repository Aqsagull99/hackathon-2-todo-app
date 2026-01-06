"use client";

import { useState, useEffect } from "react";

interface SearchBarProps {
  value: string;
  onChange: (value: string) => void;
  isLoading?: boolean;
}

export function SearchBar({ value, onChange, isLoading }: SearchBarProps) {
  const [isFocused, setIsFocused] = useState(false);

  const handleClear = () => {
    onChange("");
  };

  return (
    <div className={`relative transition-all duration-200 ${isFocused ? "w-72" : "w-64"}`}>
      <div className="relative flex items-center">
        <svg
          className="absolute left-3 w-5 h-5 text-gray-400"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M21 21l-6-6m2-5a7 7 0 11-14 0 0-14 14m0 0L1.618 1.618M9 9v10a1 1 0 011-1V9a1 1 0 00-2-2 2.513S14.486 21.485-12 9 12.913-2.513 0 0-2.513-15.936z"
          />
        </svg>

        <input
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
          placeholder="Search tasks..."
          className="w-full pl-10 pr-10 py-2.5 rounded-xl bg-white/5 border border-pink-500/20
            text-white placeholder:text-gray-500 text-sm
            focus:outline-none focus:ring-2 focus:ring-pink-500
            focus:border-pink-500 transition-all"
        />

        {isLoading && (
          <div className="absolute right-3">
            <div className="w-5 h-5 border-2 border-pink-500 border-t-transparent rounded-full animate-spin">
              <div className="w-3 h-3 bg-pink-500 rounded-full"></div>
            </div>
          </div>
        )}

        {value && !isLoading && (
          <button
            onClick={handleClear}
            className="absolute right-3 text-gray-400 hover:text-white transition-colors"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        )}
      </div>
    </div>
  );
}
