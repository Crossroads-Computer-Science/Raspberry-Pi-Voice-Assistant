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
        self.trigger_word = "rhodey"
        self.running = False
        
        # Performance monitoring
        self.start_time = time.time()
        self.interaction_count = 0
        
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
        print(f"🎙️ Roadie is listening for trigger word '{self.trigger_word}'...")
        print("💡 Say 'Roadie' followed by your request")
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
                
                # Check for trigger word
                if self.trigger_word.lower() in user_text.lower():
                    print("✨ Trigger word detected! Processing request...")
                    self._process_request(user_text)
                    self.interaction_count += 1
                else:
                    print("❌ Trigger word not found. Waiting for 'Roadie'...")
                
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
            if response.tool_calls:
                print("🛠️ Executing function calls...")
                results = self.chat_handler.process_function_calls(response, self.tools_handler)
                
                # Get a new response incorporating the function results
                response = self.chat_handler.get_chatgpt_response([], tools)
            
            # Extract and speak the final response
            if response and response.choices:
                assistant_message = response.choices[0].message.content
                print(f"🤖 Roadie: {assistant_message}")
                
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
