# 🗣️ Raspberry Pi Voice Assistant with OpenAI

This project turns a Raspberry Pi into a simple voice-powered assistant using the OpenAI API for natural language responses. It records speech, transcribes it to text, generates a response using GPT, and speaks it back using `espeak`.

---

## 🛠️ Features

- 🎙️ Voice input (via microphone)
- 💬 Transcription to text using OpenAI Whisper
- 🧠 Natural language response via OpenAI GPT
- 🔊 Spoken output using `espeak`
- 🐍 Python-based, runs on Raspberry Pi

---

## 🧰 Requirements

- A Raspberry Pi (any model with internet and audio support)
- Microphone input
- Speaker output (3.5mm jack or HDMI)
- Python 3.7+
- An OpenAI API Key

---

## 📦 Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/pi-voice-assistant.git
cd pi-voice-assistant
```
### 2. Create a virtual environment (recommended)
```bash
python3 -m venv venv
source venv/bin/activate
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Install system packages
```bash
sudo apt-get update
sudo apt-get install portaudio19-dev espeak ffmpeg
```
### 5. OpenAI API Key
- Add your OpenAI API Key
- Create a file called .env.local with your api key, or load it via the terminal:
```bash
export OPENAI_API_KEY=your-api-key
```
---

### 🙏 Credits

This project was inspired by the excellent tutorial by the [Make It Think](https://www.youtube.com/@MakeItThink) YouTube channel. Watch the original video here: [Voice Assistant on Raspberry Pi](https://www.youtube.com/watch?v=VzSrSiu0syU&ab_channel=MakeItThink).