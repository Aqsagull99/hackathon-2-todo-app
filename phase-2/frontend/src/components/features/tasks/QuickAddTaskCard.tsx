'use client';

import { motion } from 'framer-motion';
import { Plus } from 'lucide-react';
import { useSession } from '@/lib/auth-client';
import { useRouter } from 'next/navigation';

interface QuickAddTaskCardProps {
  className?: string;
}

export default function QuickAddTaskCard({ className = '' }: QuickAddTaskCardProps) {
  const { data: session, isLoading } = useSession();
  const router = useRouter();
  const isClient = typeof window !== 'undefined';

  const handleClick = () => {
    if (!session) {
      // User is not logged in, redirect to login
      router.push('/login');
    } else {
      // User is logged in, navigate to dashboard and trigger add task form
      router.push('/dashboard?addTask=true');
    }
  };

  // Show loading state while checking auth status or if not client-side rendered
  if (isLoading || !isClient) {
    return (
      <motion.div
        className={`relative rounded-2xl border border-pink-500/20 bg-black/20 backdrop-blur-xl p-6 shadow-lg cursor-not-allowed ${className}`}
        whileHover={{ scale: 1 }}
        whileTap={{ scale: 1 }}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
      >
        <div className="flex flex-col items-center justify-center py-8">
          <div className="w-8 h-8 border-2 border-pink-500 border-t-transparent rounded-full animate-spin mb-4" />
          <p className="text-pink-300 text-sm font-medium">Checking auth status...</p>
        </div>
      </motion.div>
    );
  }

  return (
    <motion.div
      className={`relative rounded-2xl border border-pink-500/20 bg-black/20 backdrop-blur-xl p-6 cursor-pointer group hover:border-pink-500/40 transition-colors duration-300 ${className}`}
      whileHover={{
        scale: 1.03,
        boxShadow: '0 25px 50px -12px rgba(255, 192, 203, 0.25)'
      }}
      whileTap={{ scale: 0.98 }}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.2 }}
      onClick={handleClick}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          handleClick();
        }
      }}
      aria-label="Quick add task - Click to add a new task"
    >
      {/* Inner glow effect */}
      <div
        className="absolute inset-0 rounded-2xl bg-gradient-to-br from-pink-500/10 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none"
        aria-hidden="true"
      />

      <div className="relative z-10 flex flex-col items-center text-center">
        {/* Icon container with animation */}
        <motion.div
          className="w-16 h-16 rounded-full bg-pink-500/20 flex items-center justify-center mb-4 flex-shrink-0"
          whileHover={{
            scale: 1.1,
            backgroundColor: 'rgba(255, 192, 203, 0.3)'
          }}
          transition={{ type: 'spring', stiffness: 400, damping: 17 }}
        >
          <Plus
            className="w-8 h-8 text-pink-400 group-hover:text-pink-300 transition-colors duration-300"
            aria-hidden="true"
          />
        </motion.div>

        {/* Title */}
        <motion.h3
          className="text-xl font-semibold text-white mb-2"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
        >
          Add Task
        </motion.h3>

        {/* Helper text */}
        <motion.p
          className="text-pink-200/80 text-sm font-medium"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
        >
          Create a new task instantly
        </motion.p>
      </div>
    </motion.div>
  );
}