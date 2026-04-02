# Module 2: Voice Activity Detection (VAD)

> **What you'll build:** A program that listens continuously and only captures audio when you speak, stopping when you go quiet.
>
> **What's new:** `webrtcvad` for speech detection, the generator-based audio stream, and the ring buffer algorithm.
>
> **What carries over:** `audio.py` from this module is reused (nearly identically) in all future modules.

Welcome to Module 2! Now that you can record and play audio, let's make your system **intelligent** — it will automatically detect when someone is speaking and when they stop. This is the foundation for hands-free voice interaction!

---

## 🎯 **What You'll Learn**

- **Voice Activity Detection (VAD)**: Automatically detecting speech vs. silence
- **Real-time Audio Processing**: Processing audio as it comes in, not just after recording
- **Audio Analysis**: Understanding audio energy, frequency characteristics, and patterns
- **Continuous Monitoring**: Keeping your system always listening for speech
- **Performance Optimization**: Efficient audio processing for real-time applications

---

## 🔍 **Understanding the Code**

### **Key Concepts**

#### 1. **Voice Activity Detection (VAD)**
```python
import webrtcvad
vad = webrtcvad.Vad(2)  # Aggressiveness level 2
```
- **What it does**: Analyzes audio to determine if someone is speaking
- **How it works**: Uses machine learning to detect speech patterns
- **Aggressiveness levels**: 0-3 (0=least aggressive, 3=most aggressive)
- **Why level 2**: Good balance between detecting speech and avoiding false positives

#### 2. **Real-time Audio Streaming (Generator Pattern)**
```python
def audio_stream(samplerate=16000, frame_duration_ms=30):
    frame_size = int(samplerate * frame_duration_ms / 1000)
    with sd.InputStream(samplerate=samplerate, channels=1, dtype='int16') as stream:
        while True:
            audio = stream.read(frame_size)[0].flatten()
            yield audio  # hand one frame to the caller, then pause until asked for the next
```
- **Generator vs. callback**: Instead of registering a callback function, we use a Python generator (`yield`). The caller pulls one frame at a time.
- **Frame-based processing**: Audio is processed in small 30ms chunks
- **Continuous operation**: The `while True` loop keeps producing frames until we stop iterating

#### 3. **The Ring Buffer Algorithm**
```python
ring_buffer = collections.deque(maxlen=int(700 / frame_duration_ms))  # ~700ms window

# Phase 1: waiting for speech to start
ring_buffer.append(frame)
num_voiced = len([f for f in ring_buffer if vad.is_speech(f.tobytes(), samplerate)])
if num_voiced > 0.9 * ring_buffer.maxlen:
    triggered = True  # speech confirmed!

# Phase 2: recording speech, watching for silence
num_unvoiced = len([f for f in ring_buffer if not vad.is_speech(f.tobytes(), samplerate)])
if num_unvoiced > 0.9 * ring_buffer.maxlen:
    break  # sustained silence — speaker has finished
```
- **Why a ring buffer?** VAD can be "jumpy" — a single quiet frame doesn't mean the speaker stopped. By requiring 90% of a 700ms window to be silent, we get smooth, natural boundaries.
- **The lead-in**: When speech is confirmed, we include all the frames already in the buffer, so we don't miss the start of the first word.

---

## 📁 **File Structure**

```
02_detect_speech/
├── main.py              # Main VAD application
├── audio.py             # VAD processing functions
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

---

## 🔧 **How It Works**

### **Step 1: Initialize VAD System**
```python
# 1. Create VAD instance with desired aggressiveness
vad = webrtcvad.Vad(2)

# 2. Calculate chunk size for real-time processing
chunk_duration = 0.03  # 30 milliseconds
chunk_size = int(samplerate * chunk_duration)
```

**What happens:**
- VAD model is loaded into memory
- Audio chunk size is calculated based on sample rate
- System prepares for continuous audio monitoring

### **Step 2: Stream Audio Frame by Frame**
```python
for frame in audio_stream(samplerate, frame_duration_ms):
    is_speech = vad.is_speech(frame.tobytes(), samplerate)
    # ... ring buffer logic
