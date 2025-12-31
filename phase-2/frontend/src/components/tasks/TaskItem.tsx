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
          className={`text-lg font-medium ${
            task.completed ? "line-through text-gray-500" : "text-gray-900"
          }`}
        >
          {task.title}
        </h3>
        {task.description && (
          <p className="text-sm text-gray-500 truncate">{task.description}</p>
        )}
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
