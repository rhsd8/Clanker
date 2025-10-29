"""
Main Robot Controller
Entry point for the interactive school robot
"""
import yaml
import os
from dotenv import load_dotenv
from modules.stt_sounddevice import WhisperSTT
from modules.llm import LLMProcessor
from modules.tts import TTSProcessor


def load_config(config_path: str = "config.yaml") -> dict:
    """Load configuration from YAML file and environment variables"""
    # Load environment variables from .env file
    load_dotenv()

    # Load YAML config
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    # Override API keys with environment variables if available
    env_openai_key = os.getenv("OPENAI_API_KEY")
    if env_openai_key:
        config["openai"]["api_key"] = env_openai_key

    env_openrouter_key = os.getenv("OPENROUTER_API_KEY")
    if env_openrouter_key:
        config["llm"]["api_key"] = env_openrouter_key

    env_elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
    if env_elevenlabs_key:
        config["tts"]["api_key"] = env_elevenlabs_key

    return config


def main():
    """Main robot control loop"""
    print("=" * 50)
    print("🤖 School Robot Assistant Starting...")
    print("=" * 50)

    # Load configuration
    config = load_config()

    # Initialize Speech-to-Text
    stt = WhisperSTT(
        api_key=config["openai"]["api_key"],
        model=config["openai"]["whisper_model"],
        sample_rate=config["audio"]["sample_rate"],
        channels=config["audio"]["channels"],
        silence_threshold=config["audio"]["silence_threshold"],
        silence_duration=config["audio"]["silence_duration"]
    )

    # Initialize LLM Processor
    llm = LLMProcessor(
        api_key=config["llm"]["api_key"],
        model=config["llm"]["model"],
        max_tokens=config["llm"]["max_tokens"],
        temperature=config["llm"]["temperature"],
        system_prompt=config["llm"]["system_prompt"]
    )

    # Initialize Text-to-Speech
    tts = TTSProcessor(
        api_key=config["tts"]["api_key"],
        voice_id=config["tts"]["voice_id"],
        model=config["tts"]["model"],
        output_format=config["tts"]["output_format"]
    )

    try:
        print("\n✅ Robot is ready!")
        print("💡 Recording mode: Press ENTER to START, then ENTER again to STOP")
        print("   Press Ctrl+C to exit\n")

        # Main conversation loop
        while True:
            # Wait for manual trigger to start listening
            print("\n" + "=" * 50)
            input("⏸️  Press ENTER to start listening for next student... ")

            # Step 1: Listen to student's question (press Enter to stop)
            student_input = stt.manual_listen_and_transcribe()

            if not student_input:
                print("⚠️  Could not understand. Please try again.")
                continue

            # Step 2: Send to LLM for processing
            robot_response = llm.generate_response(student_input)

            if not robot_response:
                print("⚠️  Could not generate response. Please try again.")
                continue

            # Step 3: Convert response to speech
            tts.speak(robot_response)

            print("\n✅ Interaction complete! Ready for next student.")

    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down robot...")
    finally:
        stt.cleanup()
        print("👋 Goodbye!")


if __name__ == "__main__":
    main()
