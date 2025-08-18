import os
import pathlib
from dotenv import load_dotenv

# Load environment variables from .env file in the same directory as this script
script_dir = pathlib.Path(__file__).parent
load_dotenv(script_dir / ".env")

import time
import signal
import sys
from audio import RaspberryPiAudio
from speak import RaspberryPiSpeech
from chat import RaspberryPiChat
from tools import RaspberryPiTools

class RaspberryPiVoiceAssistant:
    def __init__(self):
        """Initialize the Raspberry Pi Voice Assistant."""
        print("🤖 Initializing Roadie - Raspberry Pi Voice Assistant...")
        
        # Initialize components
        self.audio_handler = RaspberryPiAudio()
        self.speech_handler = RaspberryPiSpeech()
        self.chat_handler = RaspberryPiChat()
        self.tools_handler = RaspberryPiTools()
        
        # Configuration
        self.samplerate = 16000
        # Optimized trigger words for Raspberry Pi 4
        # Primary triggers (most common, checked first)
        self.primary_triggers = ["rhodey", "roadie", "computer", "assistant"]
        
        # Extended triggers (less common, checked only if needed)
        self.extended_triggers = ["hey rhodey", "hey roadie", "hey computer", "hey assistant"]
        
        # Single-word variations for speech recognition
        self.variations = {
            "rhodey": ["rody", "roady", "rowdy", "rhody"],
            "roadie": ["rody", "roady", "rowdy", "rhody"],
            "computer": ["computa", "compooter", "compuda"],
            "assistant": ["assist", "assist", "assist"]
        }
        self.running = False
        
        # Performance monitoring
        self.start_time = time.time()
        self.interaction_count = 0
        self.trigger_detection_times = []  # Track trigger detection performance
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        print("✅ Roadie initialization complete!")
        self._print_system_info()
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        print(f"\n🛑 Received signal {signum}, shutting down gracefully...")
        self.running = False
        self.cleanup()
        sys.exit(0)
    
    def _print_system_info(self):
        """Print system information and status."""
        try:
            system_status = self.tools_handler.get_system_status()
            if "error" not in system_status:
                print(f"📊 System Status:")
                print(f"   CPU: {system_status['cpu_percent']}%")
                print(f"   Memory: {system_status['memory_percent']}%")
                print(f"   Temperature: {system_status['temperature_celsius']}°C")
                print(f"   Uptime: {system_status['uptime_hours']} hours")
            else:
                print(f"⚠️ Could not get system status: {system_status['error']}")
        except Exception as e:
            print(f"⚠️ Error getting system info: {e}")
    
    def run(self):
        """Main application loop."""
        print("🎙️ Rhodey is listening...")
        print("💡 Primary trigger words (fastest):")
        for i, trigger in enumerate(self.primary_triggers, 1):
            print(f"   {i}. '{trigger}'")
        print("💡 Extended triggers:")
        for i, trigger in enumerate(self.extended_triggers, 1):
            print(f"   {i+len(self.primary_triggers)}. '{trigger}'")
        print("🔧 Available commands: weather, time, timer, system status, etc.")
        print("⏹️ Press Ctrl+C to exit")
        
        self.running = True
        
        while self.running:
            try:
                # Listen for audio input
                audio = self.audio_handler.detect_speech()
                
                if len(audio) == 0:
                    continue
                
                # Transcribe audio to text
                print("🔄 Transcribing speech...")
                user_text = self.chat_handler.transcribe_audio(audio, self.samplerate)
                
                if not user_text:
                    print("❌ Could not transcribe audio")
                    continue
                
                print(f"📝 You said: {user_text}")
                
                # Optimized trigger word detection for Raspberry Pi 4
                trigger_start_time = time.time()
                user_text_lower = user_text.lower()
                detected_trigger = None
                
                # Fast path: Check primary triggers first (most common)
                for trigger in self.primary_triggers:
                    if trigger in user_text_lower:
                        detected_trigger = trigger
                        break
                
                # Medium path: Check extended triggers only if primary failed
                if not detected_trigger:
                    for trigger in self.extended_triggers:
                        if trigger in user_text_lower:
                            detected_trigger = trigger
                            break
                
                # Slow path: Check variations only if both above failed
                if not detected_trigger:
                    for base_trigger, var_list in self.variations.items():
                        for var in var_list:
                            if var in user_text_lower:
                                detected_trigger = base_trigger
                                break
                        if detected_trigger:
                            break
                
                trigger_time = time.time() - trigger_start_time
                self.trigger_detection_times.append(trigger_time)
                
                if detected_trigger:
                    print(f"✨ Trigger word '{detected_trigger}' detected! Processing request...")
                    
                    # Remove the trigger word from the user text for cleaner processing
                    # Handle multi-word triggers properly
                    if detected_trigger in ["hey rhodey", "hey roadie", "hey computer", "hey assistant", "okay rhodey", "okay roadie"]:
                        # For multi-word triggers, remove the entire phrase
                        cleaned_text = user_text.replace(detected_trigger, "").strip()
                    else:
                        # For single-word triggers, be more careful about removal
                        words = user_text.split()
                        trigger_words = detected_trigger.split()
                        # Remove only the trigger word(s) from the beginning
                        if words[:len(trigger_words)] == trigger_words:
                            cleaned_text = " ".join(words[len(trigger_words):]).strip()
                        else:
                            cleaned_text = user_text.replace(detected_trigger, "").strip()
                    
                    if cleaned_text:
                        self._process_request(cleaned_text)
                    else:
                        # If only trigger word was said, ask what they want
                        self._process_request("What can I help you with?")
                    self.interaction_count += 1
                else:
                    print("❌ Trigger word not found. Waiting for trigger words...")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error in main loop: {e}")
                continue
    
    def _process_request(self, user_text):
        """Process user request with function calling."""
        try:
            # Add user message to conversation
            self.chat_handler.add_user_message(user_text)
            
            # Get available functions
            tools = self.chat_handler.get_available_functions()
            
            # Get AI response with potential function calls
            response = self.chat_handler.get_chatgpt_response([{"role": "user", "content": user_text}], tools)
            
            if not response:
                print("❌ Failed to get response from ChatGPT")
                return
            
            # Handle function calls if present
            try:
                # Debug: Check what attributes the response has
                print(f"🔍 Response type: {type(response)}")
                print(f"🔍 Response attributes: {dir(response)}")
                if hasattr(response, 'choices') and response.choices:
                    print(f"🔍 First choice attributes: {dir(response.choices[0])}")
                    if hasattr(response.choices[0], 'message'):
                        print(f"🔍 Message attributes: {dir(response.choices[0].message)}")
                
                # Check for tool_calls in different possible locations
                tool_calls = None
                if hasattr(response, 'tool_calls'):
                    tool_calls = response.tool_calls
                elif hasattr(response, 'choices') and response.choices and hasattr(response.choices[0], 'message'):
                    if hasattr(response.choices[0].message, 'tool_calls'):
                        tool_calls = response.choices[0].message.tool_calls
                
                if tool_calls:
                    print("🛠️ Executing function calls...")
                    results = self.chat_handler.process_function_calls(response, self.tools_handler)
                    
                    # Get a new response incorporating the function results
                    # The function results are already added to conversation history by process_function_calls
                    response = self.chat_handler.get_chatgpt_response([], tools)
                else:
                    print("🔍 No tool calls detected in response")
                    
            except Exception as e:
                print(f"⚠️ Error checking for tool calls: {e}")
                print(f"🔍 Response structure: {response}")
            
            # Extract and speak the final response
            if response and response.choices:
                assistant_message = response.choices[0].message.content
                print(f"🤖 Rhodey: {assistant_message}")
                
                # Speak the response
                self.speech_handler.speak_text(assistant_message)
                
                # Add assistant's response to conversation history
                self.chat_handler.conversation_history.append({
                    "role": "assistant",
                    "content": assistant_message
                })
            else:
                print("❌ No response content received")
                
        except Exception as e:
            print(f"❌ Error processing request: {e}")
            self.speech_handler.speak_text("I encountered an error processing your request. Please try again.")
    
    def cleanup(self):
        """Clean up resources before shutdown."""
        print("🧹 Cleaning up resources...")
        
        try:
            # Turn off all LEDs
            if hasattr(self.audio_handler, 'set_led'):
                self.audio_handler.set_led("listening", False)
                self.audio_handler.set_led("processing", False)
                self.audio_handler.set_led("speaking", False)
            
            if hasattr(self.speech_handler, 'set_led'):
                self.speech_handler.set_led(False)
            
            if hasattr(self.tools_handler, 'set_led'):
                self.tools_handler.set_led("status", False)
                self.tools_handler.set_led("timer", False)
                self.tools_handler.set_led("weather", False)
            
            # Print final statistics
            runtime = time.time() - self.start_time
            print(f"📊 Final Statistics:")
            print(f"   Runtime: {runtime/3600:.1f} hours")
            print(f"   Interactions: {self.interaction_count}")
            print(f"   Average response time: {self.chat_handler.last_response_time:.2f}s" if self.chat_handler.last_response_time else "N/A")
            
            # Performance metrics
            if self.trigger_detection_times:
                avg_trigger_time = sum(self.trigger_detection_times) / len(self.trigger_detection_times)
                max_trigger_time = max(self.trigger_detection_times)
                min_trigger_time = min(self.trigger_detection_times)
                print(f"   Trigger detection performance:")
                print(f"     Average: {avg_trigger_time*1000:.2f}ms")
                print(f"     Fastest: {min_trigger_time*1000:.2f}ms")
                print(f"     Slowest: {max_trigger_time*1000:.2f}ms")
                print(f"     Total checks: {len(self.trigger_detection_times)}")
            
        except Exception as e:
            print(f"⚠️ Error during cleanup: {e}")
        
        print("✅ Cleanup complete")

def main():
    """Main entry point."""
    try:
        # Check if API key is available
        if not os.getenv("OPENAI_API_KEY"):
            print("❌ OPENAI_API_KEY not found in environment variables")
            print("💡 Please create a .env file with your OpenAI API key")
            return
        
        # Create and run the assistant
        assistant = RaspberryPiVoiceAssistant()
        assistant.run()
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
