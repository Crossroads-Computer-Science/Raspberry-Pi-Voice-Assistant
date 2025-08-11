import subprocess

def speak_text(text, voice="Alex", rate=200):
    """
    Convert text to speech using macOS's say command.
    
    Args:
        text (str): Text to convert to speech
        voice (str): Name of the voice to use
        rate (int): Speech rate (words per minute)
    """
    try:
        # Use macOS 'say' command for text-to-speech
        subprocess.run([
            "say",
            "-v", voice,
            "-r", str(rate),
            text
        ], check=True)
        print("🔊 Speaking complete.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Speech synthesis failed: {e}")
    except FileNotFoundError:
        print(f"❌ Text-to-speech not available. Would say: {text}")
