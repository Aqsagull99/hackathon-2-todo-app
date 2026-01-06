'use client';

import { motion } from 'framer-motion';

export default function WhatsNextSection() {
  return (
    <motion.div
      className="relative rounded-2xl border border-pink-500/20 bg-black/20 backdrop-blur-xl p-6"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay: 0.3 }}
    >
      <div className="text-center mb-4">
        <h3 className="text-lg font-semibold text-white mb-2">
          What's Next?
        </h3>
      </div>

      <div className="text-center">
        <p className="text-white/90 mb-4">
          Focus on your most important tasks first
        </p>
        <div className="flex items-center justify-center gap-2 mb-4">
          <span className="text-sm font-medium text-pink-400 bg-pink-500/20 px-3 py-1 rounded-full">
            High priority
          </span>
          <span className="text-sm text-gray-400">· Due today</span>
        </div>

        <motion.button
          className="inline-flex items-center gap-2 text-pink-400 hover:text-pink-300 cursor-pointer group"
          whileHover={{ opacity: 0.8 }}
          transition={{ type: 'spring', stiffness: 400, damping: 17 }}
        >
          <span className="text-base font-medium">Start working</span>
          <svg
            className="w-4 h-4 group-hover:translate-x-1 transition-transform duration-200"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 5l7 7-7 7"
            />
          </svg>
        </motion.button>
      </div>
    </motion.div>
  );
}