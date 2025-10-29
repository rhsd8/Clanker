# School Robot Assistant

An interactive robot that listens to students, processes their questions using AI, and responds with speech.

## Features

- Speech-to-Text using OpenAI Whisper
  - Manual start (press Enter to begin listening)
  - Auto-stop on silence detection
- LLM Processing using OpenRouter DeepSeek V3.1
  - Free AI model for intelligent responses
  - Conversation context tracking
  - School-appropriate responses
- Text-to-Speech using ElevenLabs
  - Natural, expressive voice (Adam)
  - High-quality audio output
  - Direct playback through speakers
- Visual Display Interface (Coming soon)

## Current Status

✅ Speech-to-Text (OpenAI Whisper) - WORKING
✅ LLM Processing (OpenRouter DeepSeek V3.1) - WORKING
✅ Text-to-Speech (ElevenLabs Adam Voice) - WORKING
⏳ GUI Display - TODO

## Project Structure

```
Clanker/
├── main.py              # Main robot controller
├── config.yaml          # Configuration file (API keys, settings)
├── requirements.txt     # Python dependencies
├── modules/
│   ├── __init__.py
│   ├── stt.py          # Speech-to-Text module (Whisper)
│   ├── llm.py          # LLM processing (TODO)
│   └── tts.py          # Text-to-Speech (TODO)
├── gui/
│   ├── __init__.py
│   └── display.py      # Visual interface (TODO)
└── README.md
```

## Setup Instructions

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Note**: This project uses `sounddevice` instead of PyAudio for easier macOS installation. No need to install PortAudio separately!

### 2. Configure API Keys

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Then edit [.env](.env) and add your API keys:

```
# For Speech-to-Text
OPENAI_API_KEY=sk-your-openai-api-key-here

# For LLM Processing (FREE!)
OPENROUTER_API_KEY=sk-or-your-openrouter-api-key-here

# For Text-to-Speech (FREE tier: 10k chars/month)
ELEVENLABS_API_KEY=sk-your-elevenlabs-api-key-here
```

**Get your API keys:**
- **OpenAI**: https://platform.openai.com/api-keys (for Whisper STT)
- **OpenRouter**: https://openrouter.ai/keys (for DeepSeek LLM - Free tier!)
- **ElevenLabs**: https://elevenlabs.io/ (for TTS - Free tier: 10k characters/month)

**Important**: Never commit your `.env` file to git! It's already in [.gitignore](.gitignore).

### 3. Test Speech-to-Text

Run the STT module directly to test:

```bash
cd modules
python stt.py
```

Speak into your microphone after you see "Listening... Speak now!"

### 4. Run the Robot

```bash
python main.py
```

The robot will wait for you to press Enter before listening to each student.

## How It Works

### Interaction Flow

1. **Press Enter** to start recording
2. Robot begins recording through microphone
3. Student speaks their question
4. **Press Enter again** to stop recording and process
5. Audio is sent to OpenAI Whisper API for transcription
6. Text is sent to DeepSeek LLM for intelligent response
7. Robot displays the response in text
8. Response is spoken through speakers using Adam's voice (ElevenLabs)
9. Repeat for next student

This design gives you complete manual control - you decide when to start AND when to stop recording. Perfect for noisy environments or managing multiple students.

### Configuration Options

Edit [config.yaml](config.yaml) to adjust:

- `silence_threshold`: Higher = less sensitive to background noise (default: 500)
- `silence_duration`: Seconds of silence before stopping recording (default: 2.0)
- `sample_rate`: Audio quality (16000 Hz is standard for speech)
- `chunk_size`: Buffer size for audio processing (default: 1024)

## Troubleshooting

### "Could not understand" errors

- Check your microphone is working
- Increase `silence_threshold` in config.yaml if background noise is too high
- Speak louder or closer to the microphone
- Make sure student speaks for at least 1 second
- Test your microphone with `cd modules && python stt.py`

### PyAudio installation errors

macOS:
```bash
brew install portaudio
pip install --global-option='build_ext' --global-option='-I/opt/homebrew/include' --global-option='-L/opt/homebrew/lib' pyaudio
```

Windows: Download wheel from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

Linux:
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```

### API Key errors

Make sure your OpenAI API key:
- Is correctly pasted in config.yaml (no extra spaces)
- Has billing enabled on your OpenAI account
- Has not exceeded usage limits

## Next Steps

1. Add LLM processing module (OpenAI GPT-4 / Claude)
2. Add Text-to-Speech module
3. Create GUI display for visual feedback
4. Add conversation context/memory
5. Add safety filters for school-appropriate responses

## Credits

Created for school interactive robot project.
