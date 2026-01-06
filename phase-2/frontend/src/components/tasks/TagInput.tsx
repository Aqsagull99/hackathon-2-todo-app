"use client";

import { useState, useEffect } from "react";
import type { Tag } from "@/types";
import { api } from "@/lib/api";
import TagBadge from "./TagBadge";

interface TagInputProps {
  userId: string;
  selectedTagIds: number[];
  onTagsChange: (tagIds: number[]) => void;
}

export function TagInput({ userId, selectedTagIds, onTagsChange }: TagInputProps) {
  const [userTags, setUserTags] = useState<Tag[]>([]);
  const [isOpen, setIsOpen] = useState(false);
  const [newTagName, setNewTagName] = useState("");

  useEffect(() => {
    async function fetchTags() {
      try {
        const response = await api.getTags(userId);
        setUserTags(response.tags);
      } catch (error) {
        console.error("Failed to fetch tags:", error);
      }
    }
    fetchTags();
  }, [userId]);

  const handleTagToggle = (tagId: number) => {
    if (selectedTagIds.includes(tagId)) {
      onTagsChange(selectedTagIds.filter((id) => id !== tagId));
    } else {
      onTagsChange([...selectedTagIds, tagId]);
    }
  };

  const handleCreateTag = async () => {
    if (!newTagName.trim()) return;

    try {
      const colors = ["#EC4899", "#8B5CF6", "#10B981", "#F59E0B", "#EF4444"];
      const randomColor = colors[Math.floor(Math.random() * colors.length)];

      await api.createTag(userId, {
        name: newTagName.trim(),
        color: randomColor,
      });

      const response = await api.getTags(userId);
      setUserTags(response.tags);
      setNewTagName("");
    } catch (error) {
      console.error("Failed to create tag:", error);
    }
  };

  return (
    <div className="relative">
      <div className="flex flex-wrap gap-1">
        {selectedTagIds.map((tagId) => {
          const tag = userTags.find((t) => t.id === tagId);
          if (!tag) return null;

          return (
            <TagBadge
              key={tag.id}
              tag={tag}
              onClick={() => handleTagToggle(tag.id)}
            />
          );
        })}

        <button
          onClick={() => setIsOpen(!isOpen)}
          className="flex items-center gap-1 px-3 py-1.5 rounded-lg
            bg-white/5 border border-pink-500/30
            text-white hover:bg-white/10 transition-colors"
        >
          <svg
            className="w-4 h-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 5v14m-7-7v14"
            />
          </svg>
          <span className="text-sm">Add Tag</span>
        </button>
      </div>

      {isOpen && (
        <div className="absolute top-full left-0 mt-2 z-50
          w-72 bg-black/95 backdrop-blur-sm
          border border-pink-500/30 rounded-lg shadow-xl overflow-hidden">
          <div className="p-3">
            {/* Existing tags */}
            <div className="max-h-48 overflow-y-auto mb-3">
              {userTags.map((tag) => (
                <button
                  key={tag.id}
                  onClick={() => {
                    handleTagToggle(tag.id);
                    setIsOpen(false);
                  }}
                  className={`w-full text-left px-3 py-2 rounded-lg text-sm
                    hover:bg-pink-500/20 transition-colors
                    ${selectedTagIds.includes(tag.id) ? "bg-pink-500/30" : ""}`}
                >
                  <div className="flex items-center gap-2">
                    <span
                      className="w-2.5 h-2.5 rounded-full"
                      style={{ backgroundColor: tag.color }}
                    />
                    {tag.name}
                  </div>
                </button>
              ))}
            </div>

            {/* Create new tag */}
            <div className="border-t border-pink-500/20 pt-3">
              <div className="flex gap-2">
                <input
                  type="text"
                  value={newTagName}
                  onChange={(e) => setNewTagName(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter" && newTagName.trim()) {
                      handleCreateTag();
                    }
                  }}
                  placeholder="New tag..."
                  className="flex-1 px-3 py-2 rounded-lg bg-black/30
                    border border-pink-500/30 text-white
                    placeholder:text-gray-400 text-sm
                    focus:outline-none focus:ring-2 focus:ring-pink-500"
                />
                <button
                  onClick={handleCreateTag}
                  disabled={!newTagName.trim()}
                  className="px-4 py-2 rounded-lg bg-pink-500 text-white
                    font-medium text-sm hover:bg-pink-600
                    disabled:opacity-50 disabled:cursor-not-allowed
                    transition-colors"
                >
                  Add
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
