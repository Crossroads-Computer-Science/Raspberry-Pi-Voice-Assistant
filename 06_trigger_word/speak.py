# speak.py

import platform
import os
import subprocess

def speak(text):
    system = platform.system()
    
    if system == 'Darwin':  # macOS
        os.system(f'say "{text}"')
    elif system == 'Linux':
        try:
            subprocess.run(["espeak", text], check=True)
        except FileNotFoundError:
            print("⚠️ espeak not found. Install it with `brew install espeak` or `sudo apt install espeak`.")
    