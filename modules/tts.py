"""
Text-to-Speech Module using ElevenLabs API
Converts text responses to natural speech using Adam's voice
"""

from elevenlabs.client import ElevenLabs
from elevenlabs import play
from typing import Optional
import io


class TTSProcessor:
    """Text-to-Speech processor using ElevenLabs API"""

    def __init__(self, api_key: str, voice_id: str = "pNInz6obpgDQGcFmaJgB",
                 model: str = "eleven_multilingual_v2",
                 output_format: str = "mp3_44100_128"):
        """
        Initialize TTS Processor

        Args:
            api_key: ElevenLabs API key
            voice_id: Voice to use (default: Adam - pNInz6obpgDQGcFmaJgB)
            model: Model to use (default: eleven_multilingual_v2)
            output_format: Audio format (default: mp3_44100_128)
        """
        self.client = ElevenLabs(api_key=api_key)
        self.voice_id = voice_id
        self.model = model
        self.output_format = output_format

        # Voice information
        self.voice_name = "Adam"  # Default voice name

    def speak(self, text: str) -> bool:
        """
        Convert text to speech and play it

        Args:
            text: Text to convert to speech

        Returns:
            True if successful, False otherwise
        """
        if not text or not text.strip():
            print("⚠️  No text to speak")
            return False

        try:
            print(f"🔊 Speaking: {text[:50]}{'...' if len(text) > 50 else ''}")

            # Generate audio using ElevenLabs
            audio = self.client.text_to_speech.convert(
                text=text,
                voice_id=self.voice_id,
                model_id=self.model,
                output_format=self.output_format
            )

            # Play audio directly
            play(audio)

            print("✅ Speech completed")
            return True

        except Exception as e:
            print(f"❌ TTS error: {e}")
            return False

    def speak_stream(self, text: str) -> bool:
        """
        Convert text to speech with streaming (lower latency)

        Args:
            text: Text to convert to speech

        Returns:
            True if successful, False otherwise
        """
        if not text or not text.strip():
            print("⚠️  No text to speak")
            return False

        try:
            print(f"🔊 Speaking (streaming): {text[:50]}{'...' if len(text) > 50 else ''}")

            # Stream audio for faster playback
            audio_stream = self.client.text_to_speech.convert_as_stream(
                text=text,
                voice_id=self.voice_id,
                model_id=self.model,
                output_format=self.output_format
            )

            # Play streamed audio
            play(audio_stream)

            print("✅ Speech completed")
            return True

        except Exception as e:
            print(f"❌ TTS streaming error: {e}")
            # Fallback to regular speak
            print("🔄 Falling back to regular speak method...")
            return self.speak(text)

    def set_voice(self, voice_id: str, voice_name: str = "Custom"):
        """
        Change the voice

        Args:
            voice_id: ElevenLabs voice ID
            voice_name: Human-readable voice name
        """
        self.voice_id = voice_id
        self.voice_name = voice_name
        print(f"🎙️  Voice changed to: {voice_name}")

    def test_voice(self):
        """Test the current voice with a sample message"""
        test_message = f"Hello! I'm {self.voice_name}, your school robot assistant. How can I help you today?"
        return self.speak(test_message)


# Voice presets for easy switching
VOICE_PRESETS = {
    "adam": {
        "id": "pNInz6obpgDQGcFmaJgB",
        "name": "Adam",
        "description": "Clear, professional male voice"
    },
    "rachel": {
        "id": "21m00Tcm4TlvDq8ikWAM",
        "name": "Rachel",
        "description": "Clear, professional female voice"
    },
    "bella": {
        "id": "EXAVITQu4vr4xnSDxMaL",
        "name": "Bella",
        "description": "Warm, friendly female voice"
    },
    "antoni": {
        "id": "ErXwobaYiN019PkySvjV",
        "name": "Antoni",
        "description": "Deep, resonant male voice"
    }
}


# Example usage
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    # Load environment variables
    load_dotenv()
    api_key = os.getenv("ELEVENLABS_API_KEY")

    if not api_key:
        print("❌ Please set ELEVENLABS_API_KEY in .env file")
        exit(1)

    # Initialize TTS
    tts = TTSProcessor(
        api_key=api_key,
        voice_id=VOICE_PRESETS["adam"]["id"]
    )

    print("=" * 50)
    print("🤖 TTS Processor Test")
    print(f"🎙️  Using voice: {tts.voice_name}")
    print("=" * 50)

    # Test with sample text
    test_text = "Hello! I'm your school robot assistant. I can answer questions about science, math, history, and more. What would you like to learn today?"

    print(f"\n📝 Test text: {test_text}\n")

    # Test speaking
    success = tts.speak(test_text)

    if success:
        print("\n✅ TTS module working correctly!")
    else:
        print("\n❌ TTS module test failed")
