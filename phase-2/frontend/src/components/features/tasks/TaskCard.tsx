// import React from 'react';
// import { Card, CardContent } from '@/components/ui';

// interface TaskCardProps {
//   id: string;
//   title: string;
//   description?: string;
//   dueDate?: string;
//   priority?: 'Low' | 'Medium' | 'High';
//   completed: boolean;
//   onToggle?: () => void;
//   onEdit?: () => void;
//   onDelete?: () => void;
//   isSelected?: boolean;
//   onSelect?: () => void;
// }

// const TaskCard: React.FC<TaskCardProps> = ({
//   title,
//   description,
//   dueDate,
//   priority,
//   completed,
//   onToggle,
//   onEdit,
//   onDelete,
//   isSelected,
//   onSelect
// }) => {
//   return (
//     <Card
//       className={`border border-gray-200 transition-all hover:shadow-md ${
//         completed ? 'bg-gray-50 opacity-75' : 'bg-white'
//       } ${isSelected ? 'ring-2 ring-pink-500' : ''}`}
//     >
//       <CardContent className="p-4">
//         <div className="flex items-start">
//           {onSelect && (
//             <input
//               type="checkbox"
//               checked={isSelected}
//               onChange={onSelect}
//               className="mt-1 mr-3 h-4 w-4 text-pink-600 rounded border-gray-300 focus:ring-pink-500"
//             />
//           )}

//           <div className="flex-1 min-w-0">
//             <div className="flex items-center">
//               <button
//                 onClick={onToggle}
//                 className="mr-2 focus:outline-none"
//                 aria-label={completed ? "Mark as incomplete" : "Mark as complete"}
//               >
//                 <input
//                   type="checkbox"
//                   checked={completed}
//                   onChange={onToggle}
//                   className="h-4 w-4 text-pink-600 rounded border-gray-300 focus:ring-pink-500"
//                 />
//               </button>

//               <h3
//                 className={`text-sm font-medium truncate ${
//                   completed ? 'text-gray-500 line-through' : 'text-gray-900'
//                 }`}
//               >
//                 {title}
//               </h3>
//             </div>

//             {description && (
//               <p className="mt-1 text-sm text-gray-500 truncate">{description}</p>
//             )}

//             {dueDate && (
//               <div className="mt-2 flex items-center text-xs text-gray-500">
//                 <svg className="w-3 h-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
//                   <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
//                 </svg>
//                 {new Date(dueDate).toLocaleDateString()}
//               </div>
//             )}

//             {priority && (
//               <div className={`mt-1 text-xs px-2 py-1 rounded-full ${
//                 priority === 'High' ? 'bg-red-100 text-red-800' :
//                 priority === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
//                 'bg-green-100 text-green-800'
//               }`}>
//                 {priority}
//               </div>
//             )}
//           </div>

//           <div className="flex space-x-2 ml-2">
//             <button
//               onClick={onEdit}
//               className="text-gray-400 hover:text-gray-600"
//               aria-label="Edit task"
//             >
//               <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
//                 <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
//               </svg>
//             </button>
//             <button
//               onClick={onDelete}
//               className="text-gray-400 hover:text-red-600"
//               aria-label="Delete task"
//             >
//               <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
//                 <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
//               </svg>
//             </button>
//           </div>
//         </div>
//       </CardContent>
//     </Card>
//   );
// };

// export default TaskCard;