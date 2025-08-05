# transcribe.py
import openai
import soundfile as sf
import tempfile

def transcribe_audio(audio_data, samplerate=16000):
    # Write to a temporary WAV file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        sf.write(f.name, audio_data, samplerate)
        f.flush()

        # Use OpenAI Whisper to transcribe the file
        with open(f.name, "rb") as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)

        return transcript['text']