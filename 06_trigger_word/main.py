# main.py

from dotenv import load_dotenv
from trigger import wait_for_trigger
from audio import detect_speech
from transcribe import transcribe_audio
from speak import speak
import openai


# Load your OpenAI API key from .env file
load_dotenv()

# Optional: maintain conversation context
messages = [
    {
        "role": "system",
        "content": (
            "You are Jarvis, a sarcastic and helpful assistant. "
            "You love to make jokes but still get the job done."
        )
    }
]

def chat_with_openai(prompt):
    messages.append({"role": "user", "content": prompt})

    response = openai.ChatCompletion.create(
        model="gpt-4",  # or "gpt-3.5-turbo"
        messages=messages,
    )

    reply = response['choices'][0]['message']['content']
    messages.append({"role": "assistant", "content": reply})
    return reply

def main():
    print("Voice Assistant Ready. Say your trigger word...")

    while True:
        wait_for_trigger()  # Blocks until wake word is detected
        print("🎤 Trigger word detected. Listening...")

        audio_data = detect_speech()
        print("🔊 Audio captured. Transcribing...")

        try:
            transcript = transcribe_audio(audio_data)
            print("📝 You said:", transcript)

            response = chat_with_openai(transcript)
            print("🤖 Assistant:", response)

            speak(response)

        except Exception as e:
            print("⚠️ Error:", e)
            speak("Sorry, I didn't catch that.")

if __name__ == "__main__":
    main()