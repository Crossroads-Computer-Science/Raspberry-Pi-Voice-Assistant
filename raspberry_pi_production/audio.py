import numpy as np
import sounddevice as sd
import webrtcvad
import threading
import time
from gpiozero import LED
import psutil

# GPIO LED setup for Raspberry Pi (adjust pins as needed)
try:
    LISTENING_LED = LED(17)  # Green LED for listening
    PROCESSING_LED = LED(18)  # Yellow LED for processing
    SPEAKING_LED = LED(27)    # Blue LED for speaking
    GPIO_AVAILABLE = True
except:
    print("⚠️ GPIO not available - running without LED indicators")
    GPIO_AVAILABLE = False

class RaspberryPiAudio:
    def __init__(self, samplerate=16000, channels=1, dtype=np.int16):
        self.samplerate = samplerate
        self.channels = channels
        self.dtype = dtype
        self.vad = webrtcvad.Vad(2)  # Aggressiveness level 2
        self.chunk_duration = 0.03  # 30ms chunks
        self.chunk_size = int(samplerate * self.chunk_duration)
        
        # Audio device configuration optimized for Pi
        self.device_info = sd.query_devices()
        self.default_input = sd.default.device[0]
        
        # Fallback to pygame if sounddevice fails
        self.use_pygame = False
        try:
            sd.check_input_settings(device=self.default_input, 
                                  samplerate=samplerate, 
                                  channels=channels, 
                                  dtype=dtype)
        except:
            print("⚠️ Sounddevice failed, falling back to pygame")
            self.use_pygame = True
            import pygame
            pygame.mixer.init(frequency=samplerate, size=-16, channels=channels)
    
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
            print(f"⚠️ LED control error: {e}")
    
    def detect_speech(self, silence_threshold=2.0, min_speech_duration=0.5):
        """
        Detect speech with Raspberry Pi optimizations.
        
        Args:
            silence_threshold (float): Seconds of silence to stop recording
            min_speech_duration (float): Minimum speech duration to record
            
        Returns:
            numpy.ndarray: Recorded audio data
        """
        print("🎙️ Listening for speech...")
        self.set_led("listening", True)
        
        audio_chunks = []
        silence_start = None
        speech_detected = False
        
        def audio_callback(indata, frames, time, status):
            if status:
                print(f"⚠️ Audio callback status: {status}")
            
            # Convert to proper format for VAD
            audio_data = indata[:, 0].astype(np.int16)
            audio_chunks.append(audio_data.copy())
            
            # Check if this chunk contains speech
            if self.vad.is_speech(audio_data.tobytes(), self.samplerate):
                nonlocal speech_detected, silence_start
                speech_detected = True
                silence_start = None
            elif speech_detected:
                if silence_start is None:
                    silence_start = time.time()
                elif time.time() - silence_start > silence_threshold:
                    raise sd.CallbackStop()
        
        try:
            with sd.InputStream(callback=audio_callback,
                              channels=self.channels,
                              dtype=self.dtype,
                              samplerate=self.samplerate,
                              blocksize=self.chunk_size):
                print("🔴 Recording... (speak now)")
                while True:
                    time.sleep(0.1)
        except sd.CallbackStop:
            pass
        
        self.set_led("listening", False)
        
        if not audio_chunks:
            return np.array([], dtype=self.dtype)
        
        # Concatenate all audio chunks
        audio = np.concatenate(audio_chunks)
        
        # Apply basic noise reduction for Pi
        audio = self._reduce_noise(audio)
        
        print(f"✅ Recorded {len(audio) / self.samplerate:.2f} seconds of audio")
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
        print("🔊 Playing audio...")
        
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
            print(f"❌ Audio playback error: {e}")
        finally:
            self.set_led("speaking", False)
    
    def get_system_info(self):
        """Get Raspberry Pi system information"""
        try:
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
