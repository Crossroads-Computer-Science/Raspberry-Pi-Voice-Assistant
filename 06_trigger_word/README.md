# Module 6: Wake Word Detection

> **What you'll build:** A continuously listening assistant that only responds when you say "Jarvis" — and remembers the whole conversation across multiple interactions.
>
> **What's new:** The infinite `while True` loop that keeps Jarvis always listening; wake word detection by checking the transcription for "jarvis".
>
> **What carries over:** `audio.py`, `chat.py`, `speak.py` from Module 5 are essentially unchanged.

Welcome to Module 6! Now that your voice assistant can have full conversations, let's make it **always ready to help** by implementing wake word detection. This is where your assistant becomes truly hands-free - just say "Jarvis" and it springs to life, ready to assist you!

---

##  **What You'll Learn**

- **Wake Word Detection**: Making your assistant respond to a specific trigger phrase
- **Continuous Listening**: Keeping your system always ready for commands
- **Hands-Free Operation**: No more pressing buttons to start conversations
- **Efficiency Optimization**: Only processing audio when the wake word is detected
- **User Experience Design**: Creating natural, intuitive voice interactions

---

##  **Understanding the Code**

### **Key Concepts**

#### 1. **Wake Word System**
```python
TRIGGER_WORD = "jarvis"  # The wake word that activates the assistant

# Check if trigger word was spoken
if TRIGGER_WORD in user_text.lower():
    print(" Trigger word detected! Processing request...")
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
            print(" Trigger word not found. Waiting for 'Jarvis'...")
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

##  **File Structure**

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

##  **How It Works**

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
    print(" Trigger word detected! Processing request...")
    
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
print(" Listening for trigger word 'Jarvis'...")
```

**What happens:**
- Jarvis speaks its response to you
- Response is saved in conversation history
- System returns to listening mode
- Ready for your next "Jarvis" command

---

##  **Running the Code**

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
- **" Listening for trigger word 'Jarvis'..."** - System is ready
- **Say "Jarvis" + your request** - Wake word activates the system
- **" Trigger word detected!"** - System is processing your request
- **Jarvis responds** - You get your answer
- **Returns to listening** - Ready for next command

---

##  **Experiments to Try**

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

##  **Understanding the Output**

### **What You'll See**
```
 Listening for trigger word 'Jarvis'...
 Silence detected. Transcribing...
 You said: Jarvis, what's the weather like?
 Trigger word detected! Processing request...
 Jarvis: [AI response about weather]
 Speaking complete.
 Listening for trigger word 'Jarvis'...
```

### **What Each Line Means**
- ****: System is actively listening for wake word
- ****: Processing detected speech
- ****: What the system heard you say
- ****: Wake word detected - processing your request
- ****: Jarvis's response
- ****: TTS playback complete
- ****: Back to listening mode

---

##  **Common Issues & Solutions**

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

## How Wake Word Detection Actually Works

### Our simplified approach

This module detects "Jarvis" by:
1. Listening until you stop speaking
2. Sending the audio to Whisper for transcription
3. Checking if the word "jarvis" appears in the transcribed text

This works, but it's slow — you have to finish speaking, wait for the transcription, and then find out whether it was a wake word or not.

### How Alexa, Siri, and "Hey Google" actually work

Real voice assistants use a completely different approach. They run a tiny, dedicated **wake word model** (just a few megabytes) that runs entirely on-device, 24/7, without sending anything to the cloud. This model only has one job: recognize the specific sound pattern of "Alexa" or "Hey Siri." It's fast, cheap, and private.

Only *after* the wake word is detected does the device start recording and sending audio to the cloud for full speech recognition.

Our version sends everything to the cloud for transcription first — which is simpler to build but costs API credits for every background noise it picks up. It's a great learning prototype, but this is why real products need a different architecture.

**Think about:** If you wanted to build a truly low-latency, always-on wake word detector, what would you need? Look up "Porcupine wake word" or "openWakeWord" if you're curious.

---

## Stretch Challenges

1. **Change the wake word** — edit `TRIGGER_WORD = "jarvis"` to something else. Try a two-word phrase like `"hey computer"`. What happens?
2. **Add a sleeping mode** — after Jarvis responds, make it say "Going to sleep" and require you to say the wake word twice in a row before it responds again.
3. **Multiple wake words** — modify the check so that either "jarvis" or "computer" activates the assistant.
4. **Measure the cost** — after 10 interactions, check your OpenAI dashboard. How many API calls did Jarvis make per interaction? (Hint: every transcription — including the ignored ones — costs something.)

## What's Next

After mastering this module, you'll be ready for:
- **Module 7**: Giving Jarvis access to real-world tools and functions

---

##  **Pro Tips**

1. **Choose a unique wake word**: "Jarvis" is good, but avoid common words like "Hey" or "Hello"
2. **Test in your environment**: Background noise affects wake word detection
3. **Monitor system resources**: Continuous listening uses more CPU than on-demand
4. **Customize the experience**: Change the wake word to something personal
5. **Practice clear pronunciation**: Clear wake word = better detection

---

##  **Learning Check**

**Before moving to Module 7, you should be able to:**
-  Explain what wake word detection is and why it's useful
-  Understand how continuous listening works
-  Successfully activate Jarvis with the wake word
-  Explain the difference between listening mode and processing mode
-  Troubleshoot common wake word detection issues
-  Understand how the system optimizes for efficiency

---

** Outstanding! You've now mastered wake word detection. Your voice assistant is truly hands-free and always ready to help. Just say "Jarvis" and it springs to life - this is the kind of technology you see in sci-fi movies!**
