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
from speak import speak_text

# Configuration
SAMPLERATE = 16000
TRIGGER_WORD = "jarvis"  # The wake word that activates the assistant

def main():
    print("🎙️ Listening for trigger word 'Jarvis'...")
    
    # Initialize conversation history
    messages = [
        {
            "role": "system",
            "content": (
                "You are Jarvis, a sarcastic and helpful assistant. "
                "You love to make jokes but still get the job done."
            )
        }
    ]
    
    # Keep listening for the trigger word
    while True:
        try:
            # Record and process audio
            audio = detect_speech(samplerate=SAMPLERATE)
            print("🛑 Silence detected. Transcribing...")
            
            # Convert speech to text
            user_text = transcribe_audio(audio, samplerate=SAMPLERATE)
            print(f"📝 You said: {user_text}")
            
            # Check if trigger word was spoken
            if TRIGGER_WORD in user_text.lower():
                print("✨ Trigger word detected! Processing request...")
                
                # Add user's message to conversation
                messages.append({"role": "user", "content": user_text})
                
                # Get AI response and add it to conversation history
                response = get_chatgpt_response(messages)
                messages.append({"role": "assistant", "content": response})
                print(f"🤖 Jarvis: {response}")

                # Speak the response
                speak_text(response)
            else:
                print("❌ Trigger word not found. Waiting for 'Jarvis'...")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            continue

if __name__ == "__main__":
    main()
