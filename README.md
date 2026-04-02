# 🗣️ Raspberry Pi Voice Assistant with OpenAI

This project turns a Raspberry Pi into a sophisticated voice-powered assistant using OpenAI's latest AI models. It's designed as a **progressive learning experience** that builds from basic audio recording to a full-featured AI assistant with function calling capabilities.

---

## 🎯 **Learning Path for Students**

This project is structured as a **step-by-step journey** that teaches you voice assistant development from the ground up. Each folder builds upon the previous one, adding new capabilities and complexity.

### 📚 **Progressive Learning Structure**

| Folder | Topic | What You'll Learn | Difficulty |
|--------|-------|-------------------|------------|
| **01_record_playback** | Audio Basics | Recording and playing audio files | 🟢 Beginner |
| **02_detect_speech** | Voice Activity Detection | Detecting when someone is speaking | 🟢 Beginner |
| **03_transcribe** | Speech-to-Text | Converting speech to text with OpenAI Whisper | 🟡 Intermediate |
| **04_chat_response** | AI Conversations | Getting responses from ChatGPT | 🟡 Intermediate |
| **05_speak_output** | Text-to-Speech | Converting AI responses back to speech | 🟡 Intermediate |
| **06_trigger_word** | Wake Word Detection | Activating the assistant with "Jarvis" | 🟠 Advanced |
| **07_function_calling** | AI Tools | Giving the AI access to real-world functions | 🟠 Advanced |
| **08_raspberry_pi_production** | Production Ready | Full-featured assistant with GPIO and monitoring | 🔴 Expert |

---

## 🚀 **Getting Started**

