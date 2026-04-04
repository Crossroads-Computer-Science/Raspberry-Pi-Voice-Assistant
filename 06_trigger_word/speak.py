import platform
import subprocess


def speak_text(text, voice="Alex", rate=200):
    """
    Convert text to speech using the best available engine for your OS.

    - macOS:   Uses the built-in 'say' command
    - Windows: Uses pyttsx3 (install with: pip install pyttsx3)
    - Linux:   Uses espeak (install with: sudo apt install espeak)
    """
    system = platform.system()

    if system == "Darwin":  # macOS
        try:
            subprocess.run(["say", "-v", voice, "-r", str(rate), text], check=True)
            print(" Speaking complete.")
        except subprocess.CalledProcessError as e:
            print(f" Speech synthesis failed: {e}")

    elif system == "Windows":
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty("rate", rate)
            engine.say(text)
            engine.runAndWait()
            print(" Speaking complete.")
        except ImportError:
            print(" pyttsx3 not found. Install it with: pip install pyttsx3")
            print(f"   (Jarvis would have said: {text})")
        except Exception as e:
            print(f" Speech synthesis failed: {e}")

    elif system == "Linux":
        try:
            subprocess.run(["espeak", text], check=True)
            print(" Speaking complete.")
        except FileNotFoundError:
            print(" espeak not found. Install it with: sudo apt install espeak")
            print(f"   (Jarvis would have said: {text})")
        except subprocess.CalledProcessError as e:
            print(f" Speech synthesis failed: {e}")

    else:
        print(f" Text-to-speech not supported on {system}.")
        print(f"   (Jarvis would have said: {text})")
