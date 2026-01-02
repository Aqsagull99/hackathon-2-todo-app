// import React, { useState } from 'react';
// import TaskCard from './TaskCard';
// import { Card } from '@/components/ui';

// interface Task {
//   id: string;
//   title: string;
//   description?: string;
//   dueDate?: string;
//   priority: 'Low' | 'Medium' | 'High';
//   completed: boolean;
// }

// interface TaskListProps {
//   tasks: Task[];
//   onTaskToggle?: (id: string) => void;
//   onTaskEdit?: (id: string) => void;
//   onTaskDelete?: (id: string) => void;
//   showCompleted?: boolean;
//   title?: string;
// }

// const TaskList: React.FC<TaskListProps> = ({
//   tasks,
//   onTaskToggle,
//   onTaskEdit,
//   onTaskDelete,
//   showCompleted = true,
//   title = 'Tasks'
// }) => {
//   const [selectedTaskIds, setSelectedTaskIds] = useState<string[]>([]);

//   const filteredTasks = showCompleted
//     ? tasks
//     : tasks.filter(task => !task.completed);

//   const handleTaskSelect = (id: string) => {
//     if (selectedTaskIds.includes(id)) {
//       setSelectedTaskIds(selectedTaskIds.filter(taskId => taskId !== id));
//     } else {
//       setSelectedTaskIds([...selectedTaskIds, id]);
//     }
//   };

//   const handleSelectAll = () => {
//     if (selectedTaskIds.length === filteredTasks.length) {
//       setSelectedTaskIds([]);
//     } else {
//       setSelectedTaskIds(filteredTasks.map(task => task.id));
//     }
//   };

//   const isAllSelected = selectedTaskIds.length > 0 && selectedTaskIds.length === filteredTasks.length;

//   return (
//     <div>
//       <div className="flex items-center justify-between mb-4">
//         <h2 className="text-lg font-semibold text-gray-900">{title}</h2>
//         {filteredTasks.length > 0 && (
//           <button
//             onClick={handleSelectAll}
//             className="text-sm text-pink-600 hover:text-pink-800"
//           >
//             {isAllSelected ? 'Deselect All' : 'Select All'}
//           </button>
//         )}
//       </div>

//       {filteredTasks.length === 0 ? (
//         <Card className="p-8 text-center border-2 border-dashed border-gray-300">
//           <p className="text-gray-500">No tasks to display</p>
//         </Card>
//       ) : (
//         <div className="space-y-3">
//           {filteredTasks.map((task) => (
//             <TaskCard
//               key={task.id}
//               id={task.id}
//               title={task.title}
//               description={task.description}
//               dueDate={task.dueDate}
//               priority={task.priority}
//               completed={task.completed}
//               onToggle={() => onTaskToggle?.(task.id)}
//               onEdit={() => onTaskEdit?.(task.id)}
//               onDelete={() => onTaskDelete?.(task.id)}
//               isSelected={selectedTaskIds.includes(task.id)}
//               onSelect={() => handleTaskSelect(task.id)}
//             />
//           ))}
//         </div>
//       )}
//     </div>
//   );
// };

// export default TaskList;