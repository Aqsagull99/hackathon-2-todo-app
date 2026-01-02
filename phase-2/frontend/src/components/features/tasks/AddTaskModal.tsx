// "use client";

// import { useState } from "react";
// import { Input } from "@/components/ui/Input";
// import { Button } from "@/components/ui/Button";

// interface Task {
//   id: number;
//   title: string;
//   description?: string;
//   completed: boolean;
//   created_at: string;
// }

// interface AddTaskModalProps {
//   isOpen: boolean;
//   onClose: () => void;
//   onSubmit: (data: { title: string; description: string }) => void;
//   initialData?: Task;
//   isLoading?: boolean;
// }

// export function AddTaskModal({
//   isOpen,
//   onClose,
//   onSubmit,
//   initialData,
//   isLoading = false,
// }: AddTaskModalProps) {
//   const [title, setTitle] = useState(initialData?.title || "");
//   const [description, setDescription] = useState(initialData?.description || "");

//   if (!isOpen) return null;

//   const handleSubmit = (e: React.FormEvent) => {
//     e.preventDefault();
//     if (!title.trim()) return;
//     onSubmit({ title: title.trim(), description: description.trim() });
//   };

//   const handleKeyDown = (e: React.KeyboardEvent) => {
//     if (e.key === "Escape") {
//       onClose();
//     }
//   };

//   return (
//     <div
//       className="fixed inset-0 z-50 flex items-center justify-center"
//       role="dialog"
//       aria-modal="true"
//       aria-labelledby="modal-title"
//     >
//       {/* Backdrop */}
//       <div
//         className="absolute inset-0 bg-black/30 backdrop-blur-sm transition-opacity"
//         onClick={onClose}
//         aria-hidden="true"
//       />

//       {/* Modal */}
//       <div
//         className="relative bg-white rounded-xl shadow-xl w-full max-w-md mx-4 overflow-hidden focus:outline-none"
//         onKeyDown={handleKeyDown}
//       >
//         {/* Header */}
//         <div className="flex items-center justify-between px-6 py-4 border-b border-[var(--border)] bg-[var(--secondary)]">
//           <h2
//             id="modal-title"
//             className="text-xl font-semibold text-[var(--foreground)]"
//           >
//             {initialData ? "Edit Task" : "Add New Task"}
//           </h2>
//           <button
//             type="button"
//             onClick={onClose}
//             className="p-2 rounded-lg text-[var(--muted-foreground)] hover:bg-[var(--accent)] hover:text-[var(--primary)] transition-colors focus:outline-none focus:ring-2 focus:ring-[var(--primary)] focus:ring-offset-2"
//             aria-label="Close modal"
//           >
//             <svg
//               className="w-5 h-5"
//               fill="none"
//               viewBox="0 0 24 24"
//               stroke="currentColor"
//               aria-hidden="true"
//             >
//               <path
//                 strokeLinecap="round"
//                 strokeLinejoin="round"
//                 strokeWidth={2}
//                 d="M6 18L18 6M6 6l12 12"
//               />
//             </svg>
//           </button>
//         </div>

//         {/* Form */}
//         <form onSubmit={handleSubmit} className="p-6 space-y-4">
//           <Input
//             id="task-title"
//             label="Title"
//             type="text"
//             value={title}
//             onChange={(e) => setTitle(e.target.value)}
//             placeholder="What needs to be done?"
//             required
//             autoFocus
//             aria-required="true"
//             disabled={isLoading}
//           />

//           <div className="w-full">
//             <label
//               htmlFor="task-description"
//               className="block text-sm font-medium text-[var(--foreground)] mb-1"
//             >
//               Description (optional)
//             </label>
//             <textarea
//               id="task-description"
//               value={description}
//               onChange={(e) => setDescription(e.target.value)}
//               placeholder="Add more details..."
//               rows={3}
//               className="w-full px-3 py-2 border border-[var(--input)] rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-[var(--primary)] focus:border-[var(--primary)] disabled:bg-[var(--secondary)] disabled:cursor-not-allowed resize-none"
//               disabled={isLoading}
//             />
//           </div>

//           {/* Actions */}
//           <div className="flex items-center justify-end gap-3 pt-4">
//             <Button
//               type="button"
//               variant="ghost"
//               onClick={onClose}
//               disabled={isLoading}
//             >
//               Cancel
//             </Button>
//             <Button
//               type="submit"
//               isLoading={isLoading}
//               disabled={!title.trim()}
//             >
//               {initialData ? "Save Changes" : "Create Task"}
//             </Button>
//           </div>
//         </form>
//       </div>
//     </div>
//   );
// }
