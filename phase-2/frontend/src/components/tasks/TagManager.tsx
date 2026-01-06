"use client";

import { useState, useEffect } from "react";
import type { Tag } from "@/types";
import { api } from "@/lib/api";
import { TagBadge } from "./TagBadge";

interface TagManagerProps {
  userId: string;
  isOpen: boolean;
  onClose: () => void;
}

export function TagManager({ userId, isOpen, onClose }: TagManagerProps) {
  const [userTags, setUserTags] = useState<Tag[]>([]);
  const [editingTagId, setEditingTagId] = useState<number | null>(null);
  const [editName, setEditName] = useState("");
  const [editColor, setEditColor] = useState("");

  const colors = ["#EC4899", "#8B5CF6", "#10B981", "#F59E0B", "#EF4444"];

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
  }, [userId, isOpen]);

  const handleCreateTag = async () => {
    try {
      await api.createTag(userId, {
        name: "New Tag",
        color: colors[Math.floor(Math.random() * colors.length)],
      });
      const response = await api.getTags(userId);
      setUserTags(response.tags);
    } catch (error) {
      console.error("Failed to create tag:", error);
    }
  };

  const handleUpdateTag = async () => {
    if (!editingTagId) return;

    try {
      await api.updateTag(userId, editingTagId, {
        name: editName,
        color: editColor,
      });
      const response = await api.getTags(userId);
      setUserTags(response.tags);
      setEditingTagId(null);
      setEditName("");
      setEditColor("");
    } catch (error) {
      console.error("Failed to update tag:", error);
    }
  };

  const handleDeleteTag = async (tagId: number) => {
    if (!confirm("Delete this tag? It will be removed from all tasks.")) {
      return;
    }

    try {
      await api.deleteTag(userId, tagId);
      const response = await api.getTags(userId);
      setUserTags(response.tags);
    } catch (error) {
      console.error("Failed to delete tag:", error);
    }
  };

  const startEditTag = (tag: Tag) => {
    setEditingTagId(tag.id);
    setEditName(tag.name);
    setEditColor(tag.color);
  };

  const cancelEdit = () => {
    setEditingTagId(null);
    setEditName("");
    setEditColor("");
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm">
      <div className="bg-black/90 border border-pink-500/30 rounded-2xl p-6 w-full max-w-lg shadow-2xl">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-white">Manage Tags</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white transition-colors"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div className="space-y-3 max-h-96 overflow-y-auto">
          {userTags.map((tag) => (
            <div key={tag.id} className="flex items-center gap-3 bg-white/5 rounded-lg p-3">
              {editingTagId === tag.id ? (
                <>
                  <input
                    type="text"
                    value={editName}
                    onChange={(e) => setEditName(e.target.value)}
                    className="flex-1 px-3 py-2 rounded-lg bg-black/30 border border-pink-500/30 text-white text-sm focus:outline-none focus:ring-2 focus:ring-pink-500"
                  />
                  <div className="flex gap-1">
                    {colors.map((color) => (
                      <button
                        key={color}
                        onClick={() => setEditColor(color)}
                        className={`w-6 h-6 rounded-full border-2 ${
                          editColor === color ? "border-pink-500" : "border-transparent"
                        }`}
                        style={{ backgroundColor: color }}
                      />
                    ))}
                  </div>
                  <div className="flex gap-2">
                    <button
                      onClick={handleUpdateTag}
                      className="px-3 py-1.5 rounded-lg bg-pink-500 text-white text-sm font-medium hover:bg-pink-600 transition-colors"
                    >
                      Save
                    </button>
                    <button
                      onClick={cancelEdit}
                      className="px-3 py-1.5 rounded-lg bg-gray-600 text-white text-sm font-medium hover:bg-gray-700 transition-colors"
                    >
                      Cancel
                    </button>
                  </div>
                </>
              ) : (
                <>
                  <TagBadge tag={tag} />
                  <span className="flex-1 text-white text-sm">{tag.name}</span>
                  <div className="flex gap-2">
                    <button
                      onClick={() => startEditTag(tag)}
                      className="text-gray-400 hover:text-white transition-colors"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 4H4a2 2 0 0 0 0-2V14a2 2 0 0 0 2 2h7m7 7v-7m-7 7h-2M12 21V7" />
                      </svg>
                    </button>
                    <button
                      onClick={() => handleDeleteTag(tag.id)}
                      className="text-gray-400 hover:text-red-400 transition-colors"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0 0 18 7v3a2 2 0 0 1-2.929V7a2 2 0 0 0-3.414-2.929L12 12l4.736-4.866A2 2 0 0 0 5-1.414V7a2 2 0 0 0-1.929-1.414z" />
                      </svg>
                    </button>
                  </div>
                </>
              )}
            </div>
          ))}

          {userTags.length === 0 && (
            <div className="text-center py-12">
              <p className="text-gray-400 text-lg">No tags yet</p>
              <button
                onClick={handleCreateTag}
                className="mt-4 px-6 py-2.5 rounded-lg bg-pink-500 text-white font-medium hover:bg-pink-600 transition-colors"
              >
                Create First Tag
              </button>
            </div>
          )}
        </div>

        <div className="mt-6 flex justify-end">
          <button
            onClick={handleCreateTag}
            className="px-6 py-2.5 rounded-lg bg-pink-500 text-white font-medium hover:bg-pink-600 transition-colors"
          >
            + New Tag
          </button>
        </div>
      </div>
    </div>
  );
}