```

**What happens:**
- `audio_stream()` opens the microphone and yields one 30ms chunk at a time
- Each frame is immediately checked by VAD
- The `for` loop runs until we `break` out of it (when sustained silence is detected)

### **Step 3: React to VAD Results**
```python
if not triggered:
    ring_buffer.append(frame)
    if num_voiced > 0.9 * ring_buffer.maxlen:
        triggered = True           # speech confirmed — start collecting
        voiced_frames.extend(ring_buffer)
else:
    voiced_frames.append(frame)    # already recording — keep accumulating
    if num_unvoiced > 0.9 * ring_buffer.maxlen:
        break                      # sustained silence — we're done
```

**What happens:**
- Before speech: buffer fills up; 90% voiced frames trigger recording mode
- During speech: every frame is saved to `voiced_frames`
- After speech: 90% silent frames in the buffer means the speaker stopped

---

## 🎮 **Running the Code**

### **1. Navigate to the folder**
```bash
cd 02_detect_speech
```

### **2. Install dependencies**
```bash
pip install -r requirements.txt
```

### **3. Run the program**
```bash
python main.py
```

### **4. Watch the magic happen!**
- **"🎙️ Voice Activity Detection Demo"** - System is starting
- **"🎤 Speech detected!"** - You're speaking
- **"🔇 Silence..."** - You're quiet
- **Press Ctrl+C** to stop the program

---

## 🧪 **Experiments to Try**

### **Basic VAD Testing**
1. **Speak clearly**: Say "Hello, this is a test" and watch for detection
2. **Test silence**: Stop talking and see silence detection
3. **Vary speech patterns**: Try different speaking speeds and volumes

### **Advanced VAD Testing**
1. **Background noise**: Test with music or TV in background
2. **Whisper vs. shout**: See how VAD handles different volumes
3. **Different languages**: Test with non-English speech
4. **Music vs. speech**: Play music and see if VAD gets confused

### **Performance Testing**
1. **Monitor CPU usage**: Run `htop` in another terminal
2. **Test responsiveness**: How quickly does it detect speech?
3. **Memory usage**: Check if memory usage stays constant

---

## 🔍 **Understanding the Output**

### **What You'll See**
```
🎙️ Voice Activity Detection Demo
🎤 Speech detected!
🎤 Speech detected!
🎤 Speech detected!
🔇 Silence...
🔇 Silence...
🎤 Speech detected!
🎤 Speech detected!
🔇 Silence...
```

### **What Each Line Means**
- **🎙️**: VAD system started successfully
- **🎤**: VAD detected speech in the current audio chunk
- **🔇**: VAD detected silence in the current audio chunk
- **Continuous updates**: New status every 30ms (or whatever chunk size you set)

---

## 🐛 **Common Issues & Solutions**

### **"VAD not detecting speech"**
```bash
# Check microphone input levels
alsamixer

# Test with system audio tools
arecord -d 5 test.wav
aplay test.wav

# Verify VAD installation
python -c "import webrtcvad; print('VAD installed')"
```

### **"Too many false positives"**
```python
# Reduce VAD aggressiveness
vad = webrtcvad.Vad(1)  # Try level 1 instead of 2

# Or increase chunk size for more stable detection
chunk_duration = 0.05  # 50ms chunks
```

### **"High CPU usage"**
```python
# Increase sleep time in main loop
time.sleep(0.2)  # 200ms instead of 100ms

