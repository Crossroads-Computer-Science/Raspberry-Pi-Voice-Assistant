import os
import tempfile
import numpy as np
import scipy.io.wavfile as wav
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def transcribe_audio(audio: np.ndarray, samplerate: int) -> str:
    with tempfile.NamedTemporaryFile(suffix=".wav") as temp_wav:
        wav.write(temp_wav.name, samplerate, audio)
        temp_wav.seek(0)
        with open(temp_wav.name, "rb") as audio_file:
            response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="json"
            )
            return response.text

def get_chatgpt_response(messages: list) -> str:
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages
    )
    message = response.choices[0].message.content
    messages.append({"role": "assistant", "content": message})
    return message