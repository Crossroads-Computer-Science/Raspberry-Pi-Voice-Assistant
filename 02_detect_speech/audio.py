import collections
import numpy as np
import sounddevice as sd
import webrtcvad


def audio_stream(samplerate=16000, frame_duration_ms=30):
    """Generator that yields one 30ms chunk of audio at a time from the microphone."""
    frame_size = int(samplerate * frame_duration_ms / 1000)
    with sd.InputStream(samplerate=samplerate, channels=1, dtype='int16') as stream:
        while True:
            audio = stream.read(frame_size)[0].flatten()
            yield audio


def detect_speech(samplerate=16000, frame_duration_ms=30, vad_level=2):
    """
    Listen continuously and return one complete spoken utterance as a numpy array.

    How the ring buffer works:
    - We keep a sliding window (ring_buffer) of the last ~700ms of audio frames.
    - BEFORE speech starts: we wait until 90% of the buffer is flagged as voiced.
      This prevents us from missing the start of a word.
    - AFTER speech starts: we keep recording until 90% of the buffer is silence.
      This gives a natural pause before cutting off.
    """
    vad = webrtcvad.Vad(vad_level)  # vad_level 0-3: higher = more aggressive filtering
    ring_buffer = collections.deque(maxlen=int(700 / frame_duration_ms))  # ~700ms window
    triggered = False   # True once we've confirmed speech has started
    voiced_frames = []  # All frames that will make up the final audio clip

    for frame in audio_stream(samplerate, frame_duration_ms):

        if not triggered:
            # Waiting for speech to begin — fill the ring buffer and watch for voiced frames
            ring_buffer.append(frame)
            num_voiced = len([f for f in ring_buffer if vad.is_speech(f.tobytes(), samplerate)])
            if num_voiced > 0.9 * ring_buffer.maxlen:
                # Enough speech detected — lock in and include the buffered lead-in frames
                triggered = True
                voiced_frames.extend(ring_buffer)
                ring_buffer.clear()
        else:
            # Recording speech — watch for sustained silence to know when the speaker stopped
            voiced_frames.append(frame)
            ring_buffer.append(frame)
            num_unvoiced = len([f for f in ring_buffer if not vad.is_speech(f.tobytes(), samplerate)])
            if num_unvoiced > 0.9 * ring_buffer.maxlen:
                break  # Sustained silence detected — the speaker has finished

    return np.concatenate(voiced_frames)
