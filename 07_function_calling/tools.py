import requests
import datetime
import time
import threading

def get_weather(latitude: float, longitude: float) -> dict:
    """
    Get current weather data for the specified coordinates using the Open-Meteo API.
    
    Args:
        latitude (float): Latitude coordinate
        longitude (float): Longitude coordinate
        
    Returns:
        dict: Weather data including temperature and conditions
    """
    try:
        # Make API request to Open-Meteo (free, no API key required)
        url = f"https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": ["temperature_2m", "wind_speed_10m", "weather_code"]
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Extract current weather data
        current = data["current"]
        
        return {
            "temperature": current["temperature_2m"],
            "wind_speed": current["wind_speed_10m"],
            "weather_code": current["weather_code"]
        }
        
    except Exception as e:
        return f"Error getting weather data: {str(e)}"

def get_time() -> str:
    """
    Get the current time in a human-readable format.
    
    Returns:
        str: Current time
    """
    current_time = datetime.datetime.now()
    return current_time.strftime("%I:%M %p")

def timer_alert(minutes: float):
    """
    Helper function to handle timer alerts.
    
    Args:
        minutes (float): Number of minutes to wait
    """
    time.sleep(minutes * 60)
    timer_message = f"Timer for {minutes} minutes is done!"
    print(f"\n⏰ {timer_message}")
    
    # Speak the timer completion message
    try:
        from speak import speak_text
        speak_text(timer_message)
    except ImportError:
        print("Speech module not available")

def set_timer(minutes: float) -> str:
    """
    Set a timer for the specified number of minutes.
    
    Args:
        minutes (float): Number of minutes for the timer
        
    Returns:
        str: Confirmation message
    """
    try:
        # Start timer in background thread
        timer_thread = threading.Thread(target=timer_alert, args=(minutes,))
        timer_thread.daemon = True  # Allow program to exit even if timer is running
        timer_thread.start()
        
        return f"Timer set for {minutes} minutes"
    except Exception as e:
        return f"Error setting timer: {str(e)}"
