from audio import record_audio, play_audio

# Settings
SAMPLERATE = 16000  # 16 kHz
DURATION = 3  # seconds

def main():
    print("Recording...")
    audio = record_audio(seconds=DURATION, samplerate=SAMPLERATE)

    print("Playing back...")
    play_audio(audio, samplerate=SAMPLERATE)

if __name__ == "__main__":
    main()