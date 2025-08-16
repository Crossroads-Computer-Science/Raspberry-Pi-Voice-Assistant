import collections
import sys
import sounddevice as sd
import webrtcvad
import numpy as np
import scipy.io.wavfile as wav
import tempfile
from openai import OpenAI
import subprocess
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set your API keys
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# STT Parameters
samplerate = 16000
frame_duration = 30  # ms
frame_size = int(samplerate * frame_duration / 1000)
vad = webrtcvad.Vad(2)

# Trigger word (optional, can be disabled or removed)
trigger_word = "Jarvis"


model="gpt-4.1-mini"
messages=[
    {"role": "system", "content": "You are a helpful, but sarcastic and comedic assistant. You go by the name Jarvis and tell sarcastic jokes whenever possible."}
]
tools = [
    {
        "type": "function", 
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude":  {"type": "number"},
                    "longitude":  {"type": "number"}
                    },                
                    
                "required": ["location"], 
                "additionalProperties": False
            }, 
    }
    }
]



def audio_stream():
    with sd.InputStream(samplerate=samplerate, channels=1, dtype='int16') as stream:
        while True:
            audio = stream.read(frame_size)[0].flatten()
            yield audio

def detect_speech():
    ring_buffer = collections.deque(maxlen=int(700 / frame_duration))
    triggered = False
    voiced_frames = []

    for frame in audio_stream():
        is_speech = vad.is_speech(frame.tobytes(), samplerate)
        if not triggered:
            ring_buffer.append(frame)
            num_voiced = len([f for f in ring_buffer if vad.is_speech(f.tobytes(), samplerate)])
            if num_voiced > 0.9 * ring_buffer.maxlen:
                triggered = True
                voiced_frames.extend(ring_buffer)
                ring_buffer.clear()
        else:
            voiced_frames.append(frame)
            ring_buffer.append(frame)
            num_unvoiced = len([f for f in ring_buffer if not vad.is_speech(f.tobytes(), samplerate)])
            if num_unvoiced > 0.9 * ring_buffer.maxlen:
                break

    return np.concatenate(voiced_frames)

def transcribe_audio(audio):
    with tempfile.NamedTemporaryFile(suffix=".wav") as temp_wav:
        wav.write(temp_wav.name, samplerate, audio)
        temp_wav.seek(0)
        with open(temp_wav.name, "rb") as f:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                response_format="json"
                )
            return transcript.text

def get_chatgpt_response():
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools
        #function_call="auto" # Let the model decide whether to call a function
    )
    messages.append(response.choices[0].message)

    return response

import requests

def get_weather(latitude, longitude):
    response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m")
    data = response.json()

    return data['current']['temperature_2m']

def call_function(name, args):
    if name == "get_weather":
        return get_weather(**args)
    #if name == "something_else":
    #    pass


def speak_text(text, voice="Alex", rate=200):
    try:
        subprocess.run([
            "say",
            "-v", voice,
            "-r", str(rate),
            text
        ], check=True)
        print("🔊 Speaking complete.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Speech synthesis failed: {e}")
    except FileNotFoundError:
        print(f"❌ Text-to-speech not available. Would say: {text}")




# Main Loop
last_spoken_text = ""

while True:
    try:
        print("🎙 Listening for speech...")
        audio = detect_speech()
        print("🛑 Detected silence, transcribing...")
        text = transcribe_audio(audio)
        print(f"📝 You said: {text}")

        if trigger_word.lower() in text.lower():
            # -------------------------------
            messages.append({"role": "user", "content": text})

            response = get_chatgpt_response()
            message = response.choices[0].message
            
            if response.choices[0].message.tool_calls != None:
                print("Tool Calls :") 
                print(response.choices[0].message.tool_calls)
                for myfunction in response.choices[0].message.tool_calls:
                    name = myfunction.function.name 
                    args = json.loads(myfunction.function.arguments)
                    weather = get_weather(args["latitude"], args["longitude"])
                    
                    print("WEATHER DATA: ")
                    print(weather)
                    
                    messages.append({
                        "role":"tool", 
                        "tool_call_id": myfunction.id,
                        "content": str(weather)
                        })
                        
                    print(messages)
                    
                    response2 = client.chat.completions.create(
                        model=model,
                        messages=messages,
                        tools=tools
                    )
                    print("weather response")
                    print(response2)
                    message = response2.choices[0].message 
                    break

           
            print(f"🤖 Jarvis: {message.content}")
            
            if message.content != None:
                audable_message = message.content.strip()
            if audable_message != last_spoken_text:
                speak_text(audable_message)
                last_spoken_text = audable_message
        else:
            print("❌ Trigger word not found. Skipping response.")
        
        print("-" * 60)
        time.sleep(1)

    except KeyboardInterrupt:
        print("👋 Assistant terminated by user.")
        break