### **Prerequisites**
- A computer with a microphone and speakers (macOS, Windows, or Linux/Raspberry Pi)
- Python 3.9+
- An OpenAI API Key ([Get one here](https://platform.openai.com/api-keys))

### **Initial Setup**

See **[SETUP.md](./SETUP.md)** for full instructions, including Windows-specific steps (webrtcvad, pyttsx3) and Raspberry Pi system packages.

#### Quick start (macOS / Linux)
```bash
python3 -m venv venv
source venv/bin/activate
cd 01_record_playback
pip install -r requirements.txt
python main.py
```

#### Quick start (Windows)
```bash
python -m venv venv
venv\Scripts\activate
pip install webrtcvad-wheels pyttsx3
cd 01_record_playback
pip install -r requirements.txt
python main.py
```

---

## 📖 **Step-by-Step Learning Guide**

### **Step 1: Audio Fundamentals** 🎵
**Start with:** `01_record_playback/`
- Learn how to record audio from microphone
- Understand audio formats and sampling rates
- Practice playing back recorded audio
- **Goal:** Get comfortable with basic audio I/O

**Try this:** Record yourself saying "Hello Raspberry Pi" and play it back!

### **Step 2: Speech Detection** 🎤
**Move to:** `02_detect_speech/`
- Implement Voice Activity Detection (VAD)
- Learn to detect when someone starts/stops speaking
- Understand audio processing and silence detection
- **Goal:** Automatically detect speech without manual triggers

**Try this:** Speak different phrases and see how the system detects speech boundaries!

### **Step 3: AI Transcription** 📝
**Move to:** `03_transcribe/`
- Integrate OpenAI Whisper API
- Convert speech to text in real-time
- Handle API responses and error handling
- **Goal:** Turn any speech into accurate text

**Try this:** Speak complex sentences and see how accurately they're transcribed!

### **Step 4: AI Conversations** 💬
**Move to:** `04_chat_response/`
- Connect to ChatGPT API
- Generate intelligent responses to user input
- Maintain conversation context
- **Goal:** Have meaningful conversations with your AI

**Try this:** Ask the AI questions and see how it responds!

### **Step 5: Voice Output** 🔊
**Move to:** `05_speak_output/`
- Implement text-to-speech synthesis
- Choose from multiple TTS backends
- Synchronize audio output with AI responses
- **Goal:** Complete the voice interaction loop

**Try this:** Have the AI read back its responses in natural speech!

### **Step 6: Wake Word System** 🎯
**Move to:** `06_trigger_word/`
- Implement "Jarvis" wake word detection
- Create a hands-free activation system
- Optimize for continuous listening
- **Goal:** Make the assistant always ready to help

**Try this:** Say "Jarvis" followed by a question - no buttons needed!

### **Step 7: Function Calling** 🛠️
**Move to:** `07_function_calling/`
- Give your AI access to real-world functions
- Implement weather, time, and timer capabilities
- Learn about AI tool integration
- **Goal:** Make your assistant actually useful for daily tasks

**Try this:** Ask "Jarvis, what's the weather like?" and see it call real APIs!

### **Step 8: Production Deployment** 🚀
**Move to:** `08_raspberry_pi_production/`
- Add GPIO LED indicators
- Implement system monitoring
- Create a production-ready service
- **Goal:** Deploy a professional-grade voice assistant

**Try this:** Monitor your Pi's temperature and performance through voice commands!

---

## 🔧 **Working with Each Module**

### **For Each Folder:**
1. **Navigate to the folder:** `cd 0X_folder_name/`
2. **Check requirements:** `cat requirements.txt`
3. **Install dependencies:** `pip install -r requirements.txt`
4. **Set up environment:** Create `.env` file with your API key
5. **Run the module:** `python main.py`
6. **Test functionality:** Follow the prompts and experiment!

### **Environment Setup for Each Module**
Modules 03–07 require an OpenAI API key. Create a `.env` file in each module folder:
```
OPENAI_API_KEY=your-key-here
```
See [SETUP.md](./SETUP.md) for detailed instructions, including Windows steps.

---

## 🎓 **Learning Objectives**

By completing this project, you'll understand:

- **Audio Processing:** Recording, playback, and voice detection
- **AI Integration:** OpenAI APIs, Whisper, and GPT models
- **System Design:** Progressive complexity and modular architecture
- **Error Handling:** Graceful failure and user experience
- **Production Deployment:** Service management and monitoring
- **Hardware Integration:** GPIO control and system metrics

---

## 🐛 **Common Issues & Solutions**

### **Audio Problems**
```bash
# Check what audio devices Python can see (all platforms)
python -c "import sounddevice as sd; print(sd.query_devices())"
```

### **API Key Issues**
- Ensure `.env` file is in the **same folder** as the module you're running
- Check that `python-dotenv` is installed
- Verify API key is valid and has credits

### **Windows: webrtcvad won't install**
```bash
pip install webrtcvad-wheels
```

### **Windows: no speech output**
```bash
pip install pyttsx3
```

See [SETUP.md](./SETUP.md) for more detailed troubleshooting.

---

## 🎯 **Project Milestones**

- **✅ Milestone 1:** Basic audio recording and playback
- **✅ Milestone 2:** Automatic speech detection
- **✅ Milestone 3:** AI-powered speech transcription
- **✅ Milestone 4:** Intelligent conversation capabilities
- **✅ Milestone 5:** Natural voice output
- **✅ Milestone 6:** Hands-free wake word system
- **✅ Milestone 7:** Real-world function integration
- **✅ Milestone 8:** Production-ready deployment

---

## 🤝 **Getting Help**

- **Check the code:** Each module has detailed comments
- **Review requirements:** Ensure all dependencies are installed
- **Test incrementally:** Work through each step before moving on
- **Use debug mode:** Add print statements to understand what's happening

---

## 🙏 **Credits & Inspiration**

This project was inspired by the excellent tutorial by the [Make It Think](https://www.youtube.com/@MakeItThink) YouTube channel. Watch the original video here: [Voice Assistant on Raspberry Pi](https://www.youtube.com/watch?v=VzSrSiu0syU&ab_channel=MakeItThink).

---

## 🎉 **Next Steps**

After completing this project, consider:
- **Custom Wake Words:** Train your own wake word detection
- **Additional Functions:** Add more AI-powered capabilities
- **Hardware Expansion:** Integrate sensors, displays, or actuators
- **Cloud Integration:** Connect to smart home systems
- **Mobile App:** Create a companion app for remote control

---

**Happy coding! Remember: Every expert was once a beginner. Take it one step at a time! 🚀**