"use client";

import { FormEvent, useEffect, useMemo, useState } from "react";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import type {
  Task,
  TaskExtendedCreate,
  TaskExtendedUpdate,
  TaskPriority,
  RecurrencePattern,
} from "@/types";
import { PrioritySelector } from "./PrioritySelector";
import { TagInput } from "./TagInput";
import { RecurringConfig } from "./RecurringConfig";
import { DateTimePicker } from "./DateTimePicker";
import { useNotifications } from "@/lib/contexts/NotificationContext";

interface TaskFormProps {
  task?: Task | null;
  userId: string;
  onSubmit: (data: TaskExtendedCreate | TaskExtendedUpdate) => Promise<Task>;
  onCancel?: () => void;
}

export function TaskForm({ task, userId, onSubmit, onCancel }: TaskFormProps) {
  const [title, setTitle] = useState(task?.title || "");
  const [description, setDescription] = useState(task?.description || "");
  const [priority, setPriority] = useState<TaskPriority>(task?.priority || "medium");
  const [selectedTagIds, setSelectedTagIds] = useState<number[]>(task?.tags?.map((t) => t.id) || []);
  const [dueDate, setDueDate] = useState<string | null>(task?.due_date || null);
  const [recurrence, setRecurrence] = useState<RecurrencePattern | null>(task?.recurrence_pattern || null);
  const [reminderEnabled, setReminderEnabled] = useState<boolean>(!!task?.due_date);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string>("");

  const { permission, requestPermission, scheduleReminder } = useNotifications();
  const isEdit = Boolean(task);
  const timeZone = useMemo(() => Intl.DateTimeFormat().resolvedOptions().timeZone, []);

  useEffect(() => {
    if (!task) {
      setPriority("medium");
      setSelectedTagIds([]);
      setDueDate(null);
      setRecurrence(null);
      setReminderEnabled(false);
      return;
    }

    setTitle(task.title);
    setDescription(task.description || "");
    setPriority(task.priority);
    setSelectedTagIds(task.tags?.map((t) => t.id) || []);
    setDueDate(task.due_date || null);
    setRecurrence(task.recurrence_pattern || null);
    setReminderEnabled(Boolean(task.due_date));
  }, [task]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");

    if (!title.trim()) {
      setError("Title is required");
      return;
    }

    if (recurrence && !dueDate) {
      setError("Recurring tasks require a due date");
      return;
    }

    setIsLoading(true);
    try {
      const payload: TaskExtendedCreate | TaskExtendedUpdate = {
        title: title.trim(),
        description: description.trim() || null,
        priority,
        due_date: dueDate || undefined,
        due_date_tz: dueDate ? timeZone : undefined,
        recurrence_pattern: recurrence || undefined,
        tag_ids: selectedTagIds,
      };

      const savedTask = await onSubmit(payload);

      if (reminderEnabled && dueDate) {
        if (permission === "default") {
          await requestPermission();
        }
        if (permission === "granted") {
          await scheduleReminder(savedTask.id, dueDate);
        }
      }

      if (!isEdit) {
        setTitle("");
        setDescription("");
        setPriority("medium");
        setSelectedTagIds([]);
        setDueDate(null);
        setRecurrence(null);
        setReminderEnabled(false);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setIsLoading(false);
    }
  };

  const toggleReminder = () => {
    if (!dueDate) {
      setError("Set a due date before enabling reminders");
      return;
    }
    setReminderEnabled((prev) => !prev);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {error && (
        <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
          {error}
        </div>
      )}

      <Input
        label="Title"
        name="title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Enter task title..."
        required
        maxLength={200}
      />

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Description (optional)
        </label>
        <textarea
          name="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Add more details..."
          rows={3}
          maxLength={1000}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-pink-500"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Priority</label>
          <PrioritySelector value={priority} onChange={setPriority} />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Tags</label>
          <TagInput userId={userId} selectedTagIds={selectedTagIds} onTagsChange={setSelectedTagIds} />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Due Date</label>
          <DateTimePicker value={dueDate} onChange={setDueDate} />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Recurring</label>
          <RecurringConfig value={recurrence} onChange={setRecurrence} />
        </div>
      </div>

      <div className="flex flex-wrap items-center gap-3">
        <button
          type="button"
          onClick={toggleReminder}
          className={`px-4 py-2 rounded-lg text-sm font-medium border transition-colors ${
            reminderEnabled ? "bg-pink-500 text-white border-pink-500" : "border-gray-300 text-gray-600"
          }`}
        >
          {reminderEnabled ? "Reminders Enabled" : "Enable Reminder"}
        </button>
        <span className="text-sm text-gray-500">
          {dueDate ? new Date(dueDate).toLocaleString() : "No due date set"}
        </span>
        {permission === "denied" && (
          <span className="text-xs text-red-500">Browser notifications are blocked.</span>
        )}
      </div>

      <div className="flex gap-3">
        <Button type="submit" isLoading={isLoading} disabled={isLoading}>
          {isEdit ? "Save Changes" : "Create Task"}
        </Button>
        {onCancel && (
          <Button type="button" variant="secondary" onClick={onCancel} disabled={isLoading}>
            Cancel
          </Button>
        )}
      </div>
    </form>
  );
}
