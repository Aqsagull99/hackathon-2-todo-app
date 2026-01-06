import type { Tag } from "@/types";

interface TagBadgeProps {
  tag: Tag;
  onClick?: () => void;
}

export function TagBadge({ tag, onClick }: TagBadgeProps) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium
        border transition-all hover:scale-105 active:scale-95`}
      style={{
        backgroundColor: tag.color,
        borderColor: `${tag.color}40`,
        color: getContrastColor(tag.color),
      }}
    >
      {tag.name}
    </button>
  );
}

function getContrastColor(hexColor: string): string {
  const hex = hexColor.replace("#", "");
  const r = parseInt(hex.substring(0, 2), 16);
  const g = parseInt(hex.substring(2, 4), 16);
  const b = parseInt(hex.substring(4, 6), 16);
  const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
  return luminance > 0.5 ? "#000000" : "#FFFFFF";
}

export default TagBadge;
