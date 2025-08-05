import collections
import numpy as np
import sounddevice as sd
import webrtcvad

def audio_stream(samplerate=16000, frame_duration_ms=30):
    frame_size = int(samplerate * frame_duration_ms / 1000)
    with sd.InputStream(samplerate=samplerate, channels=1, dtype='int16') as stream:
        while True:
            audio = stream.read(frame_size)[0].flatten()
            yield audio

def detect_speech(samplerate=16000, frame_duration_ms=30, vad_level=2):
    vad = webrtcvad.Vad(vad_level)
    frame_size = int(samplerate * frame_duration_ms / 1000)
    ring_buffer = collections.deque(maxlen=int(700 / frame_duration_ms))  # ~700 ms of history
    triggered = False
    voiced_frames = []

    for frame in audio_stream(samplerate, frame_duration_ms):
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