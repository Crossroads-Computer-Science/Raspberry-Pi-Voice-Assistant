from audio import detect_speech
import sounddevice as sd
import numpy as np

SAMPLERATE = 16000  # Samples per second

def main():
    print("🎙 Voice Assistant – Speech Detection")
    print("Speak a sentence, then pause...")

    audio = detect_speech(samplerate=SAMPLERATE)

    print("🛑 Detected silence. Audio captured.")
    print(f"Length: {len(audio)} samples")

    # Optional playback
    print("🔁 Playing back the captured speech...")
    sd.play(audio, samplerate=SAMPLERATE)
    sd.wait()

if __name__ == "__main__":
    main()