"use client"

import { useState, useEffect } from "react"
import { RobotFace } from "@/components/robot-face"

type EmotionState = "idle" | "listening" | "thinking" | "speaking"

export default function Home() {
  const [emotionState, setEmotionState] = useState<EmotionState>("idle")
  const [statusText, setStatusText] = useState<string>("Connecting to robot...")
  const [isConnected, setIsConnected] = useState(false)
  const [isFullscreen, setIsFullscreen] = useState(false)

  // Fullscreen functionality
  const toggleFullscreen = () => {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen()
      setIsFullscreen(true)
    } else {
      document.exitFullscreen()
      setIsFullscreen(false)
    }
  }

  // Handle fullscreen change events
  useEffect(() => {
    const handleFullscreenChange = () => {
      setIsFullscreen(!!document.fullscreenElement)
    }

    document.addEventListener("fullscreenchange", handleFullscreenChange)
    return () => {
      document.removeEventListener("fullscreenchange", handleFullscreenChange)
    }
  }, [])

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyPress = (e: KeyboardEvent) => {
      // F11 or 'f' key to toggle fullscreen
      if (e.key === "F11" || (e.key === "f" && !e.ctrlKey && !e.metaKey)) {
        e.preventDefault()
        toggleFullscreen()
      }
      // Escape to exit fullscreen
      if (e.key === "Escape" && isFullscreen) {
        document.exitFullscreen()
      }
    }

    window.addEventListener("keydown", handleKeyPress)
    return () => {
      window.removeEventListener("keydown", handleKeyPress)
    }
  }, [isFullscreen])

  useEffect(() => {
    // Connect to WebSocket server (always localhost since display is extended)
    const ws = new WebSocket("ws://localhost:8000/ws")

    ws.onopen = () => {
      console.log("✅ Connected to robot")
      setIsConnected(true)
      setStatusText("Connected - Ready for students")
    }

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        console.log("📡 Received state:", data)

        // Update emotion state
        if (data.state) {
          setEmotionState(data.state as EmotionState)
        }

        // Update status text
        if (data.text) {
          setStatusText(data.text)
        }
      } catch (error) {
        console.error("Error parsing message:", error)
      }
    }

    ws.onerror = (error) => {
      console.error("❌ WebSocket error:", error)
      setIsConnected(false)
      setStatusText("Connection error - is server running?")
    }

    ws.onclose = () => {
      console.log("🔌 Disconnected from robot")
      setIsConnected(false)
      setStatusText("Disconnected - Reconnecting...")

      // Auto-reconnect after 3 seconds
      setTimeout(() => {
        window.location.reload()
      }, 3000)
    }

    // Cleanup on unmount
    return () => {
      ws.close()
    }
  }, [])

  return (
    <main className="min-h-screen w-screen flex flex-col items-center justify-center bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 relative overflow-hidden">
      {/* Fullscreen Toggle Button */}
      <button
        onClick={toggleFullscreen}
        className="fixed top-2 right-2 z-50 p-2 bg-slate-800/80 hover:bg-slate-700/80 text-slate-300 rounded-lg border border-slate-600 transition-all duration-200 hover:scale-105 backdrop-blur-sm"
        title={isFullscreen ? "Exit Fullscreen (F or ESC)" : "Enter Fullscreen (F or F11)"}
      >
        {isFullscreen ? (
          // Exit fullscreen icon
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        ) : (
          // Enter fullscreen icon
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" />
          </svg>
        )}
      </button>

      {/* Robot Face - centered and taking up most of the screen */}
      <div className="flex items-center justify-center">
        <RobotFace emotionState={emotionState} />
      </div>

      {/* Connection Instructions - compact overlay at bottom */}
      {!isConnected && (
        <div className="fixed bottom-4 left-4 right-4 text-center text-xs text-slate-500 bg-slate-800/50 rounded-lg p-2 border border-slate-700 backdrop-blur-sm">
          <p className="text-balance">Server not connected</p>
          <code className="block mt-1 text-[10px] text-slate-400">
            python server/api.py
          </code>
        </div>
      )}

      {/* Fullscreen hint - compact corner hint */}
      {!isFullscreen && (
        <div className="fixed bottom-2 left-2 text-[10px] text-slate-700 bg-slate-900/50 rounded px-2 py-1">
          Press F for fullscreen
        </div>
      )}
    </main>
  )
}
