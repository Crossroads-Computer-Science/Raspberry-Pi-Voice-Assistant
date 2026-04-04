import os
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

SAMPLERATE = 16000

def main():
    print(" Speak now. Jarvis is listening...")

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
    print(" Silence detected. Transcribing...")

    user_text = transcribe_audio(audio, samplerate=SAMPLERATE)
    print(f" You said: {user_text}")
    messages.append({"role": "user", "content": user_text})

    response = get_chatgpt_response(messages)
    messages.append({"role": "assistant", "content": response})
    print(f" Jarvis: {response}")

    speak_text(response)

if __name__ == "__main__":
    main()