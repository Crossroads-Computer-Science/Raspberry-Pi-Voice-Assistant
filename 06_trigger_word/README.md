# 🎯 Module 6: Wake Word Detection

Welcome to Module 6! Now that your voice assistant can have full conversations, let's make it **always ready to help** by implementing wake word detection. This is where your assistant becomes truly hands-free - just say "Jarvis" and it springs to life, ready to assist you!

---

## 🎯 **What You'll Learn**

- **Wake Word Detection**: Making your assistant respond to a specific trigger phrase
- **Continuous Listening**: Keeping your system always ready for commands
- **Hands-Free Operation**: No more pressing buttons to start conversations
- **Efficiency Optimization**: Only processing audio when the wake word is detected
- **User Experience Design**: Creating natural, intuitive voice interactions

---

## 🔍 **Understanding the Code**

### **Key Concepts**

#### 1. **Wake Word System**
```python
TRIGGER_WORD = "jarvis"  # The wake word that activates the assistant

# Check if trigger word was spoken
if TRIGGER_WORD in user_text.lower():
    print("✨ Trigger word detected! Processing request...")
```
- **What it does**: Listens for a specific word or phrase to activate
- **How it works**: Continuously monitors transcribed speech for the trigger
- **Why it's important**: Makes the system feel responsive and natural
- **Customization**: You can change "jarvis" to any word you prefer

#### 2. **Continuous Listening Loop**
```python
# Keep listening for the trigger word
while True:
    try:
        # Record and process audio
        audio = detect_speech(samplerate=SAMPLERATE)
        user_text = transcribe_audio(audio, samplerate=SAMPLERATE)
        
        # Check if trigger word was spoken
        if TRIGGER_WORD in user_text.lower():
            # Process the request
        else:
            print("❌ Trigger word not found. Waiting for 'Jarvis'...")
```
- **Always on**: System runs continuously, waiting for activation
- **Efficient processing**: Only does heavy work when wake word is detected
- **User feedback**: Shows when it's listening vs. when it's processing
- **Graceful handling**: Manages errors without crashing

#### 3. **Smart Request Processing**
```python
if TRIGGER_WORD in user_text.lower():
    # Extract the actual request (remove the wake word)
    request = user_text.lower().replace(TRIGGER_WORD, "").strip()
    
    # Process the request and get AI response
    response = get_chatgpt_response(messages)
    speak_text(response)
```
- **Request extraction**: Removes "Jarvis" from the actual command
- **Context preservation**: Maintains conversation history
- **Full response**: Gets AI response and speaks it back
- **Seamless experience**: From wake word to response in one flow

---

## 📁 **File Structure**

```
06_trigger_word/
├── main.py              # Main wake word application
├── audio.py             # Audio recording functions
├── chat.py              # ChatGPT integration
├── speak.py             # Text-to-speech functions
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

---

## 🔧 **How It Works**

### **Step 1: Always Listening**
```python
# 1. Start the continuous listening loop
while True:
    try:
        # 2. Record audio and transcribe it
        audio = detect_speech(samplerate=SAMPLERATE)
        user_text = transcribe_audio(audio, samplerate=SAMPLERATE)
        
        # 3. Check for the wake word
        if TRIGGER_WORD in user_text.lower():
            # Wake word detected - process request
        else:
            # No wake word - keep listening
```

**What happens:**
- System starts and begins listening continuously
- Audio is recorded and transcribed in real-time
- Each transcription is checked for the wake word "Jarvis"
- System provides feedback about what it's doing

### **Step 2: Wake Word Detection**
```python
# 1. Check if "jarvis" is in the transcribed text
if TRIGGER_WORD in user_text.lower():
    print("✨ Trigger word detected! Processing request...")
    
    # 2. Extract the actual request
    request = user_text.lower().replace(TRIGGER_WORD, "").strip()
    
    # 3. Add to conversation and get AI response
    messages.append({"role": "user", "content": user_text})
    response = get_chatgpt_response(messages)
```

**What happens:**
- System detects "Jarvis" in your speech
- It extracts your actual request (removes "Jarvis")
- Request is added to conversation history
- AI generates a response based on your request

### **Step 3: Response and Return to Listening**
```python
# 1. Speak the AI response
speak_text(response)

# 2. Add response to conversation history
messages.append({"role": "assistant", "content": response})

