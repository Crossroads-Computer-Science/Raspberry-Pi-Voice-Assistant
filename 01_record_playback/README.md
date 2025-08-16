# 🎵 Module 1: Audio Recording & Playback

Welcome to your first step in building a Raspberry Pi Voice Assistant! This module teaches you the **fundamentals of audio processing** - the building blocks that everything else will be built upon.

---

## 🎯 **What You'll Learn**

- **Audio Input/Output**: How to record from a microphone and play through speakers
- **Audio Formats**: Understanding sample rates, channels, and data types
- **Python Audio Libraries**: Working with `sounddevice` and `numpy`
- **Basic Error Handling**: Graceful failure when audio devices aren't available
- **Audio Processing Pipeline**: The foundation for voice recognition

---

## 🔍 **Understanding the Code**

### **Key Concepts**

#### 1. **Audio Sampling**
```python
SAMPLERATE = 16000  # 16,000 samples per second
```
- **What it means**: Audio is captured 16,000 times per second
- **Why 16kHz**: Human speech contains frequencies up to ~8kHz, so 16kHz gives us good quality
- **Higher rates**: 44.1kHz (CD quality) would be overkill for speech

#### 2. **Audio Data Types**
```python
dtype=np.int16  # 16-bit integer audio data
```
- **16-bit**: Each audio sample is stored as a number from -32,768 to +32,767
- **Why integers**: Easier for computers to process than floating-point
- **Dynamic range**: 96 decibels (from whisper to shout)

#### 3. **Audio Channels**
```python
channels=1  # Mono audio (single channel)
```
- **Mono vs Stereo**: Speech recognition works better with mono
- **Simpler processing**: One channel = half the data to process
- **Better for Pi**: Less memory and CPU usage

---

## 📁 **File Structure**

```
01_record_playback/
├── main.py              # Main application (what you run)
├── audio.py             # Audio processing functions
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

---

## 🔧 **How It Works**

### **Step 1: Audio Recording**
```python
# 1. Open audio input stream
with sd.InputStream(samplerate=SAMPLERATE, channels=1, dtype=np.int16) as stream:
    
    # 2. Record audio data
    audio_data, overflowed = stream.read(FRAMES)
    
    # 3. Convert to numpy array
    audio = np.frombuffer(audio_data, dtype=np.int16)
```

**What happens:**
- Microphone captures sound waves
- Sound card converts analog to digital
- Python receives raw audio data
- Data is converted to numpy array for processing

### **Step 2: Audio Playback**
```python
# 1. Play the audio
sd.play(audio, SAMPLERATE)

# 2. Wait for playback to complete
sd.wait()
```

**What happens:**
- Numpy array is sent to sound card
- Sound card converts digital to analog
- Speakers produce sound waves
- You hear your recorded audio!

---

## 🎮 **Running the Code**

### **1. Navigate to the folder**
```bash
cd 01_record_playback
```

### **2. Install dependencies**
```bash
pip install -r requirements.txt
```

### **3. Run the program**
```bash
python main.py
```

### **4. Follow the prompts**
- **"Press Enter to start recording..."** - Get ready to speak
- **"Recording... (speak now)"** - Say something interesting!
- **"Press Enter to stop recording..."** - Stop when you're done
- **"Playing back..."** - Listen to your recording

---

## 🧪 **Experiments to Try**

### **Basic Experiments**
1. **Record different sounds**: Speech, music, ambient noise
2. **Vary recording length**: Short phrases vs. long sentences
3. **Test different volumes**: Whisper, normal speech, shouting

### **Advanced Experiments**
1. **Modify sample rate**: Change `SAMPLERATE` to 8000 or 44100
2. **Change data type**: Try `np.float32` instead of `np.int16`
3. **Add effects**: Multiply audio by 0.5 to make it quieter

### **Debugging Experiments**
1. **Check audio devices**: What microphones/speakers are available?
2. **Monitor memory usage**: How much RAM does audio processing use?
3. **Test error handling**: What happens when you unplug your microphone?

---

## 🔍 **Understanding the Output**

### **What You'll See**
```
🎙️ Audio Recording and Playback Demo
Press Enter to start recording...
Recording... (speak now)
Press Enter to stop recording...
✅ Recording complete! Audio length: 3.2 seconds
🔁 Playing back the recorded speech...
🎵 Playback complete!
```

### **What Each Line Means**
- **🎙️**: Program started successfully
- **Recording...**: Audio is being captured
- **✅**: Recording completed successfully
- **Audio length**: How long your recording is
- **🔁**: Playing back your audio
- **🎵**: Playback completed

---

## 🐛 **Common Issues & Solutions**

### **"No Default Input Device"**
```bash
# Check available audio devices
python -c "import sounddevice as sd; print(sd.query_devices())"

# Install audio system packages
sudo apt-get install portaudio19-dev
```

### **"No Default Output Device"**
```bash
# Check speaker connections
aplay -l

# Test with system audio
speaker-test -t wav -c 2
```

### **"Audio Quality Issues"**
- **Echo/Feedback**: Move microphone away from speakers
- **Low Volume**: Check microphone gain in system settings
- **Background Noise**: Use a quiet environment or better microphone

---

## 🤔 **Wait, How Does Audio Recording Actually Work?**

Great question! Let me explain this in a way that makes sense without getting too technical.

### **The Magic Behind the Scenes**

Think of recording audio like taking thousands of tiny "snapshots" of sound every second. When you speak, your voice creates sound waves that travel through the air (just like ripples in a pond). Your microphone is like a super-sensitive ear that can "hear" these waves and turn them into electrical signals.

**Here's what's happening:**
Your computer can't work with continuous sound waves - it needs to break them down into tiny, manageable pieces. So it takes "samples" of the sound at regular intervals. If you're recording at 16,000 samples per second (which is what we're doing), that means your computer is taking 16,000 tiny measurements of the sound every single second!

**Why this matters:**
Imagine trying to draw a smooth curve by connecting dots. If you only have a few dots, the curve looks jagged and rough. But if you have lots of dots close together, the curve looks smooth and natural. The same thing happens with audio - more samples per second means better quality sound.

### **Real-World Example**
Think about old vinyl records vs. modern digital music. Vinyl records are like having a continuous groove that follows the sound wave perfectly (analog). Digital audio is like having thousands of tiny measurements (samples) that recreate the sound wave. When you play it back, your brain fills in the gaps between the samples, so it sounds smooth and natural.

**The key insight:** Your computer is essentially "drawing" the sound wave using thousands of tiny dots (samples), and when you play it back, it connects the dots to recreate your voice!

---

## 🔗 **What's Next**

After mastering this module, you'll be ready for:
- **Module 2**: Detecting when someone is speaking (Voice Activity Detection)
- **Module 3**: Converting speech to text (Speech-to-Text)
- **Module 4**: Getting AI responses (ChatGPT Integration)

---

## 💡 **Pro Tips**

1. **Start simple**: Get basic recording working before adding features
2. **Test incrementally**: Verify each step works before moving on
3. **Use good audio**: Clear microphone input = better results later
4. **Monitor resources**: Audio processing can use significant memory
5. **Document experiments**: Keep notes on what works and what doesn't

---

## 🎓 **Learning Check**

**Before moving to Module 2, you should be able to:**
- ✅ Record audio from your microphone
- ✅ Play back recorded audio through speakers
- ✅ Understand what sample rate and bit depth mean
- ✅ Explain the basic audio recording/playback pipeline
- ✅ Troubleshoot common audio issues

---

**🎉 Congratulations! You've taken your first step toward building an AI voice assistant. The audio skills you learn here will be the foundation for everything that follows!**
