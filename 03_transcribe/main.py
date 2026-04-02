import os
from dotenv import load_dotenv

# Load environment variables from .env BEFORE importing other modules
load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    print("❌ OpenAI API key not found!")
    print("   Create a .env file in this folder containing:")
    print("   OPENAI_API_KEY=your-key-here")
    print("   Get a key at: https://platform.openai.com/api-keys")
    exit(1)

from audio import detect_speech
from chat import transcribe_audio
import sounddevice as sd

SAMPLERATE = 16000

def main():
    print("🎙️ Speak now. The assistant will detect your speech and transcribe it.")

    audio = detect_speech(samplerate=SAMPLERATE)

    print("🛑 Detected silence, sending audio to OpenAI Whisper for transcription...")

    transcription = transcribe_audio(audio, samplerate=SAMPLERATE)

    print(f"📝 Transcription: {transcription}")

    # Optional playback
    print("🔁 Playing back the captured speech...")
    sd.play(audio, samplerate=SAMPLERATE)
    sd.wait()

if __name__ == "__main__":
    main()