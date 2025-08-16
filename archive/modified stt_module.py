modified stt_module.py code: 

import collections
import sys
import sounddevice as sd
import webrtcvad
import numpy as np
import scipy.io.wavfile as wav
import tempfile
import openai

openai.api_key = ""

# Parameters
samplerate = 16000
frame_duration = 30  # ms
frame_size = int(samplerate * frame_duration / 1000)
vad = webrtcvad.Vad(2)  # 0-3, higher = more aggressive

trigger_word = "Ben"  # Trigger word to activate ChatGPT

def audio_stream():
    with sd.InputStream(samplerate=samplerate, channels=1, dtype='int16') as stream:
        while True:
            audio = stream.read(frame_size)[0].flatten()
            yield audio

def detect_speech():
    ring_buffer = collections.deque(maxlen=int(400 / frame_duration))
    triggered = False
    voiced_frames = []

    for frame in audio_stream():
        is_speech = vad.is_speech(frame.tobytes(), samplerate)
        if not triggered:
            ring_buffer.append(frame)
            num_voiced = len([f for f in ring_buffer if vad.is_speech(f.tobytes(), samplerate)])
            if num_voiced > 0.9 * ring_buffer.maxlen:
                triggered = True
                voiced_frames.extend(ring_buffer)
                ring_buffer.clear()
        else:
            voiced_frames.append(frame)
            ring_buffer.append(frame)
            num_unvoiced = len([f for f in ring_buffer if not vad.is_speech(f.tobytes(), samplerate)])
            if num_unvoiced > 0.9 * ring_buffer.maxlen:
                break

    return np.concatenate(voiced_frames)

while True:
    print("🎙 Listening for speech...")
    audio = detect_speech()
    print("🛑 Detected silence, transcribing...")

    with tempfile.NamedTemporaryFile(suffix=".wav") as temp_wav:
        wav.write(temp_wav.name, samplerate, audio)
        temp_wav.seek(0)
        with open(temp_wav.name, "rb") as f:
            transcript = openai.Audio.transcribe("whisper-1", f)
            text = transcript["text"]
            print("📝 You said:", text)

            # Check if trigger word is present
            if trigger_word.lower() in text.lower():
                with open("transcription.txt", "a") as file:
                    file.write(text + "\n")
                print("✅ Transcription saved to transcription.txt")
            else:
                print("❌ Trigger word not found. Nothing saved.")
            
    print("-" * 50)
