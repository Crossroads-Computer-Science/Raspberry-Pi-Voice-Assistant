# Setup Guide

This guide covers everything you need to get started, regardless of whether you're on **macOS**, **Windows**, or **Linux/Raspberry Pi**.

---

## Step 1: Install Python

You need Python 3.9 or newer.

- **macOS**: Install from [python.org](https://python.org) or use Homebrew: `brew install python`
- **Windows**: Download from [python.org](https://python.org). During install, **check "Add Python to PATH"**
- **Linux/Raspberry Pi**: Usually pre-installed. Check with `python3 --version`

---

## Step 2: Create a Virtual Environment

A virtual environment keeps this project's dependencies separate from the rest of your computer.

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

You'll know it's active when you see `(venv)` at the start of your terminal prompt. **You need to activate it every time you open a new terminal.**

---

## Step 3: Install System Dependencies

### macOS
No extra steps needed. PortAudio (required by `sounddevice`) is bundled, and `say` (text-to-speech) is built into macOS.

### Windows
Install PortAudio via pipwin — this is needed for the `sounddevice` package:
```bash
pip install pipwin
pipwin install pyaudio
```

Also install the text-to-speech library:
```bash
pip install pyttsx3
```

**Important — `webrtcvad` on Windows:**
The standard `webrtcvad` package requires a C compiler to build on Windows, which most students won't have. Install the pre-built version instead:
```bash
pip install webrtcvad-wheels
```
This is a drop-in replacement — the code works identically.

### Linux / Raspberry Pi
```bash
sudo apt-get update
sudo apt-get install portaudio19-dev espeak
```

---

## Step 4: Get an OpenAI API Key

1. Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Sign in or create a free account
3. Click "Create new secret key" and copy it

**About cost:** The APIs used in this project (Whisper for transcription, GPT-4.1-mini for chat) are very affordable for learning. A full session of experimenting typically costs less than $0.10. You can set a monthly spending limit in your OpenAI account settings for peace of mind.

---

## Step 5: Set Up Your API Key (for each module)

Each module folder (03_transcribe and later) needs a `.env` file containing your API key.

**macOS / Linux:**
```bash
cd 03_transcribe
echo "OPENAI_API_KEY=your-key-here" > .env
```

**Windows (Command Prompt):**
```bash
cd 03_transcribe
echo OPENAI_API_KEY=your-key-here > .env
```

**Or create it manually:** Open a text editor, create a file called `.env` (just that, no other extension) inside the module folder, and add this line:
```
OPENAI_API_KEY=your-key-here
```

You'll need a separate `.env` file in each module folder (03 through 07). The key is the same — you're just copying the file.

---

## Step 6: Install Module Dependencies

Each module has its own `requirements.txt`. Navigate to the module folder and install:

```bash
cd 01_record_playback
pip install -r requirements.txt
```

Then run the module:
```bash
python main.py
```

Repeat for each module as you progress through them.

---

## Common Issues

### "No module named X"
Make sure your virtual environment is activated (you should see `(venv)` in your prompt). Then re-run `pip install -r requirements.txt`.

### "No Default Input Device" / microphone not found
- Check that your microphone is plugged in and set as the default input device in your OS sound settings.
- Run `python -c "import sounddevice as sd; print(sd.query_devices())"` to see what devices Python can see.

### Windows: "webrtcvad build failed"
Use `pip install webrtcvad-wheels` instead of `pip install webrtcvad`.

### Windows: "say command not found" / no speech output
Make sure you ran `pip install pyttsx3`.

### "AuthenticationError" from OpenAI
Your API key is wrong or missing. Check that your `.env` file is in the same folder as the module you're running, and that the key starts with `sk-`.

### "Insufficient quota" from OpenAI
Your account is out of credits. Add a small amount (e.g., $5) at [platform.openai.com/billing](https://platform.openai.com/billing).
