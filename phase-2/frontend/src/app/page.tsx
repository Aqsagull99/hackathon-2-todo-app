'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
  FaCheck,
  FaList,
  FaBullseye,
  FaCalendarAlt,
  FaClock,
  FaStar,
} from 'react-icons/fa';

import QuickAddTaskCard from '@/components/features/tasks/QuickAddTaskCard';
import WhatsNextSection from '@/components/features/tasks/WhatsNextSection';
import HowItWorksSection from '@/components/features/tasks/HowItWorksSection';

export default function HomePage() {
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  const headline = 'One Task at a Time'.split(' ');

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
      {/* ================= HERO SECTION ================= */}
      <div className="relative min-h-screen bg-black flex items-center justify-center overflow-hidden px-4">

        {/* Glow & Texture */}
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(236,72,153,0.15),transparent_70%)]" />
        <div className="absolute inset-0 opacity-[0.03] bg-[url('/noise.png')]" />

        {/* Floating Icons */}
        {floatingIcons.map((item, index) => (
          <motion.div
            key={index}
            className="absolute rounded-full bg-white/10 backdrop-blur-xl
            p-3 border border-white/20 shadow-lg"
            style={{
              top: item.top,
              left: item.left,
              right: item.right,
              bottom: item.bottom,
            }}
            initial={{ opacity: 0, scale: 0.6 }}
            animate={{
              opacity: 1,
              scale: 1,
              y: [0, -12, 0],
            }}
            transition={{
              duration: 4 + index,
              repeat: Infinity,
              ease: 'easeInOut',
            }}
          >
            {item.icon}
          </motion.div>
        ))}

        {/* Hero Content */}
        <motion.div
          className="relative z-10 text-center max-w-3xl"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: isMounted ? 1 : 0, y: isMounted ? 0 : 30 }}
          transition={{ duration: 0.8 }}
        >
          {/* Animated Headline */}
          <motion.h1
            className="text-4xl sm:text-5xl md:text-6xl font-bold text-white mb-6 leading-tight"
            initial="hidden"
            animate="visible"
            variants={{
              visible: { transition: { staggerChildren: 0.12 } },
            }}
          >
            {headline.map((word, i) => (
              <motion.span
                key={i}
                className="inline-block mr-2"
                variants={{
                  hidden: { opacity: 0, y: 30, filter: 'blur(6px)' },
                  visible: { opacity: 1, y: 0, filter: 'blur(0px)' },
                }}
                transition={{ duration: 0.6, ease: 'easeOut' }}
              >
                {word}
              </motion.span>
            ))}
          </motion.h1>

          {/* Subtitle */}
          <motion.p
            className="text-lg sm:text-xl md:text-2xl mb-10
            bg-gradient-to-r from-gray-300 via-pink-200 to-gray-300
            bg-clip-text text-transparent max-w-2xl mx-auto"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6, duration: 0.8 }}
          >
            A focused Todo app designed to help you move forward without distractions.
          </motion.p>

          {/* CTA */}
          <motion.button
            className="relative px-8 py-4 rounded-full font-bold text-lg text-white
            bg-gradient-to-r from-pink-500 to-pink-600 shadow-xl overflow-hidden"
            animate={{
              boxShadow: [
                '0 0 20px rgba(236,72,153,0.4)',
                '0 0 35px rgba(236,72,153,0.6)',
                '0 0 20px rgba(236,72,153,0.4)',
              ],
            }}
            transition={{ duration: 2.5, repeat: Infinity }}
            whileHover={{ scale: 1.08 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => (window.location.href = '/register')}
          >
            Get Started
          </motion.button>
        </motion.div>
      </div>

      {/* ================= FEATURES ================= */}
      <div className="py-20 px-4">
        <div className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-8">

          <QuickAddTaskCard />

          {[
            {
              title: 'Focus Mode',
              desc: 'Stay focused with a distraction-free environment.',
              icon: (
                <FaBullseye className="text-pink-400 w-7 h-7" />
              ),
            },
            {
              title: 'Productivity Tracking',
              desc: 'Track progress and build productive habits.',
              icon: (
                <FaCalendarAlt className="text-pink-400 w-7 h-7" />
              ),
            },
          ].map((item, i) => (
            <motion.div
              key={i}
              className="rounded-2xl border border-white/10 bg-white/5
              backdrop-blur-xl p-6 text-center"
              whileHover={{
                y: -12,
                scale: 1.04,
                boxShadow: '0 20px 40px rgba(236,72,153,0.15)',
              }}
              transition={{ type: 'spring', stiffness: 300, damping: 20 }}
            >
              <div
                className="w-16 h-16 mx-auto mb-4 rounded-full bg-pink-500/20
                flex items-center justify-center
                shadow-[0_0_20px_rgba(236,72,153,0.4)]"
              >
                {item.icon}
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">
                {item.title}
              </h3>
              <p className="text-gray-300">{item.desc}</p>
            </motion.div>
          ))}
        </div>
      </div>

      {/* ================= NEXT SECTIONS ================= */}
      <WhatsNextSection />
      <HowItWorksSection />
    </>
  );
}
