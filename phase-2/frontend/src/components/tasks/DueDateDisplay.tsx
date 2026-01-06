import type { Task } from "@/types";
import { useMemo } from "react";

interface DueDateDisplayProps {
  task: Task;
}

export function DueDateDisplay({ task }: DueDateDisplayProps) {
  const dueDate = useMemo(() => {
    if (!task.due_date) return null;
    return new Date(task.due_date);
  }, [task.due_date]);

  const statusInfo = useMemo(() => {
    if (!dueDate) return null;

    const now = new Date();
    const hoursDiff = (dueDate.getTime() - now.getTime()) / (1000 * 60 * 60);
    const daysDiff = hoursDiff / 24;

    if (task.completed) {
      return { text: "Completed", color: "text-gray-400" };
    }

    if (daysDiff < 0) {
      return { text: `Overdue by ${Math.abs(Math.floor(daysDiff))} days`, color: "text-red-400" };
    }

    if (daysDiff < 1) {
      return { text: "Due today", color: "text-yellow-400" };
    }

    if (daysDiff < 7) {
      return { text: `Due in ${Math.floor(daysDiff)} days`, color: "text-pink-400" };
    }

    return { text: dueDate.toLocaleDateString("en-US", { month: "short", day: "numeric" }), color: "text-gray-300" };
  }, [dueDate, task.completed]);

  if (!dueDate) return null;

  const info = statusInfo!;

  return (
    <div className="flex items-center gap-1 text-xs text-gray-400">
      <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M8 2v4a6 6 0 016 6v12a6 6 0 01-6-6H8z M6 14l4-4 4 4"
        />
      </svg>
      <span className={info.color}>{info.text}</span>
    </div>
  );
}
