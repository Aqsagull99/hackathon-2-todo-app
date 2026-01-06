'use client';

import { motion } from 'framer-motion';
import { Zap, Calendar, CheckCircle2 } from 'lucide-react';

export default function HowItWorksSection() {
  const steps = [
    {
      icon: <Zap className="w-6 h-6 text-pink-400" />,
      text: "Add tasks"
    },
    {
      icon: <Calendar className="w-6 h-6 text-pink-400" />,
      text: "Plan your day"
    },
    {
      icon: <CheckCircle2 className="w-6 h-6 text-pink-400" />,
      text: "Get things done"
    }
  ];

  return (
    <motion.div
      className="relative rounded-2xl border border-pink-500/20 bg-black/20 backdrop-blur-xl p-6"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay: 0.4 }}
    >
      <div className="text-center mb-6">
        <h3 className="text-lg font-semibold text-white mb-2">
          How It Works
        </h3>
      </div>

      <div className="flex flex-col items-center gap-6">
        {steps.map((step, index) => (
          <motion.div
            key={index}
            className="flex flex-col items-center text-center"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.5 + index * 0.1 }}
          >
            {/* Icon */}
            <div className="w-12 h-12 rounded-full bg-pink-500/10 flex items-center justify-center mb-3">
              {step.icon}
            </div>

            {/* Step text */}
            <p className="text-sm text-gray-300 font-medium">
              {step.text}
            </p>

            {/* Arrow separator (except for last item) */}
            {index < steps.length - 1 && (
              <div className="w-full flex justify-center my-2">
                <svg
                  className="w-6 h-6 text-pink-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M19 14l-7 7m0 0l-7-7m7 7V3"
                  />
                </svg>
              </div>
            )}
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
}