"use client";

import { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { api } from "@/lib/api";
import type { Reminder, ReminderStatus } from "@/types";

interface NotificationContextType {
  permission: NotificationPermission;
  requestPermission: () => Promise<void>;
  reminders: Reminder[];
  scheduleReminder: (taskId: number, dueTime: string) => Promise<void>;
  snoozeReminder: (reminderId: number, minutes: number) => Promise<void>;
  dismissReminder: (reminderId: number) => Promise<void>;
}

const NotificationContext = createContext<NotificationContextType | null>(null);

export function useNotifications() {
  const context = useContext(NotificationContext);
  if (!context) {
    throw new Error("useNotifications must be used within NotificationProvider");
  }
  return context;
}

interface NotificationProviderProps {
  children: ReactNode;
  userId: string;
}

export function NotificationProvider({ children, userId }: NotificationProviderProps) {
  const [permission, setPermission] = useState<NotificationPermission>("default");
  const [reminders, setReminders] = useState<Reminder[]>([]);

  // Check notification permission on mount
  useEffect(() => {
    if ("Notification" in window) {
      setPermission(Notification.permission);
    }
  }, []);

  const requestPermission = async () => {
    if ("Notification" in window) {
      const result = await Notification.requestPermission();
      setPermission(result);
    }
  };

  const scheduleReminder = async (taskId: number, dueTime: string) => {
    try {
      await api.createReminder(userId, taskId, dueTime);
      // Reminders are handled by the frontend with browser notifications
      // Backend stores them for reference
    } catch (error) {
      console.error("Failed to schedule reminder:", error);
      throw error;
    }
  };

  const snoozeReminder = async (reminderId: number, minutes: number) => {
    try {
      await api.snoozeReminder(userId, reminderId, minutes);
      // Schedule new notification
      const reminder = reminders.find((r) => r.id === reminderId);
      if (reminder) {
        const snoozedUntil = new Date(reminder.due_time);
        snoozedUntil.setMinutes(snoozedUntil.getMinutes() + minutes);

        // Schedule browser notification
        if (permission === "granted") {
          const timeout = snoozedUntil.getTime() - Date.now();
          if (timeout > 0) {
            setTimeout(() => {
              new Notification(`Task reminder snoozed`, {
                body: `Snoozed for ${minutes} minutes`,
                tag: "task-reminder",
              });
            }, timeout);
          }
        }
      }
    } catch (error) {
      console.error("Failed to snooze reminder:", error);
      throw error;
    }
  };

  const dismissReminder = async (reminderId: number) => {
    try {
      await api.dismissReminder(userId, reminderId);
      setReminders((prev) => prev.filter((r) => r.id !== reminderId));
    } catch (error) {
      console.error("Failed to dismiss reminder:", error);
      throw error;
    }
  };

  return (
    <NotificationContext.Provider
      value={{
        permission,
        requestPermission,
        reminders,
        scheduleReminder,
        snoozeReminder,
        dismissReminder,
      }}
    >
      {children}
    </NotificationContext.Provider>
  );
}
