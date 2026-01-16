"use client";

import { useState } from "react";
import type { Task } from "@/types";
import { Button } from "@/components/ui/Button";

interface TaskItemProps {
  task: Task;
  onToggle: (taskId: number) => Promise<void>;
  onDelete: (taskId: number) => Promise<void>;
  onEdit: (task: Task) => void;
}

export function TaskItem({ task, onToggle, onDelete, onEdit }: TaskItemProps) {
  const [isLoading, setIsLoading] = useState(false);

  const handleToggle = async () => {
    setIsLoading(true);
    try {
      await onToggle(task.id);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!confirm("Are you sure you want to delete this task?")) return;
    setIsLoading(true);
    try {
      await onDelete(task.id);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div
      className={`flex items-center gap-4 p-4 border-b border-gray-100 hover:bg-gray-50 transition-colors ${
        task.completed ? "opacity-60" : ""
      }`}
    >
      {/* Checkbox */}
      <button
        onClick={handleToggle}
        disabled={isLoading}
        className={`w-6 h-6 rounded-full border-2 flex items-center justify-center transition-colors ${
          task.completed
            ? "bg-green-500 border-green-500 text-white"
            : "border-gray-300 hover:border-green-500"
        }`}
      >
        {task.completed && (
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
        )}
      </button>

      {/* Task Content */}
      <div className="flex-1 min-w-0">
        <h3
          className={`text-lg font-semibold ${
            task.completed ? "line-through text-gray-400" : "text-gray-900"
          }`}
        >
          {task.title}
        </h3>
        {task.description && (
          <p className="text-sm text-gray-600 mt-1.5 mb-2">{task.description}</p>
        )}

        {/* Extended Fields: Priority, Due Date, Recurrence, Reminder, Tags with Distinct Colors */}
        <div className="flex flex-wrap gap-2.5 mt-3">
          {/* Priority Badge - Prominent with Icon */}
          {task.priority && (
            <div className={`inline-flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-lg font-semibold shadow-sm ${
              task.priority === "high" 
                ? "bg-red-50 text-red-700 border border-red-200" 
                : task.priority === "low"
                ? "bg-blue-50 text-blue-700 border border-blue-200"
                : "bg-amber-50 text-amber-700 border border-amber-200"
            }`}>
              {task.priority === "high" && (
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                </svg>
              )}
              {task.priority === "low" && (
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clipRule="evenodd" />
                </svg>
              )}
              <span className="capitalize">{task.priority}</span>
            </div>
          )}

          {/* Due Date Badge - Green with Calendar Icon */}
          {task.due_date && (
            <div className="inline-flex items-center gap-1.5 text-xs bg-emerald-50 text-emerald-700 border border-emerald-200 px-3 py-1.5 rounded-lg font-semibold shadow-sm">
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v2h16V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h12a1 1 0 100-2H6z" clipRule="evenodd" />
              </svg>
              {new Date(task.due_date).toLocaleDateString('en-US', { 
                month: 'short', 
                day: 'numeric',
                year: new Date(task.due_date).getFullYear() !== new Date().getFullYear() ? 'numeric' : undefined
              })}
            </div>
          )}

          {/* Recurrence Pattern - Purple with Repeat Icon */}
          {task.recurrence_pattern && (
            <div className="inline-flex items-center gap-1.5 text-xs bg-purple-50 text-purple-700 border border-purple-200 px-3 py-1.5 rounded-lg font-semibold shadow-sm">
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 1011.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 105.199 7.03V4a1 1 0 01-1-1zm5 9a1 1 0 100-2 1 1 0 000 2z" clipRule="evenodd" />
              </svg>
              <span className="capitalize">{task.recurrence_pattern}</span>
            </div>
          )}

          {/* Reminder - Orange with Clock Icon */}
          {task.reminder && (
            <div className="inline-flex items-center gap-1.5 text-xs bg-orange-50 text-orange-700 border border-orange-200 px-3 py-1.5 rounded-lg font-semibold shadow-sm">
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v3.586L7.707 9.293a1 1 0 00-1.414 1.414l3 3a1 1 0 001.414 0l3-3a1 1 0 00-1.414-1.414L11 10.586V7z" clipRule="evenodd" />
              </svg>
              {task.reminder}
            </div>
          )}

          {/* Tags - Teal with Tag Icon */}
          {task.tags && task.tags.length > 0 && task.tags.map((tag, i) => (
            <div key={i} className="inline-flex items-center gap-1.5 text-xs bg-teal-50 text-teal-700 border border-teal-200 px-3 py-1.5 rounded-lg font-semibold shadow-sm">
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M17.778 8.222c-4.296-4.296-11.26-4.296-15.556 0A11.323 11.323 0 001.945 10.461c-.187.262-.289.56-.289.883 0 .823.671 1.494 1.494 1.494.323 0 .621-.102.883-.289 2.04-1.294 4.747-2.066 7.644-2.066 2.897 0 5.604.772 7.644 2.066.262.187.56.289.883.289.823 0 1.494-.671 1.494-1.494 0-.323-.102-.621-.289-.883a11.322 11.322 0 00-1.277-2.162zm0 3.556c-3.057-3.057-8.02-3.057-11.077 0a8.227 8.227 0 00-1.148 1.579c-.186.262-.288.56-.288.882 0 .823.671 1.495 1.494 1.495.322 0 .62-.103.882-.288 1.837-1.167 4.084-1.862 6.57-1.862s4.733.695 6.57 1.862c.262.185.56.288.882.288.823 0 1.494-.672 1.494-1.495 0-.322-.102-.62-.288-.882a8.227 8.227 0 00-1.148-1.579z" clipRule="evenodd" />
              </svg>
              {typeof tag === 'string' ? tag : tag.name}
            </div>
          ))}
        </div>
      </div>

      {/* Actions */}
      <div className="flex items-center gap-2">
        <Button variant="ghost" size="sm" onClick={() => onEdit(task)}>
          Edit
        </Button>
        <Button variant="danger" size="sm" onClick={handleDelete} isLoading={isLoading}>
          Delete
        </Button>
      </div>
    </div>
  );
}
