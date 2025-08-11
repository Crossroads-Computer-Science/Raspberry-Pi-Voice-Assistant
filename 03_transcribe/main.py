import os
from dotenv import load_dotenv

# Load environment variables from .env BEFORE importing other modules
load_dotenv()

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