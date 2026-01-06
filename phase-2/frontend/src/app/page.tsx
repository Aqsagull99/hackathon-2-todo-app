'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FaCheck, FaList, FaBullseye, FaCalendarAlt, FaClock, FaStar } from 'react-icons/fa';
import QuickAddTaskCard from '@/components/features/tasks/QuickAddTaskCard';
import WhatsNextSection from '@/components/features/tasks/WhatsNextSection';
import HowItWorksSection from '@/components/features/tasks/HowItWorksSection';

export default function HomePage() {
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  // Floating icons data
  const floatingIcons = [
    { icon: <FaCheck className="text-pink-400" size={24} />, top: '15%', left: '10%' },
    { icon: <FaList className="text-pink-400" size={24} />, top: '25%', right: '15%' },
    { icon: <FaBullseye className="text-pink-400" size={24} />, bottom: '20%', left: '20%' },
    { icon: <FaCalendarAlt className="text-pink-400" size={24} />, top: '60%', right: '25%' },
    { icon: <FaClock className="text-pink-400" size={24} />, bottom: '10%', right: '10%' },
    { icon: <FaStar className="text-pink-400" size={24} />, top: '40%', left: '15%' },
  ];

  return (
    <>
      {/* Hero Section - Centered vertically */}
      <div className="min-h-screen bg-black flex items-center justify-center p-4 sm:p-6 md:p-8 relative overflow-hidden">
        {/* Floating glassmorphism icons - only in hero */}
        {floatingIcons.map((item, index) => (
          <motion.div
            key={index}
            className="absolute rounded-full bg-white/10 backdrop-blur-lg p-3 border border-white/20 shadow-lg"
            style={{
              top: item.top,
              left: item.left,
              right: item.right,
              bottom: item.bottom,
            }}
            initial={{ opacity: 0, scale: 0.5 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, delay: index * 0.1 }}
            whileHover={{ scale: 1.1, rotate: 5 }}
          >
            {item.icon}
          </motion.div>
        ))}

        {/* Main content container - centered content in hero */}
        <motion.div
          className="text-center z-10 max-w-sm sm:max-w-lg md:max-w-2xl w-full px-4"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: isMounted ? 1 : 0, y: isMounted ? 0 : 20 }}
          transition={{ duration: 0.8 }}
        >
          {/* Main headline */}
          <motion.h1
            className="text-4xl sm:text-5xl md:text-6xl font-bold text-white mb-4 sm:mb-6"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: isMounted ? 1 : 0, y: isMounted ? 0 : 20 }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            One Task at a Time
          </motion.h1>

          {/* Description */}
          <motion.p
            className="text-lg sm:text-xl md:text-2xl text-gray-300 mb-6 sm:mb-10 max-w-2xl mx-auto"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: isMounted ? 1 : 0, y: isMounted ? 0 : 20 }}
            transition={{ duration: 0.8, delay: 0.4 }}
          >
            A focused Todo app designed to help you move forward without distractions.
          </motion.p>

          {/* CTA Button */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: isMounted ? 1 : 0, y: isMounted ? 0 : 20 }}
            transition={{ duration: 0.8, delay: 0.6 }}
          >
            <motion.button
              className="px-6 sm:px-8 py-3 sm:py-4 bg-gradient-to-r from-pink-500 to-pink-600 text-white font-bold text-base sm:text-lg rounded-full shadow-lg hover:shadow-xl transition-all duration-300"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => {
                // Navigate to signup page
                window.location.href = '/register';
              }}
            >
              Get Started
            </motion.button>
          </motion.div>
        </motion.div>

        {/* Additional floating elements for depth - only in hero */}
        <div className="absolute top-1/4 left-1/4 w-16 h-16 rounded-full bg-pink-500/10 blur-xl"></div>
        <div className="absolute bottom-1/3 right-1/3 w-24 h-24 rounded-full bg-pink-500/10 blur-xl"></div>
        <div className="absolute top-1/2 right-1/4 w-20 h-20 rounded-full bg-pink-500/10 blur-xl"></div>
      </div>

      {/* Features Section - Below hero, normal vertical flow */}
      <div className="relative z-10 py-12 sm:py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl sm:max-w-5xl md:max-w-6xl mx-auto">
          <motion.div
            className="grid grid-cols-1 md:grid-cols-3 gap-8"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 1.2, duration: 0.6 }}
          >
            {/* Quick Add Task Card */}
            <div className="flex justify-center items-center">
              <QuickAddTaskCard className="w-full max-w-sm" />
            </div>

            {/* Focus Mode Card */}
            <motion.div
              className="rounded-2xl border border-white/10 bg-white/5 backdrop-blur-xl p-4 sm:p-6 text-center"
              whileHover={{ y: -10, scale: 1.02 }}
              transition={{ type: "spring", stiffness: 300, damping: 20 }}
            >
              <div className="w-14 h-14 sm:w-16 sm:h-16 rounded-full bg-pink-500/20 flex items-center justify-center mx-auto mb-3 sm:mb-4">
                <svg className="w-6 h-6 sm:w-8 sm:h-8 text-pink-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
              </div>
              <h3 className="text-lg sm:text-xl font-semibold text-white mb-1 sm:mb-2">Focus Mode</h3>
              <p className="text-sm sm:text-base text-gray-300">Stay focused with our distraction-free environment.</p>
            </motion.div>

            {/* Productivity Tracking Card */}
            <motion.div
              className="rounded-2xl border border-white/10 bg-white/5 backdrop-blur-xl p-4 sm:p-6 text-center"
              whileHover={{ y: -10, scale: 1.02 }}
              transition={{ type: "spring", stiffness: 300, damping: 20 }}
            >
              <div className="w-14 h-14 sm:w-16 sm:h-16 rounded-full bg-pink-500/20 flex items-center justify-center mx-auto mb-3 sm:mb-4">
                <svg className="w-6 h-6 sm:w-8 sm:h-8 text-pink-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <h3 className="text-lg sm:text-xl font-semibold text-white mb-1 sm:mb-2">Productivity Tracking</h3>
              <p className="text-sm sm:text-base text-gray-300">Track your progress and improve your productivity over time.</p>
            </motion.div>
          </motion.div>
        </div>
      </div>

      {/* What's Next Section - Below features, normal vertical flow */}
      <WhatsNextSection />

      {/* How It Works Section - Below What's Next, normal vertical flow */}
      <HowItWorksSection />
    </>
  );
}