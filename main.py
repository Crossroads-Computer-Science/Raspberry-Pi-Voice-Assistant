import collections
import sys
import sounddevice as sd
import webrtcvad
import numpy as np
import scipy.io.wavfile as wav
import tempfile
from openai import OpenAI
import subprocess
import time
import os

# Set your API keys
client = OpenAI(api_key="YOUR_KEY_HERE")

# STT Parameters
samplerate = 16000
frame_duration = 30  # ms
frame_size = int(samplerate * frame_duration / 1000)
vad = webrtcvad.Vad(2)

# Trigger word (optional, can be disabled or removed)
trigger_word = "Jarvis"

def audio_stream():
    with sd.InputStream(samplerate=samplerate, channels=1, dtype='int16') as stream:
        while True:
            audio = stream.read(frame_size)[0].flatten()
            yield audio

def detect_speech():
    ring_buffer = collections.deque(maxlen=int(700 / frame_duration))
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

def transcribe_audio(audio):
    with tempfile.NamedTemporaryFile(suffix=".wav") as temp_wav:
        wav.write(temp_wav.name, samplerate, audio)
        temp_wav.seek(0)
        with open(temp_wav.name, "rb") as f:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                response_format="json"
                )
            return transcript.text

def get_chatgpt_response(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Your name is Jarvis. You are a smart, sarcastic, sardonic, but ultimately helpful voice assistant. You like to add humor wherever possible."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

def speak_text(text, voice="en-us", pitch=50, speed=140):
    try:
        subprocess.run([
            "espeak-ng",
            "-v", voice,
            "-p", str(pitch),
            "-s", str(speed),
            text
        ], check=True)
        print("🔊 Speaking complete.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Speech synthesis failed: {e}")


# Main Loop
last_spoken_text = ""

while True:
    try:
        print("🎙 Listening for speech...")
        audio = detect_speech()
        print("🛑 Detected silence, transcribing...")
        text = transcribe_audio(audio)
        print(f"📝 You said: {text}")

        if trigger_word.lower() in text.lower():
            response = get_chatgpt_response(text)
            print(f"🤖 Jarvis: {response}")

            if response != last_spoken_text:
                speak_text(response)
                last_spoken_text = response
        else:
            print("❌ Trigger word not found. Skipping response.")
        
        print("-" * 60)
        time.sleep(1)

    except KeyboardInterrupt:
        print("👋 Assistant terminated by user.")
        break
