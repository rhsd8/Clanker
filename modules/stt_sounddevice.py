"""
Speech-to-Text Module using OpenAI Whisper API
Captures audio from microphone and converts to text
Uses sounddevice (easier to install on macOS than PyAudio)
"""

import io
import wave
import sounddevice as sd
import numpy as np
from openai import OpenAI
from typing import Optional
import queue
import threading


class WhisperSTT:
    """Speech-to-Text using OpenAI Whisper API with sounddevice"""

    def __init__(self, api_key: str, model: str = "whisper-1",
                 sample_rate: int = 16000, channels: int = 1,
                 silence_threshold: int = 500,
                 silence_duration: float = 2.0):
        """
        Initialize Whisper STT

        Args:
            api_key: OpenAI API key
            model: Whisper model name (default: whisper-1)
            sample_rate: Audio sample rate in Hz
            channels: Number of audio channels (1 for mono)
            silence_threshold: Volume threshold to detect silence
            silence_duration: Seconds of silence before stopping
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.sample_rate = sample_rate
        self.channels = channels
        self.silence_threshold = silence_threshold
        self.silence_duration = silence_duration

        # Manual recording control
        self.is_recording = False
        self.recording_frames = []
        self.audio_queue = queue.Queue()

    def record_audio(self, max_duration: int = 30, on_stop_callback=None) -> bytes:
        """
        Record audio from microphone until silence is detected

        Args:
            max_duration: Maximum recording duration in seconds
            on_stop_callback: Optional callback to call when recording stops

        Returns:
            Audio data as bytes (WAV format)
        """
        print("🎤 Listening... Speak now!")

        frames = []
        silence_chunks = 0
        chunks_per_second = self.sample_rate / 1024  # Using 1024 as blocksize
        silence_chunks_threshold = int(self.silence_duration * chunks_per_second)
        started_speaking = False

        def audio_callback(indata, frames_count, time_info, status):
            """Callback for sounddevice"""
            if status:
                print(f"Audio status: {status}")
            frames.append(indata.copy())

        # Start recording
        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            callback=audio_callback,
            blocksize=1024,
            dtype='int16'
        ):
            # Record for max duration or until silence
            total_chunks = int(max_duration * chunks_per_second)

            for i in range(total_chunks):
                sd.sleep(int(1000 / chunks_per_second))  # Sleep in milliseconds

                if len(frames) > 0:
                    # Check volume of latest chunk
                    volume = np.abs(frames[-1]).mean()

                    if volume > self.silence_threshold:
                        started_speaking = True
                        silence_chunks = 0
                    elif started_speaking:
                        silence_chunks += 1

                    # Stop if silence detected after speaking
                    if started_speaking and silence_chunks > silence_chunks_threshold:
                        print("🔇 Silence detected, processing...")
                        # Call callback before returning
                        if on_stop_callback:
                            on_stop_callback()
                        break

        if not frames:
            print("⚠️  No audio recorded!")
            return self._frames_to_wav(np.array([], dtype='int16'))

        # Concatenate all frames
        audio_data = np.concatenate(frames, axis=0)
        return self._frames_to_wav(audio_data)

    def _frames_to_wav(self, audio_data: np.ndarray) -> bytes:
        """Convert numpy audio data to WAV format"""
        wav_buffer = io.BytesIO()

        with wave.open(wav_buffer, 'wb') as wav_file:
            wav_file.setnchannels(self.channels)
            wav_file.setsampwidth(2)  # 16-bit audio = 2 bytes
            wav_file.setframerate(self.sample_rate)
            wav_file.writeframes(audio_data.tobytes())

        wav_buffer.seek(0)
        return wav_buffer.read()

    def transcribe(self, audio_data: bytes) -> Optional[str]:
        """
        Transcribe audio using OpenAI Whisper API

        Args:
            audio_data: Audio data in WAV format

        Returns:
            Transcribed text or None if error
        """
        try:
            # Create a file-like object from audio data
            audio_file = io.BytesIO(audio_data)
            audio_file.name = "audio.wav"

            # Send to Whisper API
            print("🔄 Transcribing audio...")
            transcript = self.client.audio.transcriptions.create(
                model=self.model,
                file=audio_file,
                language="en"  # Can be auto-detected or changed
            )

            text = transcript.text.strip()
            print(f"📝 Transcribed: {text}")
            return text

        except Exception as e:
            print(f"❌ Transcription error: {e}")
            return None

    def listen_and_transcribe(self, max_duration: int = 30) -> Optional[str]:
        """
        Record audio and transcribe in one step

        Args:
            max_duration: Maximum recording duration in seconds

        Returns:
            Transcribed text or None if error
        """
        audio_data = self.record_audio(max_duration)
        return self.transcribe(audio_data)

    def start_recording(self):
        """Start manual recording - call stop_recording() to finish"""
        if self.is_recording:
            print("⚠️  Already recording!")
            return

        print("🎤 Recording started... Press Enter or call stop_recording() to stop")
        self.is_recording = True
        self.recording_frames = []

        def audio_callback(indata, frames_count, time_info, status):
            """Callback for continuous recording"""
            if self.is_recording:
                self.recording_frames.append(indata.copy())

        self.recording_stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            callback=audio_callback,
            blocksize=1024,
            dtype='int16'
        )
        self.recording_stream.start()

    def stop_recording(self) -> Optional[bytes]:
        """
        Stop manual recording and return audio data

        Returns:
            Audio data in WAV format or None if no recording active
        """
        if not self.is_recording:
            print("⚠️  No active recording!")
            return None

        print("🔇 Recording stopped, processing...")
        self.is_recording = False

        if self.recording_stream:
            self.recording_stream.stop()
            self.recording_stream.close()
            self.recording_stream = None

        if not self.recording_frames:
            print("⚠️  No audio data recorded!")
            return None

        # Concatenate all frames
        audio_data = np.concatenate(self.recording_frames, axis=0)
        self.recording_frames = []

        return self._frames_to_wav(audio_data)

    def manual_listen_and_transcribe(self, on_stop_callback=None) -> Optional[str]:
        """
        Manual recording with start/stop control

        User presses Enter to stop recording

        Args:
            on_stop_callback: Optional callback function to call when recording stops
                             (before transcription starts)

        Returns:
            Transcribed text or None if error
        """
        self.start_recording()

        # Wait for user to press Enter
        try:
            input("\n⏸️  Press ENTER to stop recording...\n")
        except KeyboardInterrupt:
            print("\n⚠️  Recording cancelled")
            self.is_recording = False
            if self.recording_stream:
                self.recording_stream.stop()
                self.recording_stream.close()
            return None

        audio_data = self.stop_recording()

        # Call the callback immediately after stopping (before transcription)
        if on_stop_callback:
            on_stop_callback()

        if audio_data:
            return self.transcribe(audio_data)
        return None

    def cleanup(self):
        """Clean up audio resources"""
        if self.is_recording:
            self.stop_recording()

    def list_devices(self):
        """List all available audio input devices"""
        print("\n🎤 Available audio input devices:")
        print(sd.query_devices())


# Example usage
if __name__ == "__main__":
    import yaml

    # Load config
    with open("../config.yaml", "r") as f:
        config = yaml.safe_load(f)

    # Initialize STT
    stt = WhisperSTT(
        api_key=config["openai"]["api_key"],
        model=config["openai"]["whisper_model"],
        sample_rate=config["audio"]["sample_rate"],
        silence_threshold=config["audio"]["silence_threshold"],
        silence_duration=config["audio"]["silence_duration"]
    )

    # List available devices
    stt.list_devices()

    try:
        # Test recording and transcription
        print("\n" + "=" * 50)
        text = stt.listen_and_transcribe()
        if text:
            print(f"\n✅ Final result: {text}")
        else:
            print("\n❌ Failed to transcribe audio")
    finally:
        stt.cleanup()
