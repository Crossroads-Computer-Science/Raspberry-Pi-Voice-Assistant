import os
import tempfile
import numpy as np
import scipy.io.wavfile as wav
from openai import OpenAI
import json
import time

# Initialize OpenAI client with API key from environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class RaspberryPiChat:
    def __init__(self):
        self.conversation_history = []
        self.function_calls = []
        self.last_response_time = None
        
        # System message optimized for Raspberry Pi assistant
        self.system_message = {
            "role": "system",
            "content": (
                "You are Roadie, a helpful and witty voice assistant running on a Raspberry Pi. "
                "You are the mascot for Crossroads School for Arts and Sciences in Santa Monica, CA, which is a roadrunner. "
                "You are a friendly and helpful assistant who can help with a variety of tasks. "
                "You love to tell dad jokes. "
                "You have access to various tools and can help with:\n"
                "- Getting weather information\n"
                "- Setting timers and reminders\n"
                "- Providing time and date information\n"
                "- System monitoring and status\n"
                "- General conversation and assistance\n\n"
                "Keep responses concise but friendly. Use your tools when appropriate. "
                "If asked about system status, use the get_system_status function. "
                "For weather, use coordinates (you can ask the user for their location)."
            )
        }
        
        # Initialize conversation with system message
        self.conversation_history.append(self.system_message)
    
    def transcribe_audio(self, audio: np.ndarray, samplerate: int) -> str:
        """
        Save audio to a temporary WAV file and send to OpenAI Whisper API for transcription.
        
        Args:
            audio (np.ndarray): Audio data
            samplerate (int): Sample rate of the audio
            
        Returns:
            str: Transcribed text
        """
        try:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
                wav.write(temp_wav.name, samplerate, audio)
                temp_wav.seek(0)
                
                with open(temp_wav.name, "rb") as audio_file:
                    response = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file,
                        response_format="json"
                    )
                    
                    # Clean up temporary file
                    os.unlink(temp_wav.name)
                    
                    return response.text.strip()
                    
        except Exception as e:
            print(f"❌ Transcription error: {e}")
            return ""
    
    def get_chatgpt_response(self, messages, tools=None, use_function_calling=True):
        """
        Get response from ChatGPT with optional function calling.
        
        Args:
            messages (list): Conversation messages
            tools (list): Available tools/functions
            use_function_calling (bool): Whether to enable function calling
            
        Returns:
            OpenAI response object
        """
        try:
            # Add conversation history
            all_messages = self.conversation_history + messages
            
            # Prepare API call parameters
            api_params = {
                "model": "gpt-4o-mini",  # Use mini for faster responses on Pi
                "messages": all_messages,
                "max_tokens": 150,  # Limit response length for voice
                "temperature": 0.7
            }
            
            # Add tools if function calling is enabled
            if use_function_calling and tools:
                api_params["tools"] = tools
                api_params["tool_choice"] = "auto"
                print(f"🔧 Function calling enabled with {len(tools)} tools")
            else:
                print(f"🔧 Function calling disabled or no tools provided")
            
            # Make API call
            start_time = time.time()
            response = client.chat.completions.create(**api_params)
            self.last_response_time = time.time() - start_time
            
            # Add response to conversation history
            self.conversation_history.append(response.choices[0].message)
            
            return response
            
        except Exception as e:
            print(f"❌ ChatGPT API error: {e}")
            return None
    
    def process_function_calls(self, response, tools_instance):
        """
        Process function calls from ChatGPT response.
        
        Args:
            response: ChatGPT response object
            tools_instance: Instance of RaspberryPiTools
            
        Returns:
            list: Results of function calls
        """
        if not response.tool_calls:
            return []
        
        results = []
        print("🛠️ Executing function calls...")
        
        for tool_call in response.tool_calls:
            try:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                print(f"🔧 Calling {function_name} with args: {function_args}")
                
                # Execute the appropriate function
                if function_name == "get_weather":
                    result = tools_instance.get_weather(**function_args)
                elif function_name == "get_time":
                    result = tools_instance.get_time()
                elif function_name == "set_timer":
                    result = tools_instance.set_timer(**function_args)
                elif function_name == "get_system_status":
                    result = tools_instance.get_system_status()
                elif function_name == "cancel_timer":
                    result = tools_instance.cancel_timer(**function_args)
                elif function_name == "get_active_timers":
                    result = tools_instance.get_active_timers()
                elif function_name == "system_command":
                    result = tools_instance.system_command(**function_args)
                else:
                    result = {"error": f"Function {function_name} not implemented"}
                
                results.append({
                    "function_name": function_name,
                    "result": result,
                    "tool_call_id": tool_call.id
                })
                
                # Add function result to conversation history
                self.conversation_history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })
                
            except Exception as e:
                error_result = {"error": f"Function execution failed: {str(e)}"}
                results.append({
                    "function_name": function_name,
                    "result": error_result,
                    "tool_call_id": tool_call.id
                })
                
                # Add error to conversation history
                self.conversation_history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(error_result)
                })
        
        return results
    
    def get_conversation_summary(self) -> dict:
        """Get a summary of the current conversation."""
        return {
            "total_messages": len(self.conversation_history),
            "user_messages": len([m for m in self.conversation_history if m["role"] == "user"]),
            "assistant_messages": len([m for m in self.conversation_history if m["role"] == "assistant"]),
            "function_calls": len([m for m in self.conversation_history if m["role"] == "tool"]),
            "last_response_time": self.last_response_time,
            "conversation_start": self.conversation_history[0]["timestamp"] if self.conversation_history else None
        }
    
    def clear_conversation(self):
        """Clear conversation history (keep system message)."""
        self.conversation_history = [self.system_message]
        self.function_calls = []
        self.last_response_time = None
        print("🧹 Conversation history cleared")
    
    def add_user_message(self, content: str):
        """Add a user message to the conversation."""
        user_message = {
            "role": "user",
            "content": content,
            "timestamp": time.time()
        }
        self.conversation_history.append(user_message)
    
    def get_available_functions(self) -> list:
        """Get list of available functions for the assistant."""
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "Get current weather for a location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "latitude": {"type": "number", "description": "Latitude coordinate"},
                            "longitude": {"type": "number", "description": "Longitude coordinate"}
                        },
                        "required": ["latitude", "longitude"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_time",
                    "description": "Get current time and date information",
                    "parameters": {"type": "object", "properties": {}, "required": []}
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
                            "minutes": {"type": "number", "description": "Number of minutes"},
                            "description": {"type": "string", "description": "Optional timer description"}
                        },
                        "required": ["minutes"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_system_status",
                    "description": "Get Raspberry Pi system status and health information",
                    "parameters": {"type": "object", "properties": {}, "required": []}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "cancel_timer",
                    "description": "Cancel an active timer",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "timer_id": {"type": "integer", "description": "Timer ID to cancel"}
                        },
                        "required": ["timer_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_active_timers",
                    "description": "Get information about all active timers",
                    "parameters": {"type": "object", "properties": {}, "required": []}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "system_command",
                    "description": "Execute a safe system command",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "command": {"type": "string", "description": "System command to execute"}
                        },
                        "required": ["command"]
                    }
                }
            }
        ]

# Legacy functions for backward compatibility
def transcribe_audio(audio: np.ndarray, samplerate: int) -> str:
    """Legacy function for backward compatibility"""
    chat_handler = RaspberryPiChat()
    return chat_handler.transcribe_audio(audio, samplerate)

def get_chatgpt_response(messages, tools=None):
    """Legacy function for backward compatibility"""
    chat_handler = RaspberryPiChat()
    return chat_handler.get_chatgpt_response(messages, tools)
