import type { TaskPriority } from "@/types";

interface PriorityBadgeProps {
  priority: TaskPriority;
}

export function PriorityBadge({ priority }: PriorityBadgeProps) {
  const config = {
    high: {
      bg: "bg-red-500",
      label: "High",
      icon: "!",
    },
    medium: {
      bg: "bg-pink-500",
      label: "Medium",
      icon: null,
    },
    low: {
      bg: "bg-gray-500",
      label: "Low",
      icon: null,
    },
  }[priority];

  return (
    <span
      className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full
        text-xs font-semibold text-white ${config.bg}`}
    >
      {config.icon && <span className="font-bold">{config.icon}</span>}
      {config.label}
    </span>
  );
}
