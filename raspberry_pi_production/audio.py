import sounddevice as sd
import webrtcvad
import numpy as np
import collections
import time

# GPIO setup (if available)
GPIO_AVAILABLE = False
try:
    from gpiozero import LED
    LISTENING_LED = LED(17)  # Green LED for listening
    PROCESSING_LED = LED(27)  # Yellow LED for processing
    SPEAKING_LED = LED(22)    # Red LED for speaking
    GPIO_AVAILABLE = True
except ImportError:
    print(" GPIO not available - LED indicators disabled")

class RaspberryPiAudio:
    def __init__(self, samplerate=16000, channels=1, dtype=np.int16):
        self.samplerate = samplerate
        self.channels = channels
        self.dtype = dtype
        
        # Initialize VAD with error handling
        try:
            self.vad = webrtcvad.Vad(2)  # Aggressiveness level 2
            print(" VAD initialized successfully")
        except Exception as e:
            print(f" VAD initialization failed: {e}")
            self.vad = None
            
        # Audio device configuration optimized for Pi
        try:
            self.device_info = sd.query_devices()
            self.default_input = sd.default.device[0]
            print(f" Audio device: {self.default_input}")
        except Exception as e:
            print(f" Could not query audio devices: {e}")
            self.default_input = None
        
        # Fallback to pygame if sounddevice fails
        self.use_pygame = False
        try:
            if self.default_input is not None:
                sd.check_input_settings(device=self.default_input, 
                                      samplerate=samplerate, 
                                      channels=channels, 
                                      dtype=dtype)
                print(" Sounddevice audio settings verified")
            else:
                raise Exception("No audio device available")
        except Exception as e:
            print(f" Sounddevice failed: {e}")
            print(" Falling back to pygame")
            self.use_pygame = True
            try:
                import pygame
                pygame.mixer.init(frequency=samplerate, size=-16, channels=channels)
                print(" Pygame audio backend initialized")
            except Exception as pygame_error:
                print(f" Pygame fallback also failed: {pygame_error}")
    
    def set_led(self, led_name, state):
        """Set LED state with error handling"""
        if not GPIO_AVAILABLE:
            return
            
        try:
            if led_name == "listening":
                LISTENING_LED.on() if state else LISTENING_LED.off()
            elif led_name == "processing":
                PROCESSING_LED.on() if state else PROCESSING_LED.off()
            elif led_name == "speaking":
                SPEAKING_LED.on() if state else SPEAKING_LED.off()
        except Exception as e:
            print(f" LED control error: {e}")
    
    def detect_speech(self, silence_threshold=2.0, min_speech_duration=0.5):
        """
        Detect speech using the working ring buffer approach from archive.
        
        Args:
            silence_threshold (float): Seconds of silence to stop recording
            min_speech_duration (float): Minimum speech duration to record
            
        Returns:
            numpy.ndarray: Recorded audio data
        """
        print(" Listening for speech...")
        self.set_led("listening", True)
        
        # Use the working approach from archive
        frame_duration = 30  # ms
        frame_size = int(self.samplerate * frame_duration / 1000)
        
        def audio_stream():
            """Simple audio stream using the working approach"""
            with sd.InputStream(samplerate=self.samplerate, channels=self.channels, dtype=self.dtype) as stream:
                while True:
                    try:
                        audio = stream.read(frame_size)[0].flatten()
                        yield audio
                    except Exception as e:
                        print(f" Audio stream read error: {e}")
                        break
        
        # Ring buffer approach (working method from archive)
        ring_buffer = collections.deque(maxlen=int(700 / frame_duration))
        triggered = False
        voiced_frames = []
        
        try:
            for frame in audio_stream():
                if self.vad is not None:
                    is_speech = self.vad.is_speech(frame.tobytes(), self.samplerate)
                else:
                    # If VAD not available, assume all frames are speech
                    is_speech = True
                
                if not triggered:
                    ring_buffer.append(frame)
                    if self.vad is not None:
                        num_voiced = len([f for f in ring_buffer if self.vad.is_speech(f.tobytes(), self.samplerate)])
                        if num_voiced > 0.9 * ring_buffer.maxlen:
                            triggered = True
                            voiced_frames.extend(ring_buffer)
                            ring_buffer.clear()
                    else:
                        # Simple trigger after some frames
                        if len(ring_buffer) > 10:
                            triggered = True
                            voiced_frames.extend(ring_buffer)
                            ring_buffer.clear()
                else:
                    voiced_frames.append(frame)
                    ring_buffer.append(frame)
                    if self.vad is not None:
                        num_unvoiced = len([f for f in ring_buffer if not self.vad.is_speech(f.tobytes(), self.samplerate)])
                        if num_unvoiced > 0.9 * ring_buffer.maxlen:
                            break
                    else:
                        # Simple timeout
                        if len(voiced_frames) > self.samplerate * 5:  # 5 seconds max
                            break
                            
        except KeyboardInterrupt:
            print(" Recording interrupted by user")
        except Exception as e:
            print(f" Speech detection error: {e}")
        
        self.set_led("listening", False)
        
        if not voiced_frames:
            print(" No audio recorded")
            return np.array([], dtype=self.dtype)
        
        # Concatenate all audio frames
        audio = np.concatenate(voiced_frames)
        
        # Apply basic noise reduction for Pi
        audio = self._reduce_noise(audio)
        
        print(f" Recorded {len(audio) / self.samplerate:.2f} seconds of audio")
        return audio
    
    def _reduce_noise(self, audio, threshold=0.01):
        """Simple noise reduction optimized for Pi performance"""
        # Calculate RMS of audio
        rms = np.sqrt(np.mean(audio.astype(np.float32)**2))
        
        # Apply threshold-based noise gate
        if rms < threshold:
            audio = audio * 0.1  # Reduce very quiet sections
        
        return audio
    
    def play_audio(self, audio, blocking=True):
        """Play audio with LED indicator"""
        self.set_led("speaking", True)
        print(" Playing audio...")
        
        try:
            if self.use_pygame:
                # Use pygame as fallback
                import pygame
                pygame.mixer.music.load(audio)
                pygame.mixer.music.play()
                if blocking:
                    while pygame.mixer.music.get_busy():
                        pygame.time.wait(100)
            else:
                # Use sounddevice
                sd.play(audio, self.samplerate)
                if blocking:
                    sd.wait()
        except Exception as e:
            print(f" Audio playback error: {e}")
        finally:
            self.set_led("speaking", False)
    
    def get_system_info(self):
        """Get Raspberry Pi system information"""
        try:
            import psutil
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            temperature = self._get_cpu_temperature()
            
            return {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "temperature": temperature,
                "audio_device": self.default_input
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _get_cpu_temperature(self):
        """Get CPU temperature (Raspberry Pi specific)"""
        try:
            with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
                temp = float(f.read()) / 1000.0
                return temp
        except:
            return None

# Convenience function for backward compatibility
def detect_speech(samplerate=16000, **kwargs):
    """Legacy function for backward compatibility"""
    audio_handler = RaspberryPiAudio(samplerate=samplerate)
    return audio_handler.detect_speech(**kwargs)
