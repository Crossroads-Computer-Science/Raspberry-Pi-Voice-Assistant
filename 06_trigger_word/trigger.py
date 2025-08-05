from audio import detect_speech
from transcribe import transcribe_audio

def wait_for_trigger(trigger_word="computer"):
    while True:
        print("Listening for trigger...")
        audio_data = detect_speech()
        text = transcribe_audio(audio_data)
        print(f"Heard: {text}")
        if trigger_word.lower() in text.lower():
            break