# 3. Return to listening mode
print("🎙️ Listening for trigger word 'Jarvis'...")
```

**What happens:**
- Jarvis speaks its response to you
- Response is saved in conversation history
- System returns to listening mode
- Ready for your next "Jarvis" command

---

## 🎮 **Running the Code**

### **1. Navigate to the folder**
```bash
cd 06_trigger_word
```

### **2. Install dependencies**
```bash
pip install -r requirements.txt
```

### **3. Set up your API key**
```bash
# Create .env file with your OpenAI API key
echo "OPENAI_API_KEY=your_actual_api_key_here" > .env
```

### **4. Run the program**
```bash
python main.py
```

### **5. Experience hands-free operation!**
- **"🎙️ Listening for trigger word 'Jarvis'..."** - System is ready
- **Say "Jarvis" + your request** - Wake word activates the system
- **"✨ Trigger word detected!"** - System is processing your request
- **Jarvis responds** - You get your answer
- **Returns to listening** - Ready for next command

---

## 🧪 **Experiments to Try**

### **Basic Wake Word Testing**
1. **Simple activation**: Say "Jarvis, hello" and see it respond
2. **Different requests**: "Jarvis, what time is it?" or "Jarvis, tell me a joke"
3. **Wake word placement**: Try "Hello Jarvis" vs "Jarvis hello"

### **Advanced Testing**
1. **Conversation flow**: Have multiple exchanges with Jarvis
2. **Background noise**: Test wake word detection in noisy environments
3. **Different voices**: Test with different people saying "Jarvis"
4. **Wake word variations**: Try "Hey Jarvis" or "Jarvis please"

### **Performance Testing**
1. **Response time**: How quickly does it detect and respond?
2. **False positives**: Does it activate when you don't say "Jarvis"?
3. **Battery usage**: Monitor system resources during continuous listening
4. **Memory usage**: Check if conversation history grows properly

---

## 🔍 **Understanding the Output**

### **What You'll See**
```
🎙️ Listening for trigger word 'Jarvis'...
🛑 Silence detected. Transcribing...
📝 You said: Jarvis, what's the weather like?
✨ Trigger word detected! Processing request...
🤖 Jarvis: [AI response about weather]
🔊 Speaking complete.
🎙️ Listening for trigger word 'Jarvis'...
```

### **What Each Line Means**
- **🎙️**: System is actively listening for wake word
- **🛑**: Processing detected speech
- **📝**: What the system heard you say
- **✨**: Wake word detected - processing your request
- **🤖**: Jarvis's response
- **🔊**: TTS playback complete
- **🎙️**: Back to listening mode

---

## 🐛 **Common Issues & Solutions**

### **"Wake word not being detected"**
- **Speak clearly**: Make sure "Jarvis" is pronounced clearly
- **Check transcription**: See if "Jarvis" appears in the transcribed text
- **Reduce background noise**: Quiet environment helps with detection
- **Adjust microphone**: Better mic = better wake word detection

### **"System not responding after wake word"**
- **Check API key**: Make sure OpenAI API is working
- **Verify internet**: ChatGPT needs internet connection
- **Check conversation flow**: Make sure messages are being added properly

### **"High CPU usage during listening"**
- **Optimize audio processing**: Reduce sample rate or chunk size
- **Add delays**: Increase sleep time in the main loop
- **Monitor resources**: Use `htop` to see what's using CPU

---

## 🤔 **Wait, How Does Wake Word Detection Actually Work?**

Great question! Let me explain this in a way that makes sense without getting too technical.

### **The Magic Behind the Scenes**

Think of wake word detection like having a really attentive friend who's always listening to you, but only pays attention when you say their name. This friend can hear everything you're saying, but they only "wake up" and start helping when you specifically call them.

**Here's what's happening:**
Your system is constantly listening to everything around it, just like you might hear background noise, music, or other people talking. But it's specifically listening for the pattern of sounds that make up the word "Jarvis." When it hears that pattern, it's like flipping a switch from "listening mode" to "helping mode."

**Why this is so clever:**
Instead of your computer constantly trying to process every sound it hears (which would be exhausting and waste battery), it only does the heavy lifting when you actually want help. It's like having a smart light switch that only turns on the lights when you say "turn on the lights" instead of trying to turn them on for every sound it hears.

### **Real-World Example**
Think about how you might be in a room with lots of people talking, but when someone says your name, you immediately perk up and pay attention. That's exactly what your wake word system does! It can ignore all the background conversation, but the moment it hears "Jarvis," it's like someone tapped you on the shoulder and said "Hey, you're needed!"

**The key insight:** Wake word detection isn't about understanding everything you're saying - it's about being really good at recognizing one specific pattern (your wake word) so it can save energy and only help when you actually want it to!

---

## 🔗 **What's Next**

After mastering this module, you'll be ready for:
- **Module 7**: Giving Jarvis access to real-world tools and functions
- **Module 8**: Building a production-ready voice assistant with hardware integration

---

## 💡 **Pro Tips**

1. **Choose a unique wake word**: "Jarvis" is good, but avoid common words like "Hey" or "Hello"
2. **Test in your environment**: Background noise affects wake word detection
3. **Monitor system resources**: Continuous listening uses more CPU than on-demand
4. **Customize the experience**: Change the wake word to something personal
5. **Practice clear pronunciation**: Clear wake word = better detection

---

## 🎓 **Learning Check**

**Before moving to Module 7, you should be able to:**
- ✅ Explain what wake word detection is and why it's useful
- ✅ Understand how continuous listening works
- ✅ Successfully activate Jarvis with the wake word
- ✅ Explain the difference between listening mode and processing mode
- ✅ Troubleshoot common wake word detection issues
- ✅ Understand how the system optimizes for efficiency

---

**🎉 Outstanding! You've now mastered wake word detection. Your voice assistant is truly hands-free and always ready to help. Just say "Jarvis" and it springs to life - this is the kind of technology you see in sci-fi movies!**
