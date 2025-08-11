import os
import tempfile
import scipy.io.wavfile as wav
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def transcribe_audio(audio, samplerate=16000):
    """
    Transcribe audio data to text using OpenAI's Whisper model.
    
    Args:
        audio (numpy.ndarray): Audio data to transcribe
        samplerate (int): Sample rate of the audio
        
    Returns:
        str: Transcribed text
    """
    # Save audio to temporary WAV file
    with tempfile.NamedTemporaryFile(suffix=".wav") as temp_wav:
        wav.write(temp_wav.name, samplerate, audio)
        temp_wav.seek(0)
        
        # Transcribe using OpenAI's Whisper model
        with open(temp_wav.name, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )
            
        return transcript

def get_chatgpt_response(messages, tools=None):
    """
    Get a response from ChatGPT based on the conversation history.
    
    Args:
        messages (list): List of conversation messages
        tools (list, optional): List of available tools/functions
        
    Returns:
        openai.types.chat.ChatCompletion: ChatGPT's response including potential function calls
    """
    # Prepare the API call parameters
    params = {
        "model": "gpt-3.5-turbo",  # You can adjust the model as needed
        "messages": messages
    }
    
    # Add tools if provided
    if tools:
        params["tools"] = tools
        params["tool_choice"] = "auto"  # Let the model decide when to use tools
    
    # Get completion from ChatGPT
    response = client.chat.completions.create(**params)
    
    return response.choices[0]
