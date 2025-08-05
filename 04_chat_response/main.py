import os
from dotenv import load_dotenv
from audio import detect_speech
from chat import transcribe_audio, get_chatgpt_response

# Load environment variables from .env
load_dotenv()

SAMPLERATE = 16000

def main():
    print("🎙️ Speak now. The assistant will detect your speech, transcribe it, and respond.")

    # Initialize conversation with system message
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful, sarcastic, and comedic assistant named Jarvis. "
                "Try to add sarcastic jokes whenever possible."
            )
        }
    ]

    audio = detect_speech(samplerate=SAMPLERATE)
    print("🛑 Detected silence, sending audio to OpenAI Whisper for transcription...")

    user_text = transcribe_audio(audio, samplerate=SAMPLERATE)
    print(f"📝 You said: {user_text}")

    # Append user message
    messages.append({"role": "user", "content": user_text})

    # Get ChatGPT response
    response = get_chatgpt_response(messages)
    print(f"🤖 Jarvis: {response}")

if __name__ == "__main__":
    main()