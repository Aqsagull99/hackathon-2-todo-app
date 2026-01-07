'use client';

import { motion } from 'framer-motion';
import { Zap, Calendar, CheckCircle2 } from 'lucide-react';

export default function HowItWorksSection() {
  const steps = [
    {
      icon: <Zap className="w-6 h-6 text-pink-400" />,
      title: 'Add Tasks',
      desc: 'Quickly capture what matters before it slips away.',
    },
    {
      icon: <Calendar className="w-6 h-6 text-pink-400" />,
      title: 'Plan Your Day',
      desc: 'Organize tasks with clarity and realistic priorities.',
    },
    {
      icon: <CheckCircle2 className="w-6 h-6 text-pink-400" />,
      title: 'Get Things Done',
      desc: 'Focus, complete, and enjoy real progress.',
    },
  ];

  return (
    <motion.section
      className="relative mx-auto max-w-6xl px-4 py-20"
      initial={{ opacity: 0 }}
      whileInView={{ opacity: 1 }}
      viewport={{ once: true }}
      transition={{ duration: 0.8 }}
    >
      {/* Background Glow */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(236,72,153,0.12),transparent_70%)]" />

      {/* Card */}
      <motion.div
        className="relative rounded-3xl border border-pink-500/20
        bg-white/5 backdrop-blur-xl p-8 sm:p-12 overflow-hidden"
        initial={{ y: 30, opacity: 0 }}
        whileInView={{ y: 0, opacity: 1 }}
        viewport={{ once: true }}
        transition={{ duration: 0.7, ease: 'easeOut' }}
      >
        {/* Heading */}
        <motion.div
          className="text-center mb-14"
          initial={{ opacity: 0, y: 10 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
        >
          <h3 className="text-2xl sm:text-3xl font-bold text-white mb-3">
            How It Works
          </h3>
          <p className="text-gray-400 max-w-xl mx-auto">
            A simple flow designed to keep you focused and productive.
          </p>
        </motion.div>

        {/* Steps */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-10 relative">
          {steps.map((step, index) => (
            <motion.div
              key={index}
              className="relative text-center"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.15 }}
            >
              {/* Connector Line */}
              {index < steps.length - 1 && (
                <div className="hidden md:block absolute top-8 right-[-50%] w-full h-px bg-gradient-to-r from-pink-500/40 to-transparent" />
              )}

              {/* Icon */}
              <motion.div
                className="w-14 h-14 mx-auto mb-5 rounded-full
                bg-pink-500/20 flex items-center justify-center
                shadow-[0_0_25px_rgba(236,72,153,0.45)]"
                animate={{ y: [0, -6, 0] }}
                transition={{ duration: 3, repeat: Infinity, ease: 'easeInOut' }}
              >
                {step.icon}
              </motion.div>

              {/* Text */}
              <h4 className="text-lg font-semibold text-white mb-2">
                {step.title}
              </h4>
              <p className="text-sm text-gray-300 max-w-xs mx-auto">
                {step.desc}
              </p>
            </motion.div>
          ))}
        </div>

        {/* Decorative Blur */}
        <div className="absolute -bottom-24 -left-24 w-64 h-64 bg-pink-500/20 rounded-full blur-3xl" />
      </motion.div>
    </motion.section>
  );
}
