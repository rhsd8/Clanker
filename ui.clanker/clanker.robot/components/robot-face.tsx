"use client"

import { motion, AnimatePresence } from "framer-motion"
import { useEffect, useState } from "react"

type EmotionState = "idle" | "listening" | "thinking" | "speaking"

interface RobotFaceProps {
  emotionState: EmotionState
}

export function RobotFace({ emotionState }: RobotFaceProps) {
  const [waveformBars, setWaveformBars] = useState<number[]>([0.3, 0.5, 0.4, 0.6, 0.3])

  // Animate waveform bars for listening mode
  useEffect(() => {
    if (emotionState === "listening") {
      const interval = setInterval(() => {
        setWaveformBars((prev) => prev.map(() => Math.random() * 0.6 + 0.2))
      }, 150)
      return () => clearInterval(interval)
    }
  }, [emotionState])

  // Eye configurations for different states (scaled up for larger face)
  const eyeConfig = {
    idle: {
      width: 160,
      height: 160,
      color: "rgba(148, 163, 184, 0.6)", // slate-400 with opacity
      glow: "rgba(148, 163, 184, 0.3)",
    },
    listening: {
      width: 180,
      height: 180,
      color: "rgba(59, 130, 246, 0.9)", // blue-500
      glow: "rgba(59, 130, 246, 0.5)",
    },
    thinking: {
      width: 170,
      height: 170,
      color: "rgba(168, 85, 247, 0.9)", // purple-500
      glow: "rgba(168, 85, 247, 0.5)",
    },
    speaking: {
      width: 170,
      height: 150,
      color: "rgba(251, 146, 60, 0.9)", // orange-400
      glow: "rgba(251, 146, 60, 0.5)",
    },
  }

  const currentEyeConfig = eyeConfig[emotionState]

  return (
    <div className="relative w-[85vmin] h-[85vmin] flex items-center justify-center">
      {/* Main face container */}
      <motion.div
        className="relative w-full h-full rounded-full bg-gradient-to-br from-slate-100 to-slate-300 shadow-2xl"
        animate={{
          scale: emotionState === "listening" ? [1, 1.02, 1] : 1,
        }}
        transition={{
          duration: 2,
          repeat: emotionState === "listening" ? Number.POSITIVE_INFINITY : 0,
          ease: "easeInOut",
        }}
      >
        {/* Ambient glow */}
        <motion.div
          className="absolute inset-0 rounded-full"
          animate={{
            boxShadow:
              emotionState === "idle"
                ? "0 0 60px rgba(148, 163, 184, 0.3)"
                : emotionState === "listening"
                  ? "0 0 80px rgba(59, 130, 246, 0.6)"
                  : "0 0 80px rgba(251, 146, 60, 0.6)",
          }}
          transition={{ duration: 0.5 }}
        />

        {/* Eyes container */}
        <div className="absolute inset-0 flex items-center justify-center gap-24">
          {/* Left eye */}
          <motion.div
            className="relative rounded-full"
            animate={{
              width: currentEyeConfig.width,
              height: currentEyeConfig.height,
              backgroundColor: currentEyeConfig.color,
              boxShadow: `0 0 60px ${currentEyeConfig.glow}`,
            }}
            transition={{ duration: 0.3 }}
          >
            {/* Eye shine */}
            <div className="absolute top-4 left-4 w-8 h-8 bg-white rounded-full opacity-60" />
          </motion.div>

          {/* Right eye */}
          <motion.div
            className="relative rounded-full"
            animate={{
              width: currentEyeConfig.width,
              height: currentEyeConfig.height,
              backgroundColor: currentEyeConfig.color,
              boxShadow: `0 0 60px ${currentEyeConfig.glow}`,
            }}
            transition={{ duration: 0.3 }}
          >
            {/* Eye shine */}
            <div className="absolute top-4 left-4 w-8 h-8 bg-white rounded-full opacity-60" />
          </motion.div>
        </div>

        {/* Mouth/speaking indicator */}
        <AnimatePresence mode="wait">
          {emotionState === "speaking" && (
            <motion.div
              key="speaking-mouth"
              className="absolute bottom-32 left-1/2 -translate-x-1/2 w-64 h-16 rounded-full bg-gradient-to-r from-orange-400 to-orange-500"
              initial={{ opacity: 0, scaleY: 0 }}
              animate={{
                opacity: [0.6, 1, 0.6],
                scaleY: [0.2, 1, 0.8],
                boxShadow: [
                  "0 0 40px rgba(251, 146, 60, 0.4)",
                  "0 0 60px rgba(251, 146, 60, 0.6)",
                  "0 0 40px rgba(251, 146, 60, 0.4)",
                ],
              }}
              exit={{ opacity: 0, scaleY: 0 }}
              transition={{
                duration: 0.8,
                repeat: Number.POSITIVE_INFINITY,
                ease: "easeInOut",
              }}
            />
          )}
        </AnimatePresence>

        {/* Idle mode - slow subtle mouth breathing */}
        <AnimatePresence>
          {emotionState === "idle" && (
            <motion.div
              className="absolute bottom-32 left-1/2 -translate-x-1/2 w-48 h-6 rounded-full bg-slate-400"
              initial={{ opacity: 0, scaleY: 0 }}
              animate={{
                opacity: [0.3, 0.5, 0.3],
                scaleY: [0.8, 1, 0.8],
              }}
              exit={{ opacity: 0, scaleY: 0 }}
              transition={{
                duration: 4,
                repeat: Number.POSITIVE_INFINITY,
                ease: "easeInOut",
              }}
            />
          )}
        </AnimatePresence>

        {/* Waveform for listening mode */}
        <AnimatePresence>
          {emotionState === "listening" && (
            <motion.div
              className="absolute bottom-28 left-1/2 -translate-x-1/2 flex items-end gap-4 h-24"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              {waveformBars.map((height, index) => (
                <motion.div
                  key={index}
                  className="w-4 bg-blue-400 rounded-full"
                  animate={{
                    height: `${height * 100}%`,
                  }}
                  transition={{
                    duration: 0.15,
                    ease: "easeOut",
                  }}
                  style={{
                    boxShadow: "0 0 20px rgba(59, 130, 246, 0.5)",
                  }}
                />
              ))}
            </motion.div>
          )}
        </AnimatePresence>

        {/* Breathing glow for idle mode */}
        <AnimatePresence>
          {emotionState === "idle" && (
            <motion.div
              className="absolute inset-16 rounded-full bg-slate-200"
              initial={{ opacity: 0 }}
              animate={{
                opacity: [0.1, 0.3, 0.1],
              }}
              exit={{ opacity: 0 }}
              transition={{
                duration: 3,
                repeat: Number.POSITIVE_INFINITY,
                ease: "easeInOut",
              }}
            />
          )}
        </AnimatePresence>

        {/* Thinking indicator - spinning dots */}
        <AnimatePresence>
          {emotionState === "thinking" && (
            <motion.div
              className="absolute bottom-28 left-1/2 -translate-x-1/2 flex gap-4"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              {[0, 1, 2].map((index) => (
                <motion.div
                  key={index}
                  className="w-6 h-6 bg-purple-400 rounded-full"
                  animate={{
                    y: [0, -20, 0],
                    opacity: [0.5, 1, 0.5],
                  }}
                  transition={{
                    duration: 0.6,
                    repeat: Number.POSITIVE_INFINITY,
                    ease: "easeInOut",
                    delay: index * 0.2,
                  }}
                  style={{
                    boxShadow: "0 0 20px rgba(168, 85, 247, 0.5)",
                  }}
                />
              ))}
            </motion.div>
          )}
        </AnimatePresence>

        {/* Cheek ripples for listening mode */}
        <AnimatePresence>
          {emotionState === "listening" && (
            <>
              {/* Left cheek ripple */}
              <motion.div
                className="absolute left-16 top-1/2 -translate-y-1/2 w-32 h-32 rounded-full border-4 border-blue-400"
                initial={{ opacity: 0, scale: 0.5 }}
                animate={{
                  opacity: [0.6, 0],
                  scale: [0.5, 1.2],
                }}
                transition={{
                  duration: 1.5,
                  repeat: Number.POSITIVE_INFINITY,
                  ease: "easeOut",
                }}
              />
              {/* Right cheek ripple */}
              <motion.div
                className="absolute right-16 top-1/2 -translate-y-1/2 w-32 h-32 rounded-full border-4 border-blue-400"
                initial={{ opacity: 0, scale: 0.5 }}
                animate={{
                  opacity: [0.6, 0],
                  scale: [0.5, 1.2],
                }}
                transition={{
                  duration: 1.5,
                  repeat: Number.POSITIVE_INFINITY,
                  ease: "easeOut",
                  delay: 0.75,
                }}
              />
            </>
          )}
        </AnimatePresence>
      </motion.div>

      {/* State label */}
      
    </div>
  )
}
