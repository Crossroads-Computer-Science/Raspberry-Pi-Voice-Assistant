import os
from dotenv import load_dotenv

# Load environment variables from .env BEFORE importing other modules
load_dotenv()

from audio import detect_speech
from chat import transcribe_audio, get_chatgpt_response
from speak import speak_text

SAMPLERATE = 16000

def main():
    print("🎙️ Speak now. Jarvis is listening...")

    messages = [
        {
            "role": "system",
            "content": (
                "You are Jarvis, a sarcastic and helpful assistant. "
                "You love to make jokes but still get the job done."
            )
        }
    ]

    audio = detect_speech(samplerate=SAMPLERATE)
    print("🛑 Silence detected. Transcribing...")

    user_text = transcribe_audio(audio, samplerate=SAMPLERATE)
    print(f"📝 You said: {user_text}")
    messages.append({"role": "user", "content": user_text})

    response = get_chatgpt_response(messages)
    print(f"🤖 Jarvis: {response}")

    speak_text(response)

if __name__ == "__main__":
    main()