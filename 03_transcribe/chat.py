import os
import tempfile
import numpy as np
import scipy.io.wavfile as wav
from openai import OpenAI

# Initialize OpenAI client with API key from environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def transcribe_audio(audio: np.ndarray, samplerate: int) -> str:
    """
    Save audio to a temporary WAV file and send to OpenAI Whisper API for transcription.
    """
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