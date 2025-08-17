# 🤖 Jarvis - Raspberry Pi Voice Assistant (Production)

A production-ready, fully-featured voice assistant optimized for Raspberry Pi with GPIO LED indicators, system monitoring, and comprehensive function calling capabilities.

## ✨ Features

### 🎤 Core Voice Assistant
- **Wake Word Detection**: Say "Jarvis" to activate
- **Speech-to-Text**: OpenAI Whisper API integration
- **Text-to-Speech**: Multiple TTS backends with fallbacks
- **Natural Language Processing**: GPT-4o-mini for intelligent responses

### 🔧 Function Calling & Tools
- **Weather Information**: Get current weather by coordinates
- **Timer Management**: Set, monitor, and cancel timers
- **System Monitoring**: CPU, memory, temperature, uptime
- **Time & Date**: Current time, date, and timezone
- **System Commands**: Safe execution of system commands

### 🎯 Raspberry Pi Optimizations
- **GPIO LED Indicators**: Visual feedback for different states
- **Audio Fallbacks**: Multiple audio backends for reliability
- **Performance Monitoring**: System health and resource usage
- **Graceful Shutdown**: Signal handling and resource cleanup
- **Temperature Monitoring**: CPU temperature tracking

### 💡 Hardware Features
- **Status LED (GPIO 22)**: System health indicator
- **Listening LED (GPIO 17)**: Audio input active
- **Processing LED (GPIO 18)**: AI processing active
- **Speaking LED (GPIO 27)**: Speech output active
- **Timer LED (GPIO 23)**: Timer running indicator
- **Weather LED (GPIO 24)**: Weather API active
- **Trigger Button (GPIO 25)**: Manual activation (optional)

## 🚀 Quick Start

### 1. Prerequisites
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install system dependencies
sudo apt install -y python3-pip python3-venv espeak festival
sudo apt install -y portaudio19-dev python3-pyaudio
sudo apt install -y libasound2-dev

# Enable SPI and I2C if using additional sensors
sudo raspi-config
```

### 2. Setup Environment
```bash
# Navigate to project directory
cd 08_raspberry_pi_production

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your OpenAI API key
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

### 3. Run the Assistant
```bash
# Activate virtual environment
source venv/bin/activate

# Run the assistant
python main.py
```

## 🔌 GPIO Pin Configuration

| Pin | Function | Description |
|-----|----------|-------------|
| 17  | Listening LED | Green - Audio input active |
| 18  | Processing LED | Yellow - AI processing |
| 22  | Status LED | Blue - System health |
| 23  | Timer LED | Orange - Timer running |
| 24  | Weather LED | Purple - Weather API active |
| 25  | Trigger Button | Manual activation (optional) |
| 27  | Speaking LED | Blue - Speech output |

## 🎯 Usage Examples

### Basic Commands
- **"Jarvis, what time is it?"** - Get current time
- **"Jarvis, set a timer for 5 minutes"** - Set a timer
- **"Jarvis, how's the system doing?"** - System status
- **"Jarvis, what's the weather like?"** - Weather information

### Advanced Features
- **Timer Management**: Set multiple timers with descriptions
- **System Monitoring**: Real-time performance metrics
- **Weather Data**: Detailed weather with multiple units
- **Function Chaining**: Complex multi-step requests

## ⚙️ Configuration

### Environment Variables
Create a `.env` file in the project directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### Audio Configuration
The system automatically detects and configures:
- **Primary**: Sounddevice (ALSA/PulseAudio)
- **Fallback**: Pygame audio backend
- **TTS Backends**: espeak, festival, gTTS, macOS say

### GPIO Configuration
Modify the GPIO pins in the respective modules:
- `audio.py` - Audio state LEDs
- `speak.py` - Speech state LED
- `tools.py` - System status LEDs
- `main.py` - Main application

## 🔧 Troubleshooting

### Common Issues

#### Audio Not Working
```bash
# Check audio devices
aplay -l
arecord -l

# Test microphone
arecord -d 5 test.wav
aplay test.wav

# Install additional audio packages
sudo apt install -y pulseaudio pulseaudio-utils
```

#### GPIO Errors
```bash
# Check GPIO permissions
sudo usermod -a -G gpio $USER

# Verify GPIO access
python3 -c "from gpiozero import LED; LED(17).on()"
```

#### Package Version Conflicts
```bash
# If you get version compatibility errors, try the flexible requirements:
pip install -r requirements_flexible.txt

# Or install packages individually without version constraints:
pip install sounddevice numpy scipy webrtcvad openai python-dotenv gpiozero psutil pygame gtts pydub requests

# Check your Python version:
python3 --version

# For newer Python versions (3.11+), some packages may need latest versions
```

#### Performance Issues
```bash
# Monitor system resources
htop
free -h
vcgencmd measure_temp

# Check for background processes
ps aux | grep python
```

### Debug Mode
Enable verbose logging by modifying the main loop in `main.py`:
```python
# Add debug prints
print(f"Debug: Audio length: {len(audio)}")
print(f"Debug: Transcription: {user_text}")
```

## 📊 Performance Monitoring

The assistant automatically monitors:
- **Response Times**: API call performance
- **System Health**: CPU, memory, temperature
- **Interaction Count**: Total conversations
- **Runtime Statistics**: Uptime and usage

## 🔒 Security Features

- **Command Whitelisting**: Only safe system commands allowed
- **API Key Protection**: Environment variable storage
- **Resource Limits**: Timeout protection for external calls
- **Error Handling**: Graceful failure recovery

## 🚀 Production Deployment

### Systemd Service
Create `/etc/systemd/system/jarvis.service`:
```ini
[Unit]
Description=Jarvis Voice Assistant
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/08_raspberry_pi_production
Environment=PATH=/home/pi/08_raspberry_pi_production/venv/bin
ExecStart=/home/pi/08_raspberry_pi_production/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Enable Service
```bash
sudo systemctl enable jarvis
sudo systemctl start jarvis
sudo systemctl status jarvis
```

### Log Management
```bash
# View logs
sudo journalctl -u jarvis -f

# Rotate logs
sudo logrotate /etc/logrotate.d/jarvis
```

## 🔄 Updates & Maintenance

### Regular Updates
```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Update Python dependencies
source venv/bin/activate
pip install --upgrade -r requirements.txt

# Restart service
sudo systemctl restart jarvis
```

### Backup Configuration
```bash
# Backup important files
cp .env .env.backup
cp -r venv venv.backup
```

## 🤝 Contributing

This production version is designed for:
- **Educational Use**: Learn voice assistant development
- **Home Automation**: Personal Raspberry Pi projects
- **Prototyping**: Test voice interfaces
- **Production Deployment**: Stable, reliable operation

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for Whisper and GPT APIs
- Raspberry Pi Foundation for hardware platform
- Open source community for audio and GPIO libraries

---

**Happy coding with your Raspberry Pi Voice Assistant! 🎉**
