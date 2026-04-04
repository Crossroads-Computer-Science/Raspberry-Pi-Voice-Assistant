import collections
import numpy as np
import sounddevice as sd
import webrtcvad

def detect_speech(samplerate=16000, frame_duration=30):
    """
    Record audio until silence is detected.
    
    Args:
        samplerate (int): Audio sample rate in Hz
        frame_duration (int): Duration of each audio frame in milliseconds
        
    Returns:
        numpy.ndarray: Recorded audio data
    """
    # Calculate frame size based on sample rate and duration
    frame_size = int(samplerate * frame_duration / 1000)
    
    # Initialize Voice Activity Detection (VAD)
    vad = webrtcvad.Vad(2)  # Aggressiveness mode 2 (0-3)
    
    # Create a ring buffer to store recent audio frames
    ring_buffer = collections.deque(maxlen=int(700 / frame_duration))  # ~700ms buffer
    
    # Initialize variables for speech detection
    triggered = False  # True when speech is detected
    voiced_frames = []  # Store frames containing speech
    
    # Open audio input stream
    with sd.InputStream(samplerate=samplerate, channels=1, dtype='int16') as stream:
        print(" Listening...")
        
        while True:
            # Read one frame of audio
            audio = stream.read(frame_size)[0].flatten()
            
            # Check if frame contains speech
            is_speech = vad.is_speech(audio.tobytes(), samplerate)
            
            if not triggered:
                # Not yet triggered, add frame to ring buffer
                ring_buffer.append(audio)
                
                # Count frames in buffer that contain speech
                num_voiced = len([f for f in ring_buffer 
                                if vad.is_speech(f.tobytes(), samplerate)])
                
                # Trigger if enough speech frames are detected
                if num_voiced > 0.9 * ring_buffer.maxlen:
                    triggered = True
                    voiced_frames.extend(ring_buffer)
                    ring_buffer.clear()
            else:
                # Already triggered, keep adding speech frames
                voiced_frames.append(audio)
                ring_buffer.append(audio)
                
                # Count frames in buffer that don't contain speech
                num_unvoiced = len([f for f in ring_buffer 
                                  if not vad.is_speech(f.tobytes(), samplerate)])
                
                # Stop if enough silence is detected
                if num_unvoiced > 0.9 * ring_buffer.maxlen:
                    break
    
    # Combine all speech frames into one array
    return np.concatenate(voiced_frames)
