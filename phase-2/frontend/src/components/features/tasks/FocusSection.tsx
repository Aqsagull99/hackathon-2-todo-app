'use client';

import { motion } from 'framer-motion';
import QuickAddTaskCard from './QuickAddTaskCard';
import WhatsNextSection from './WhatsNextSection';
import HowItWorksSection from './HowItWorksSection';

export default function FocusSection() {
  return (
    <section className="py-16 px-4 sm:px-6 lg:px-8">
      <div className="max-w-6xl mx-auto">
        <motion.div
          className="text-center mb-12"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
            Get Things Done
          </h2>
          <p className="text-pink-200/80 text-lg max-w-2xl mx-auto">
            Focus on what matters most with our intuitive task management system
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <QuickAddTaskCard />
          <WhatsNextSection />
          <HowItWorksSection />
        </div>
      </div>
    </section>
  );
}