# Robot State Flow

## Complete Interaction Flow

### 1. **IDLE** (Gray Eyes)
- Robot waiting for next student
- Press ENTER in Terminal 2 to start

### 2. **LISTENING** (Blue Eyes)
- Robot is recording audio
- Automatically starts when you press ENTER
- Student speaks their question

### 3. **THINKING** (Purple Eyes, Bouncing Dots)
- **Triggered immediately when:**
  - You press ENTER to stop recording, OR
  - 3 seconds of silence detected after speaking
- Robot is:
  1. First transcribing audio (Whisper API)
  2. Then processing with LLM (DeepSeek)

### 4. **SPEAKING** (Orange Eyes)
- Robot playing audio response
- Using ElevenLabs TTS (Josh voice)

### 5. Back to **IDLE**
- Ready for next student

## Updated Files

### [modules/stt_sounddevice.py](modules/stt_sounddevice.py:218-252)
- Added `on_stop_callback` parameter to `manual_listen_and_transcribe()`
- Added `on_stop_callback` parameter to `record_audio()`
- Callback fires immediately when recording stops (before transcription)

### [main.py](main.py:95-98)
- Passes lambda callback to switch to "thinking" state immediately
- Flow: Listening → **Stop Recording** → **THINKING** → Transcribe → Process LLM → Speaking

## Visual Timeline

```
User Press ENTER to start
         ↓
    🔵 LISTENING (Blue Eyes)
         ↓
    Student speaks...
         ↓
User Press ENTER OR 3 seconds silence
         ↓
    🟣 THINKING (Purple Eyes) ← IMMEDIATE!
         ↓
    Transcribing audio (Whisper)
         ↓
    Processing with LLM (DeepSeek)
         ↓
    🟠 SPEAKING (Orange Eyes)
         ↓
    Playing audio response (Josh voice)
         ↓
    ⚪ IDLE (Gray Eyes)
```

## Testing

1. Make sure all servers are running:
   ```bash
   # Terminal 1
   python3 server/api.py

   # Terminal 2
   python3 main.py

   # Terminal 3
   cd ui.clanker/clanker.robot && npm run dev
   ```

2. Open browser: `http://192.168.191.101:3000`

3. In Terminal 2, press ENTER to start

4. Watch the robot face:
   - Should turn BLUE when listening starts
   - Should turn PURPLE immediately when you press ENTER or after 3 seconds silence
   - Should turn ORANGE when speaking
   - Should return to GRAY when done

## Key Change

**Before**: Face stayed blue during transcription and only turned purple during LLM processing

**Now**: Face turns purple **immediately** when recording stops (either manual Enter press or auto-silence detection)
