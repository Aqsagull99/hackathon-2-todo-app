'use client';

import { motion } from 'framer-motion';
import { FaArrowRight, FaBullseye } from 'react-icons/fa';

export default function WhatsNextSection() {
  return (
    <motion.section
      className="relative mx-auto max-w-5xl px-4 py-16"
      initial={{ opacity: 0 }}
      whileInView={{ opacity: 1 }}
      viewport={{ once: true }}
      transition={{ duration: 0.8 }}
    >
      {/* Glow Background */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(236,72,153,0.12),transparent_70%)]" />

      <motion.div
        className="relative rounded-3xl border border-pink-500/20
        bg-white/5 backdrop-blur-xl p-8 sm:p-12 text-center overflow-hidden"
        initial={{ y: 30, opacity: 0 }}
        whileInView={{ y: 0, opacity: 1 }}
        viewport={{ once: true }}
        transition={{ duration: 0.7, ease: 'easeOut' }}
      >
        {/* Floating Icon */}
        <motion.div
          className="w-16 h-16 mx-auto mb-6 rounded-full
          bg-pink-500/20 flex items-center justify-center
          shadow-[0_0_25px_rgba(236,72,153,0.45)]"
          animate={{ y: [0, -8, 0] }}
          transition={{ duration: 3, repeat: Infinity, ease: 'easeInOut' }}
        >
          <FaBullseye className="text-pink-400 w-7 h-7" />
        </motion.div>

        {/* Title */}
        <motion.h3
          className="text-2xl sm:text-3xl font-bold text-white mb-4"
          initial={{ opacity: 0, y: 10 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.1 }}
        >
          What’s Next?
        </motion.h3>

        {/* Description */}
        <motion.p
          className="text-lg text-gray-300 max-w-xl mx-auto mb-6"
          initial={{ opacity: 0, y: 10 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.2 }}
        >
          Focus on the single most important task that moves you forward today.
        </motion.p>

        {/* Priority Tags */}
        <motion.div
          className="flex items-center justify-center gap-3 mb-8"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ delay: 0.3 }}
        >
          <span className="text-sm font-semibold text-pink-300 bg-pink-500/20 px-4 py-1.5 rounded-full">
            High Priority
          </span>
          <span className="text-sm text-gray-400">• Due Today</span>
        </motion.div>

        {/* CTA */}
        <motion.button
          className="group inline-flex items-center gap-3
          text-pink-400 font-semibold text-lg"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <span>Start Working</span>
          <motion.span
            className="flex items-center justify-center w-9 h-9
            rounded-full bg-pink-500/20"
            whileHover={{ x: 4 }}
            transition={{ type: 'spring', stiffness: 400, damping: 15 }}
          >
            <FaArrowRight className="text-pink-400 w-4 h-4" />
          </motion.span>
        </motion.button>

        {/* Decorative Blur */}
        <div className="absolute -bottom-16 -right-16 w-40 h-40 bg-pink-500/20 rounded-full blur-3xl" />
      </motion.div>
    </motion.section>
  );
}
