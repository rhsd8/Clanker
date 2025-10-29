# 🤖 Complete Robot Setup Guide

Your Python backend is now connected to the React UI! Follow these steps to run the complete system.

## 📋 Prerequisites

Make sure you have:
- ✅ Python 3.8+ installed
- ✅ Node.js 18+ installed
- ✅ All API keys in `.env` file
- ✅ Python dependencies installed

## 🚀 Running the Complete System

You need to run **3 terminals** simultaneously:

### Terminal 1: WebSocket Server

```bash
cd server
python api.py
```

**What this does:**
- Starts WebSocket server on `http://localhost:8000`
- Broadcasts robot state changes to React UI
- Shows connection status

**You should see:**
```
🚀 Starting Robot WebSocket Server
📡 WebSocket: ws://localhost:8000/ws
🌐 HTTP API: http://localhost:8000
```

---

### Terminal 2: Python Robot Backend

```bash
python main.py
```

**What this does:**
- Runs the main robot controller
- Handles STT → LLM → TTS pipeline
- Broadcasts state changes to UI

**You should see:**
```
🤖 School Robot Assistant Starting...
✅ Robot is ready!
💡 Recording mode: Press ENTER to START, then ENTER again to STOP
```

---

### Terminal 3: React Frontend

```bash
cd ui.clanker/clanker.robot
npm run dev
```

**What this does:**
- Starts Next.js dev server on `http://localhost:3000`
- Displays animated robot face
- Connects to WebSocket server

**You should see:**
```
✓ Ready in 2s
○ Local:   http://localhost:3000
```

---

## 🎭 How It Works

### 1. Open Browser
Visit `http://localhost:3000` to see the robot face

### 2. Interaction Flow

```
You press Enter
    ↓
Face shows LISTENING (blue eyes)
    ↓
Student speaks
    ↓
You press Enter to stop
    ↓
Face shows THINKING (purple eyes + bouncing dots)
    ↓
LLM processes question
    ↓
Face shows SPEAKING (orange eyes + mouth)
    ↓
Robot speaks response with Josh's voice
    ↓
Face returns to IDLE (gray eyes)
```

### 3. State Changes

| Python State | Robot Face | Visual Indicator |
|-------------|------------|------------------|
| `idle` | Gray eyes | Gentle breathing animation |
| `listening` | Blue eyes | Audio waveform + ripples |
| `thinking` | Purple eyes | Bouncing dots |
| `speaking` | Orange eyes | Animated mouth |

---

## 🎨 Robot Face States

### Idle (Gray)
- Waiting for next student
- Gentle breathing animation
- Status: "Ready for students"

### Listening (Blue)
- Recording audio
- Audio waveform visualization
- Expanding ripples on cheeks
- Status: "Recording audio..."

### Thinking (Purple)
- Processing with LLM
- Three bouncing dots
- Eyes slightly larger
- Status: "Processing: [question]..."

### Speaking (Orange)
- Playing TTS audio
- Animated mouth
- Eyes slightly squinted
- Status: "[robot response]"

---

## 🔧 Troubleshooting

### UI Shows "Disconnected"
**Problem:** WebSocket server not running

**Solution:**
```bash
# Terminal 1
cd server
python api.py
```

### "Connection error - is server running?"
**Problem:** React can't connect to WebSocket

**Solutions:**
1. Check WebSocket server is running (Terminal 1)
2. Check no firewall blocking port 8000
3. Refresh browser page

### Robot face doesn't update
**Problem:** WebSocket server running but not receiving updates

**Solution:**
1. Check Terminal 1 for connection logs
2. Check Terminal 2 shows state broadcasts like: `📡 State broadcasted: listening`
3. Restart all 3 terminals

### "⚠️ WebSocket server not running"
**Problem:** Python backend can't reach WebSocket server

**Solution:**
```bash
# Make sure Terminal 1 is running
cd server
python api.py
```

---

##  🎯 Quick Start (All in One)

If using iTerm2 or tmux, you can run all 3 in split panes:

```bash
# Terminal 1 (top)
cd server && python api.py

# Terminal 2 (middle)
python main.py

# Terminal 3 (bottom)
cd ui.clanker/clanker.robot && npm run dev
```

Then open: `http://localhost:3000`

---

## 📊 System Architecture

```
┌─────────────────────┐
│   React Frontend    │
│  (Robot Face UI)    │
│  localhost:3000     │
└──────────┬──────────┘
           │ WebSocket
           │ ws://localhost:8000/ws
┌──────────▼──────────┐
│  WebSocket Server   │
│   (FastAPI)         │
│  localhost:8000     │
└──────────┬──────────┘
           │ HTTP POST
           │ /state endpoint
┌──────────▼──────────┐
│  Python Backend     │
│  (main.py)          │
│  STT → LLM → TTS    │
└─────────────────────┘
```

---

## 🎤 Testing the System

### 1. Verify WebSocket Connection
Open browser console (`F12`) and check for:
```
✅ Connected to robot
📡 Received state: {state: "idle", text: "Ready for students"}
```

### 2. Test State Changes
In Python terminal, press Enter and watch:
- **Terminal 2**: Shows state broadcasts
- **Browser**: Face changes to listening (blue)
- **Terminal 1**: Shows WebSocket messages

### 3. Test Full Flow
1. Press Enter in Terminal 2
2. Say "What is photosynthesis?"
3. Press Enter to stop
4. Watch face change: listening → thinking → speaking → idle

---

## 🚀 Production Deployment

For your school robot display:

### Extended Display Setup
- Run all 3 terminals on your computer
- Extend display to external monitor/screen
- Open browser at `http://localhost:3000` on the extended display
- Set browser to fullscreen mode (F11)
- All terminals run on main computer, UI shows on extended display

---

## 📝 Notes

- WebSocket server must start BEFORE React UI
- Python backend can run with or without WebSocket server
- If WebSocket server is down, Python still works but UI won't update
- Browser auto-reconnects if WebSocket drops

---

## 🎉 You're All Set!

Your robot is now fully integrated with:
- ✅ Speech-to-Text (Whisper)
- ✅ LLM Processing (DeepSeek)
- ✅ Text-to-Speech (ElevenLabs Josh)
- ✅ Animated UI (React + WebSocket)

**Enjoy your interactive school robot!** 🤖✨
