import os
from dotenv import load_dotenv

# Load environment variables from .env BEFORE importing other modules
load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    print("❌ OpenAI API key not found!")
    print("   Create a .env file in this folder containing:")
    print("   OPENAI_API_KEY=your-key-here")
    print("   Get a key at: https://platform.openai.com/api-keys")
    exit(1)

from audio import detect_speech
from chat import transcribe_audio, get_chatgpt_response

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

    # Get ChatGPT response and add it to the conversation history
    response = get_chatgpt_response(messages)
    messages.append({"role": "assistant", "content": response})
    print(f"🤖 Jarvis: {response}")

if __name__ == "__main__":
    main()