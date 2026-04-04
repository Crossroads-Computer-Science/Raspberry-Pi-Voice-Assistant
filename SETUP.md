# Setup Guide

- [Mac Setup](#mac-setup)
- [Windows Setup](#windows-setup)

---

## Mac Setup

### 1. Open the Project in VS Code

Open VS Code, then go to **File > Open Folder** and select the `Raspberry-Pi-Voice-Assistant` folder.

### 2. Create a Virtual Environment

Open the VS Code terminal (**Terminal > New Terminal**) and run:

```bash
python3 -m venv .venv
```

VS Code will detect the new environment and ask if you want to use it — click **Yes**. From now on, VS Code will automatically activate it whenever you open a terminal in this project.

### 3. Get an OpenAI API Key

1. Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click **Create new secret key** and copy it

**About cost:** The APIs used here (Whisper for transcription, GPT-4.1-mini for chat) are very affordable. A full session of experimenting typically costs less than $0.10. You can set a monthly spending limit in your OpenAI account settings.

### 4. Work Through Each Module

For each module, open the module folder in VS Code's file explorer, run the `pip install` command in the terminal, then open `main.py` and press the **Run** button (the play triangle at the top right).

#### Module 01 - Record & Playback

```bash
pip install sounddevice numpy
```

Then open `01_record_playback/main.py` and run it.

#### Module 02 - Detect Speech

```bash
pip install sounddevice numpy webrtcvad
```

Then open `02_detect_speech/main.py` and run it.

#### Module 03 - Transcribe

First, create a file called `.env` inside the `03_transcribe` folder. Open it in VS Code and add:

```
OPENAI_API_KEY=your-key-here
```

Then:

```bash
pip install sounddevice numpy webrtcvad openai python-dotenv scipy
```

Open `03_transcribe/main.py` and run it.

#### Module 04 - Chat Response

Create a `.env` file inside `04_chat_response` with your API key (same as above).

```bash
pip install sounddevice numpy webrtcvad openai python-dotenv scipy
```

Open `04_chat_response/main.py` and run it.

#### Module 05 - Speak Output

Create a `.env` file inside `05_speak_output` with your API key.

```bash
pip install sounddevice numpy webrtcvad openai python-dotenv scipy
```

Open `05_speak_output/main.py` and run it.

#### Module 06 - Trigger Word

Create a `.env` file inside `06_trigger_word` with your API key.

```bash
pip install sounddevice numpy webrtcvad openai python-dotenv scipy
```

Open `06_trigger_word/main.py` and run it.

#### Module 07 - Function Calling

Create a `.env` file inside `07_function_calling` with your API key.

```bash
pip install sounddevice numpy webrtcvad openai python-dotenv scipy requests
```

Open `07_function_calling/main.py` and run it.

---

## Windows Setup

### 1. Open the Project in VS Code

Open VS Code, then go to **File > Open Folder** and select the `Raspberry-Pi-Voice-Assistant` folder.

### 2. Create a Virtual Environment

Open the VS Code terminal (**Terminal > New Terminal**) and run:

```cmd
python -m venv .venv
```

VS Code will detect the new environment and ask if you want to use it — click **Yes**. From now on, VS Code will automatically activate it whenever you open a terminal in this project.

### 3. Install PortAudio and Text-to-Speech

`sounddevice` requires PortAudio, and Windows needs a separate text-to-speech library. Run these in the terminal:

```cmd
pip install pipwin
pipwin install pyaudio
pip install pyttsx3
```

### 4. Get an OpenAI API Key

1. Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click **Create new secret key** and copy it

**About cost:** A full session of experimenting typically costs less than $0.10. You can set a monthly spending limit in your OpenAI account settings.

### 5. Work Through Each Module

For each module, run the `pip install` command in the VS Code terminal, then open `main.py` and press the **Run** button (the play triangle at the top right).

#### Module 01 - Record & Playback

```cmd
pip install sounddevice numpy
```

Then open `01_record_playback/main.py` and run it.

#### Module 02 - Detect Speech

> **Note:** Use `webrtcvad-wheels` instead of `webrtcvad` — it's a pre-built version that avoids a compiler error on Windows.

```cmd
pip install sounddevice numpy webrtcvad-wheels
```

Then open `02_detect_speech/main.py` and run it.

#### Module 03 - Transcribe

First, create a file called `.env` inside the `03_transcribe` folder. Open it in VS Code and add:

```
OPENAI_API_KEY=your-key-here
```

Then:

```cmd
pip install sounddevice numpy webrtcvad-wheels openai python-dotenv scipy
```

Open `03_transcribe/main.py` and run it.

#### Module 04 - Chat Response

Create a `.env` file inside `04_chat_response` with your API key (same as above).

```cmd
pip install sounddevice numpy webrtcvad-wheels openai python-dotenv scipy
```

Open `04_chat_response/main.py` and run it.

#### Module 05 - Speak Output

Create a `.env` file inside `05_speak_output` with your API key.

```cmd
pip install sounddevice numpy webrtcvad-wheels openai python-dotenv scipy pyttsx3
```

Open `05_speak_output/main.py` and run it.

#### Module 06 - Trigger Word

Create a `.env` file inside `06_trigger_word` with your API key.

```cmd
pip install sounddevice numpy webrtcvad-wheels openai python-dotenv scipy pyttsx3
```

Open `06_trigger_word/main.py` and run it.

#### Module 07 - Function Calling

Create a `.env` file inside `07_function_calling` with your API key.

```cmd
pip install sounddevice numpy webrtcvad-wheels openai python-dotenv scipy requests pyttsx3
```

Open `07_function_calling/main.py` and run it.

---

## Common Issues

**VS Code says "Select Interpreter" or can't find packages**
Click the Python version shown in the bottom-left status bar and select the `.venv` option from the list. Then open a new terminal and try again.

**"No module named X"**
The virtual environment may not be active in your current terminal. Close the terminal, open a new one in VS Code (**Terminal > New Terminal**), and re-run the `pip install` line.

**Microphone not found / "No Default Input Device"**
Check that your microphone is plugged in and set as the default input in your OS sound settings. To see what Python detects, run in the terminal:
```bash
python3 -c "import sounddevice as sd; print(sd.query_devices())"
```

**Windows: webrtcvad build error**
Use `pip install webrtcvad-wheels` instead of `pip install webrtcvad`.

**"AuthenticationError" from OpenAI**
Your `.env` file is missing or in the wrong folder. Make sure it's inside the module folder you're running, and that the key starts with `sk-`.

**"Insufficient quota" from OpenAI**
Your account is out of credits. Add a small amount at [platform.openai.com/billing](https://platform.openai.com/billing).
