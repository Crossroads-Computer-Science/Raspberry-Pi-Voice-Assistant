import os
import json
from dotenv import load_dotenv

# Load environment variables from .env BEFORE importing other modules
load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    print(" OpenAI API key not found!")
    print("   Create a .env file in this folder containing:")
    print("   OPENAI_API_KEY=your-key-here")
    print("   Get a key at: https://platform.openai.com/api-keys")
    exit(1)

from audio import detect_speech
from chat import transcribe_audio, get_chatgpt_response
from speak import speak_text
from tools import get_weather, get_time, set_timer

# Configuration
SAMPLERATE = 16000
TRIGGER_WORD = "jarvis"

def main():
    print(" Listening for trigger word 'Jarvis'...")
    
    # Initialize conversation history with system message
    messages = [
        {
            "role": "system",
            "content": (
                "You are Jarvis, a sarcastic and helpful assistant. "
                "You love to make jokes but still get the job done. "
                "You have access to several tools you can use to help the user."
            )
        }
    ]
    
    # Define available tools/functions
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get the current weather for a location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "latitude": {
                            "type": "number",
                            "description": "The latitude coordinate"
                        },
                        "longitude": {
                            "type": "number",
                            "description": "The longitude coordinate"
                        }
                    },
                    "required": ["latitude", "longitude"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_time",
                "description": "Get the current time",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "set_timer",
                "description": "Set a timer for a specified number of minutes",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "minutes": {
                            "type": "number",
                            "description": "Number of minutes to set the timer for"
                        }
                    },
                    "required": ["minutes"]
                }
            }
        }
    ]
    
    # Keep listening for the trigger word
    while True:
        try:
            # Record and process audio
            audio = detect_speech(samplerate=SAMPLERATE)
            print(" Silence detected. Transcribing...")
            
            # Convert speech to text
            user_text = transcribe_audio(audio, samplerate=SAMPLERATE)
            print(f" You said: {user_text}")
            
            # Check if trigger word was spoken
            if TRIGGER_WORD in user_text.lower():
                print(" Trigger word detected! Processing request...")
                
                # Add user's message to conversation
                messages.append({"role": "user", "content": user_text})
                
                # Get AI response with potential function calls
                response = get_chatgpt_response(messages, tools)
                
                # Handle function calls if present
                if response.tool_calls:
                    print(" Executing function calls...")
                    
                    for tool_call in response.tool_calls:
                        function_name = tool_call.function.name
                        function_args = json.loads(tool_call.function.arguments)
                        
                        # Execute the appropriate function
                        if function_name == "get_weather":
                            result = get_weather(**function_args)
                        elif function_name == "get_time":
                            result = get_time()
                        elif function_name == "set_timer":
                            result = set_timer(**function_args)
                        else:
                            result = "Function not implemented"
                        
                        # Add the function result to messages
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": str(result)
                        })
                    
                    # Get a new response incorporating the function results
                    response = get_chatgpt_response(messages, tools)
                
                # Extract and speak the final response
                assistant_message = response.message.content
                print(f" Jarvis: {assistant_message}")
                speak_text(assistant_message)
                
                # Add assistant's response to conversation history
                messages.append({"role": "assistant", "content": assistant_message})
            else:
                print(" Trigger word not found. Waiting for 'Jarvis'...")
                
        except KeyboardInterrupt:
            print("\n Goodbye!")
            break
        except Exception as e:
            print(f" Error: {str(e)}")
            continue

if __name__ == "__main__":
    main()
