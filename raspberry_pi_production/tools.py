import requests
import datetime
import time
import threading
import subprocess
import psutil
from gpiozero import LED, Button
import json

# GPIO setup for Raspberry Pi
try:
    # LEDs for different states
    STATUS_LED = LED(22)      # Status indicator
    TIMER_LED = LED(23)       # Timer indicator
    WEATHER_LED = LED(24)     # Weather indicator
    
    # Button for manual trigger (optional)
    TRIGGER_BUTTON = Button(25, pull_up=True)
    GPIO_AVAILABLE = True
except:
    print("⚠️ GPIO not available - running without hardware indicators")
    GPIO_AVAILABLE = False

class RaspberryPiTools:
    def __init__(self):
        self.timers = {}  # Store active timers
        self.timer_counter = 0
        
        if GPIO_AVAILABLE:
            self._setup_gpio()
    
    def _setup_gpio(self):
        """Setup GPIO pins and event handlers"""
        try:
            # Blink status LED to show system is ready
            STATUS_LED.blink(on_time=0.5, off_time=0.5, n=3)
            
            # Setup button handler
            TRIGGER_BUTTON.when_pressed = self._button_pressed
            print("✅ GPIO setup complete")
        except Exception as e:
            print(f"⚠️ GPIO setup error: {e}")
    
    def _button_pressed(self):
        """Handle button press events"""
        print("🔘 Manual trigger button pressed!")
        # This could be used to manually activate the assistant
    
    def set_led(self, led_name, state):
        """Set LED state with error handling"""
        if not GPIO_AVAILABLE:
            return
            
        try:
            if led_name == "status":
                STATUS_LED.on() if state else STATUS_LED.off()
            elif led_name == "timer":
                TIMER_LED.on() if state else TIMER_LED.off()
            elif led_name == "weather":
                WEATHER_LED.on() if state else WEATHER_LED.off()
        except Exception as e:
            print(f"⚠️ LED control error: {e}")
    
    def get_system_status(self) -> dict:
        """
        Get comprehensive Raspberry Pi system status.
        
        Returns:
            dict: System information including CPU, memory, temperature, etc.
        """
        try:
            # Basic system info
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Network info
            network = psutil.net_io_counters()
            
            # Temperature (Raspberry Pi specific)
            temperature = self._get_cpu_temperature()
            
            # Uptime
            uptime = time.time() - psutil.boot_time()
            
            status = {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_available_gb": round(memory.available / (1024**3), 2),
                "disk_percent": disk.percent,
                "disk_free_gb": round(disk.free / (1024**3), 2),
                "network_bytes_sent": network.bytes_sent,
                "network_bytes_recv": network.bytes_recv,
                "temperature_celsius": temperature,
                "uptime_hours": round(uptime / 3600, 2),
                "timestamp": datetime.datetime.now().isoformat()
            }
            
            # Set status LED based on system health
            if GPIO_AVAILABLE:
                if cpu_percent > 80 or memory.percent > 90:
                    self.set_led("status", True)  # Warning state
                else:
                    self.set_led("status", False)  # Normal state
            
            return status
            
        except Exception as e:
            return {"error": f"Failed to get system status: {str(e)}"}
    
    def _get_cpu_temperature(self) -> float:
        """Get CPU temperature from Raspberry Pi thermal sensor"""
        try:
            with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
                temp = float(f.read()) / 1000.0
                return round(temp, 1)
        except:
            return None
    
    def get_weather(self, latitude: float, longitude: float) -> dict:
        """
        Get current weather data with enhanced error handling and caching.
        
        Args:
            latitude (float): Latitude coordinate
            longitude (float): Longitude coordinate
            
        Returns:
            dict: Weather data including temperature and conditions
        """
        try:
            self.set_led("weather", True)
            
            # Make API request to Open-Meteo (free, no API key required)
            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "current": ["temperature_2m", "wind_speed_10m", "weather_code", "relative_humidity_2m"],
                "hourly": ["precipitation_probability", "weather_code"],
                "timezone": "auto"
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Extract current weather data
            current = data["current"]
            
            # Get weather description from code
            weather_description = self._get_weather_description(current["weather_code"])
            
            weather_data = {
                "temperature_celsius": current["temperature_2m"],
                "temperature_fahrenheit": round(current["temperature_2m"] * 9/5 + 32, 1),
                "wind_speed_kmh": current["wind_speed_10m"],
                "wind_speed_mph": round(current["wind_speed_10m"] * 0.621371, 1),
                "weather_code": current["weather_code"],
                "weather_description": weather_description,
                "humidity_percent": current.get("relative_humidity_2m", "N/A"),
                "location": f"{latitude:.2f}, {longitude:.2f}"
            }
            
            print(f"🌤️ Weather retrieved: {weather_description}, {weather_data['temperature_celsius']}°C")
            return weather_data
            
        except requests.exceptions.Timeout:
            return {"error": "Weather API request timed out"}
        except requests.exceptions.RequestException as e:
            return {"error": f"Weather API request failed: {str(e)}"}
        except Exception as e:
            return {"error": f"Error getting weather data: {str(e)}"}
        finally:
            self.set_led("weather", False)
    
    def _get_weather_description(self, code: int) -> str:
        """Convert weather code to human-readable description"""
        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Slight snow",
            73: "Moderate snow",
            75: "Heavy snow",
            95: "Thunderstorm"
        }
        return weather_codes.get(code, f"Unknown weather (code {code})")
    
    def get_time(self) -> dict:
        """
        Get current time and date information.
        
        Returns:
            dict: Time and date information
        """
        now = datetime.datetime.now()
        
        time_info = {
            "time_12h": now.strftime("%I:%M %p"),
            "time_24h": now.strftime("%H:%M"),
            "date": now.strftime("%B %d, %Y"),
            "day_of_week": now.strftime("%A"),
            "timezone": now.astimezone().tzname(),
            "timestamp": now.isoformat()
        }
        
        return time_info
    
    def set_timer(self, minutes: float, description: str = "") -> dict:
        """
        Set a timer with enhanced features.
        
        Args:
            minutes (float): Number of minutes for the timer
            description (str): Optional description of the timer
            
        Returns:
            dict: Timer information and confirmation
        """
        try:
            if minutes <= 0:
                return {"error": "Timer duration must be positive"}
            
            timer_id = self.timer_counter
            self.timer_counter += 1
            
            # Create timer thread
            timer_thread = threading.Thread(
                target=self._timer_alert,
                args=(timer_id, minutes, description),
                daemon=True
            )
            
            # Store timer info
            self.timers[timer_id] = {
                "thread": timer_thread,
                "start_time": time.time(),
                "duration_minutes": minutes,
                "description": description,
                "active": True
            }
            
            # Start timer
            timer_thread.start()
            
            # Set timer LED
            if GPIO_AVAILABLE:
                self.set_led("timer", True)
            
            timer_info = {
                "timer_id": timer_id,
                "duration_minutes": minutes,
                "description": description,
                "start_time": datetime.datetime.now().isoformat(),
                "end_time": (datetime.datetime.now() + datetime.timedelta(minutes=minutes)).isoformat(),
                "message": f"Timer set for {minutes} minutes"
            }
            
            print(f"⏰ Timer {timer_id} set for {minutes} minutes: {description}")
            return timer_info
            
        except Exception as e:
            return {"error": f"Error setting timer: {str(e)}"}
    
    def _timer_alert(self, timer_id: int, minutes: float, description: str):
        """Helper function to handle timer alerts with speech output."""
        try:
            # Wait for timer duration
            time.sleep(minutes * 60)
            
            # Check if timer was cancelled
            if timer_id in self.timers and not self.timers[timer_id]["active"]:
                return
            
            # Create timer completion message
            timer_message = f"Timer for {minutes} minutes is complete!"
            if description:
                timer_message += f" {description}"
            
            print(f"\n⏰ {timer_message}")
            
            # Try to speak the timer completion message
            try:
                from speak import speak_text
                speak_text(timer_message)
            except ImportError:
                print("Speech module not available")
            
            # Remove completed timer
            if timer_id in self.timers:
                del self.timers[timer_id]
            
            # Turn off timer LED if no active timers
            if GPIO_AVAILABLE and not self.timers:
                self.set_led("timer", False)
                
        except Exception as e:
            print(f"❌ Timer {timer_id} error: {e}")
    
    def cancel_timer(self, timer_id: int) -> dict:
        """Cancel an active timer."""
        if timer_id not in self.timers:
            return {"error": f"Timer {timer_id} not found"}
        
        timer = self.timers[timer_id]
        timer["active"] = False
        
        # Note: We can't actually stop the thread, but we mark it as inactive
        # The thread will exit gracefully when it completes
        
        del self.timers[timer_id]
        
        # Turn off timer LED if no active timers
        if GPIO_AVAILABLE and not self.timers:
            self.set_led("timer", False)
        
        return {"message": f"Timer {timer_id} cancelled"}
    
    def get_active_timers(self) -> dict:
        """Get information about all active timers."""
        active_timers = {}
        
        for timer_id, timer in self.timers.items():
            if timer["active"]:
                elapsed = time.time() - timer["start_time"]
                remaining = (timer["duration_minutes"] * 60) - elapsed
                
                active_timers[timer_id] = {
                    "duration_minutes": timer["duration_minutes"],
                    "description": timer["description"],
                    "elapsed_minutes": round(elapsed / 60, 1),
                    "remaining_minutes": round(max(0, remaining / 60), 1),
                    "start_time": datetime.datetime.fromtimestamp(timer["start_time"]).isoformat()
                }
        
        return active_timers
    
    def set_speech_speed(self, speed: str) -> dict:
        """
        Set speech synthesis speed.
        
        Args:
            speed (str): Speed preset ('slow', 'normal', 'fast', 'very_fast') or custom rate (150-600)
            
        Returns:
            dict: Result of speed change operation
        """
        try:
            # Try to import speech handler
            from speak import RaspberryPiSpeech
            
            # Create speech handler instance
            speech_handler = RaspberryPiSpeech()
            
            # Check if it's a preset
            if speed in speech_handler.speed_presets:
                success = speech_handler.set_speed(speed)
                if success:
                    return {
                        "success": True,
                        "message": f"Speech speed set to {speed}",
                        "rate": speech_handler.speed_presets[speed],
                        "current_speed": speech_handler.get_current_speed()
                    }
                else:
                    return {"error": f"Failed to set speech speed to {speed}"}
            
            # Check if it's a custom rate
            try:
                custom_rate = int(speed)
                success = speech_handler.set_custom_rate(custom_rate)
                if success:
                    return {
                        "success": True,
                        "message": f"Speech rate set to {custom_rate}",
                        "rate": custom_rate,
                        "current_speed": speech_handler.get_current_speed()
                    }
                else:
                    return {"error": f"Failed to set custom speech rate {custom_rate}"}
            except ValueError:
                return {"error": f"Invalid speed format. Use preset names or numbers 150-600"}
                
        except ImportError:
            return {"error": "Speech module not available"}
        except Exception as e:
            return {"error": f"Speech speed change failed: {str(e)}"}
    
    def get_speech_speed(self) -> dict:
        """
        Get current speech synthesis speed settings.
        
        Returns:
            dict: Current speed settings and available options
        """
        try:
            from speak import RaspberryPiSpeech
            
            speech_handler = RaspberryPiSpeech()
            
            return {
                "success": True,
                "current_speed": speech_handler.get_current_speed(),
                "current_rate": speech_handler.rate,
                "available_presets": list(speech_handler.speed_presets.keys()),
                "rate_range": "150-600"
            }
            
        except ImportError:
            return {"error": "Speech module not available"}
        except Exception as e:
            return {"error": f"Failed to get speech speed: {str(e)}"}
    
    def system_command(self, command: str) -> dict:
        """
        Execute a system command safely.
        
        Args:
            command (str): Command to execute
            
        Returns:
            dict: Command result and output
        """
        # Whitelist of safe commands
        safe_commands = [
            "uptime", "date", "whoami", "pwd", "ls", "df", "free",
            "ps", "top", "htop", "iostat", "vmstat"
        ]
        
        if command.split()[0] not in safe_commands:
            return {"error": f"Command '{command.split()[0]}' is not in safe command list"}
        
        try:
            result = subprocess.run(
                command.split(),
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return {
                "command": command,
                "return_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "success": result.returncode == 0
            }
            
        except subprocess.TimeoutExpired:
            return {"error": "Command timed out"}
        except Exception as e:
            return {"error": f"Command execution failed: {str(e)}"}

# Legacy functions for backward compatibility
def get_weather(latitude: float, longitude: float) -> dict:
    """Legacy function for backward compatibility"""
    tools = RaspberryPiTools()
    return tools.get_weather(latitude, longitude)

def get_time() -> str:
    """Legacy function for backward compatibility"""
    tools = RaspberryPiTools()
    time_info = tools.get_time()
    return time_info["time_12h"]

def set_timer(minutes: float) -> str:
    """Legacy function for backward compatibility"""
    tools = RaspberryPiTools()
    result = tools.set_timer(minutes)
    return result.get("message", str(result))

def timer_alert(minutes: float):
    """Legacy function for backward compatibility"""
    tools = RaspberryPiTools()
    tools._timer_alert(0, minutes, "")