# Or reduce chunk frequency
chunk_duration = 0.05  # Larger chunks = fewer processing calls
```

---

## 🧠 **Key Learning Points**

### **VAD Fundamentals**
- **Speech vs. noise**: VAD distinguishes human speech from background sounds
- **Real-time processing**: Audio is analyzed as it arrives, not after recording
- **Chunk-based analysis**: Small audio pieces are processed independently
- **Machine learning**: VAD uses trained models to recognize speech patterns

### **Audio Processing Concepts**
- **Streaming audio**: Continuous data flow vs. batch processing
- **Callback functions**: Event-driven programming for real-time systems
- **Audio buffers**: Managing memory for continuous audio processing
- **Performance optimization**: Balancing accuracy with system resources

### **System Design Principles**
- **Separation of concerns**: VAD logic separate from audio I/O
- **Error handling**: Graceful degradation when audio devices fail
- **Resource management**: Proper cleanup of audio streams
- **User experience**: Immediate feedback for speech detection

---

## Stretch Challenges

1. **Tune the aggressiveness** — change `vad_level` from 2 to 0 or 3. What breaks? What improves?
2. **Adjust the silence window** — change `700` in `maxlen=int(700 / frame_duration_ms)` to `300` or `1500`. How does it affect when recording stops?
3. **Count the frames** — add a print statement inside the `for` loop counting how many total frames were processed vs. how many made it into `voiced_frames`. What ratio do you get for a short sentence?
4. **Visualize it** — after `detect_speech()` returns, plot the audio array with `import matplotlib.pyplot as plt; plt.plot(audio); plt.show()`. Can you see where speech starts and ends?

## What's Next

After mastering this module, you'll be ready for:
- **Module 3**: Converting detected speech to text (Speech-to-Text)
- **Module 4**: Getting AI responses to transcribed speech
- **Module 5**: Speaking AI responses back to the user

---

## 💡 **Pro Tips**

1. **Start with clear speech**: Good microphone input = better VAD results
2. **Adjust aggressiveness**: Level 2 is usually good, but adjust based on your environment
3. **Monitor performance**: Watch CPU usage and adjust chunk sizes accordingly
4. **Test in your environment**: VAD performance varies with background noise
5. **Use quality audio**: Better microphone = more reliable speech detection

---

## 🎓 **Learning Check**

**Before moving to Module 3, you should be able to:**
- ✅ Explain what Voice Activity Detection is and why it's useful
- ✅ Understand how real-time audio streaming works
- ✅ Explain the difference between streaming and recording audio
- ✅ Modify VAD aggressiveness and see the effects
- ✅ Troubleshoot common VAD issues
- ✅ Explain how audio chunking works for real-time processing

---

## 🤔 **Wait, How Does VAD Actually Work?**

Great question! Let me explain this in a way that makes sense without getting too technical.

### **The Magic Behind the Scenes**

Think of VAD like having a really smart friend who's always listening to you, but only pays attention when you're actually talking. This friend doesn't just listen for loud sounds - they're specifically listening for the patterns that make up human speech.

**Here's what's happening:**
When you speak, your voice creates specific sound patterns that are different from background noise like a fan, music, or someone typing on a keyboard. VAD has been trained (using lots of examples) to recognize these speech patterns. It's like teaching a computer to recognize the difference between someone saying "hello" and the sound of a car driving by outside.

**Why this is so cool:**
Instead of your computer constantly trying to process every sound it hears (which would be exhausting and waste battery), VAD acts like a smart filter. It only wakes up the heavy-duty processing when it thinks you're actually talking to it. This is why your phone's voice assistant doesn't respond to every random noise in the room!

### **Real-World Example**
Imagine you're in a coffee shop. There's background music, people chatting, coffee machines whirring, and maybe a baby crying. VAD is smart enough to ignore all of that background noise, but when you lean in and say "Hey Siri" or "OK Google," it immediately recognizes that as human speech and activates the voice assistant.

**The key insight:** VAD doesn't just detect "sound" - it detects "speech." This is a huge difference that makes modern voice assistants possible!

---

**🎉 Excellent! You've now mastered real-time audio processing. Your system can automatically detect when someone is speaking - this is the foundation for truly intelligent voice interaction!**
