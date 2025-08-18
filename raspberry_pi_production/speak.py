import subprocess
import tempfile
import os
from gpiozero import LED
import threading
import time

# GPIO LED setup (same as audio.py)
try:
    SPEAKING_LED = LED(27)  # Blue LED for speaking
    GPIO_AVAILABLE = True
except:
    print("⚠️ GPIO not available - running without LED indicators")
    GPIO_AVAILABLE = False

class RaspberryPiSpeech:
    def __init__(self, voice="Alex", rate=300):
        self.voice = voice
        self.rate = rate  # Default rate increased for faster speech
        self.speaking = False
        
        # Speed presets for different use cases
        self.speed_presets = {
            "slow": 200,      # Very clear, good for learning
            "normal": 300,    # Balanced speed and clarity
            "fast": 400,      # Quick responses
            "very_fast": 500  # Rapid responses (may reduce clarity)
        }
        
        # Try to detect available TTS backends
        self.backends = self._detect_backends()
        print(f"🎤 Available TTS backends: {list(self.backends.keys())}")
    
    def _detect_backends(self):
        """Detect available text-to-speech backends on the system"""
        backends = {}
        
        # Check for macOS 'say' command
        try:
            subprocess.run(["say", "--help"], capture_output=True, check=True)
            backends["macos_say"] = True
        except:
            backends["macos_say"] = False
        
        # Check for espeak (common on Linux/Raspberry Pi)
        try:
            subprocess.run(["espeak", "--help"], capture_output=True, check=True)
            backends["espeak"] = True
        except:
            backends["espeak"] = False
        
        # Check for festival
        try:
            subprocess.run(["festival", "--help"], capture_output=True, check=True)
            backends["festival"] = True
        except:
            backends["festival"] = False
        
        # Check for gTTS (Google Text-to-Speech)
        try:
            import gtts
            backends["gtts"] = True
        except ImportError:
            backends["gtts"] = False
        
        return backends
    
    def set_led(self, state):
        """Set speaking LED state"""
        if not GPIO_AVAILABLE:
            return
            
        try:
            if state:
                SPEAKING_LED.on()
            else:
                SPEAKING_LED.off()
        except Exception as e:
            print(f"⚠️ LED control error: {e}")
    
    def speak_text(self, text, voice=None, rate=None):
        """
        Convert text to speech using the best available backend.
        
        Args:
            text (str): Text to convert to speech
            voice (str): Voice to use (backend-specific)
            rate (int): Speech rate (backend-specific)
        """
        if not text or not text.strip():
            return
        
        voice = voice or self.voice
        rate = rate or self.rate
        
        print(f"🔊 Speaking: {text[:50]}{'...' if len(text) > 50 else ''}")
        self.set_led(True)
        self.speaking = True
        
        try:
            # Try backends in order of preference
            if self.backends.get("espeak"):
                self._speak_espeak(text, voice, rate)
            elif self.backends.get("macos_say"):
                self._speak_macos(text, voice, rate)
            elif self.backends.get("festival"):
                self._speak_festival(text)
            elif self.backends.get("gtts"):
                self._speak_gtts(text)
            else:
                print("❌ No TTS backend available")
                return False
                
            print("✅ Speech synthesis complete")
            return True
            
        except Exception as e:
            print(f"❌ Speech synthesis failed: {e}")
            return False
        finally:
            self.set_led(False)
            self.speaking = False
    
    def _speak_espeak(self, text, voice, rate):
        """Use espeak (common on Raspberry Pi) with optimized settings"""
        try:
            # espeak command with Raspberry Pi optimizations
            cmd = [
                "espeak",
                "-v", voice if voice != "Alex" else "en",
                "-s", str(rate),
                "--punct=some",  # Say some punctuation
                "-g", "5",       # Word gap (0-10, lower = faster)
                "-k", "5",       # Emphasis (0-20, lower = less emphasis, faster)
                text
            ]
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ espeak failed: {e}")
            raise
    
    def _speak_macos(self, text, voice, rate):
        """Use macOS 'say' command"""
        try:
            subprocess.run([
                "say",
                "-v", voice,
                "-r", str(rate),
                text
            ], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ macOS say failed: {e}")
            raise
    
    def _speak_festival(self, text):
        """Use festival TTS"""
        try:
            # Create a temporary script file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.scm', delete=False) as f:
                f.write(f'(SayText "{text}")')
                script_file = f.name
            
            # Run festival with the script
            subprocess.run(["festival", script_file], check=True)
            
            # Clean up
            os.unlink(script_file)
        except Exception as e:
            print(f"❌ Festival failed: {e}")
            raise
    
    def _speak_gtts(self, text):
        """Use Google Text-to-Speech (requires internet)"""
        try:
            from gtts import gTTS
            import pygame
            
            # Create temporary audio file
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
                temp_file = f.name
            
            # Generate speech
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(temp_file)
            
            # Play audio with pygame
            pygame.mixer.init()
            pygame.mixer.music.load(temp_file)
            pygame.mixer.music.play()
            
            # Wait for completion
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            # Clean up
            pygame.mixer.quit()
            os.unlink(temp_file)
            
        except Exception as e:
            print(f"❌ gTTS failed: {e}")
            raise
    
    def set_speed(self, speed_preset):
        """Set speech speed using predefined presets"""
        if speed_preset in self.speed_presets:
            self.rate = self.speed_presets[speed_preset]
            print(f"🎤 Speech speed set to: {speed_preset} ({self.rate})")
            return True
        else:
            print(f"❌ Invalid speed preset. Available: {list(self.speed_presets.keys())}")
            return False
    
    def set_custom_rate(self, rate):
        """Set custom speech rate (150-600 recommended)"""
        if 150 <= rate <= 600:
            self.rate = rate
            print(f"🎤 Custom speech rate set to: {rate}")
            return True
        else:
            print(f"❌ Rate must be between 150-600. Current: {rate}")
            return False
    
    def get_current_speed(self):
        """Get current speed preset name"""
        for name, rate in self.speed_presets.items():
            if rate == self.rate:
                return name
        return f"custom ({self.rate})"
    
    def speak_async(self, text, voice=None, rate=None):
        """Speak text asynchronously (non-blocking)"""
        thread = threading.Thread(
            target=self.speak_text,
            args=(text, voice, rate)
        )
        thread.daemon = True
        thread.start()
        return thread
    
    def stop_speaking(self):
        """Stop current speech (if possible)"""
        self.speaking = False
        self.set_led(False)
        print("⏹️ Speech stopped")
    
    def get_available_voices(self):
        """Get list of available voices for current backend"""
        voices = []
        
        if self.backends.get("espeak"):
            try:
                result = subprocess.run(["espeak", "--voices"], 
                                      capture_output=True, text=True, check=True)
                # Parse espeak voices output
                for line in result.stdout.split('\n'):
                    if line.strip() and not line.startswith('Pty'):
                        parts = line.split()
                        if len(parts) >= 4:
                            voices.append(parts[3])
            except:
                pass
        
        elif self.backends.get("macos_say"):
            try:
                result = subprocess.run(["say", "-v", "?"], 
                                      capture_output=True, text=True, check=True)
                # Parse macOS voices output
                for line in result.stdout.split('\n'):
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 1:
                            voices.append(parts[0])
            except:
                pass
        
        return voices[:10] if voices else ["default"]  # Limit to first 10

# Convenience function for backward compatibility
def speak_text(text, voice="Alex", rate=300):
    """Legacy function for backward compatibility"""
    speech_handler = RaspberryPiSpeech(voice=voice, rate=rate)
    return speech_handler.speak_text(text, voice, rate)
