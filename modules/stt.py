"""
Speech-to-Text Module using OpenAI Whisper API
Captures audio from microphone and converts to text
"""

import os
import io
import wave
import pyaudio
import numpy as np
from openai import OpenAI
from typing import Optional
import time
import threading


class WhisperSTT:
    """Speech-to-Text using OpenAI Whisper API"""

    def __init__(self, api_key: str, model: str = "whisper-1",
                 sample_rate: int = 16000, channels: int = 1,
                 chunk_size: int = 1024, silence_threshold: int = 500,
                 silence_duration: float = 2.0):
        """
        Initialize Whisper STT

        Args:
            api_key: OpenAI API key
            model: Whisper model name (default: whisper-1)
            sample_rate: Audio sample rate in Hz
            channels: Number of audio channels (1 for mono)
            chunk_size: Audio chunk size for recording
            silence_threshold: Volume threshold to detect silence
            silence_duration: Seconds of silence before stopping
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.silence_threshold = silence_threshold
        self.silence_duration = silence_duration

        # Initialize PyAudio
        self.audio = pyaudio.PyAudio()

        # Manual recording control
        self.is_recording = False
        self.recording_frames = []
        self.recording_stream = None

    def record_audio(self, max_duration: int = 30) -> bytes:
        """
        Record audio from microphone until silence is detected

        Args:
            max_duration: Maximum recording duration in seconds

        Returns:
            Audio data as bytes
        """
        print("🎤 Listening... Speak now!")

        stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )

        frames = []
        silent_chunks = 0
        chunks_per_second = self.sample_rate / self.chunk_size
        silence_chunks_threshold = int(self.silence_duration * chunks_per_second)
        max_chunks = int(max_duration * chunks_per_second)

        started_speaking = False

        try:
            for i in range(max_chunks):
                data = stream.read(self.chunk_size, exception_on_overflow=False)
                frames.append(data)

                # Convert to numpy array to check volume
                audio_data = np.frombuffer(data, dtype=np.int16)
                volume = np.abs(audio_data).mean()

                # Detect if user started speaking
                if volume > self.silence_threshold:
                    started_speaking = True
                    silent_chunks = 0
                elif started_speaking:
                    silent_chunks += 1

                # Stop if silence detected after speaking
                if started_speaking and silent_chunks > silence_chunks_threshold:
                    print("🔇 Silence detected, processing...")
                    break

        finally:
            stream.stop_stream()
            stream.close()

        # Convert frames to WAV format
        audio_data = b''.join(frames)
        return self._frames_to_wav(audio_data)

    def _frames_to_wav(self, audio_data: bytes) -> bytes:
        """Convert raw audio frames to WAV format"""
        wav_buffer = io.BytesIO()

        with wave.open(wav_buffer, 'wb') as wav_file:
            wav_file.setnchannels(self.channels)
            wav_file.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
            wav_file.setframerate(self.sample_rate)
            wav_file.writeframes(audio_data)

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

        self.recording_stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size,
            stream_callback=self._recording_callback
        )

        self.recording_stream.start_stream()

    def _recording_callback(self, in_data, frame_count, time_info, status):
        """Callback for continuous recording"""
        if self.is_recording:
            self.recording_frames.append(in_data)
            return (in_data, pyaudio.paContinue)
        return (in_data, pyaudio.paComplete)

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
            self.recording_stream.stop_stream()
            self.recording_stream.close()
            self.recording_stream = None

        if not self.recording_frames:
            print("⚠️  No audio data recorded!")
            return None

        # Convert frames to WAV format
        audio_data = b''.join(self.recording_frames)
        self.recording_frames = []

        return self._frames_to_wav(audio_data)

    def manual_listen_and_transcribe(self) -> Optional[str]:
        """
        Manual recording with start/stop control

        User presses Enter to stop recording, or call stop_recording() programmatically

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
                self.recording_stream.stop_stream()
                self.recording_stream.close()
            return None

        audio_data = self.stop_recording()

        if audio_data:
            return self.transcribe(audio_data)
        return None

    def cleanup(self):
        """Clean up audio resources"""
        if self.is_recording:
            self.stop_recording()
        self.audio.terminate()


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

    try:
        # Test recording and transcription
        text = stt.listen_and_transcribe()
        if text:
            print(f"\n✅ Final result: {text}")
        else:
            print("\n❌ Failed to transcribe audio")
    finally:
        stt.cleanup()
