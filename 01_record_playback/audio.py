import sounddevice as sd
import numpy as np

def record_audio(seconds: int = 3, samplerate: int = 16000) -> np.ndarray:
    audio = sd.rec(int(seconds * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    return audio.flatten()

def play_audio(audio: np.ndarray, samplerate: int = 16000):
    sd.play(audio, samplerate=samplerate)
    sd.wait()