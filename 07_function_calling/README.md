# Module 7: Function Calling & AI Tools

> **What you'll build:** Ask "Jarvis, what's the weather?" and it actually checks. Ask it to set a timer and it does. The AI decides which tools to use and when.
>
> **What's new:** `tools.py` with real functions; the two-step API call pattern where ChatGPT requests a function, we run it, and then re-ask ChatGPT with the result.
>
> **What carries over:** Everything from Module 6. This module adds `tools.py` and updates how `get_chatgpt_response()` is called.

Welcome to Module 7! Now that Jarvis can have conversations and respond to wake words, let's give it **superpowers** by connecting it to real-world functions. This is where your voice assistant becomes truly useful - it can check the weather, set timers, tell you the time, and even run system commands!

---

##  **What You'll Learn**

- **Function Calling**: Giving AI access to real-world tools and capabilities
- **API Integration**: Connecting to external services like weather APIs
- **System Commands**: Safely executing commands on your Raspberry Pi
- **AI Tool Selection**: How AI chooses which tools to use for your requests
- **Practical Applications**: Making your assistant actually useful for daily tasks

---

##  **Understanding the Code**

### **Key Concepts**

#### 1. **Function Calling System**
```python
# Define available tools/functions
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a location",
            "parameters": {...}
        }
    }
]
```
- **What it does**: Tells the AI what tools are available and how to use them
- **How it works**: AI sees these descriptions and chooses the right tool for your request
- **Why it's amazing**: AI can now do things beyond just talking
- **Safety**: Only safe, predefined functions are available

#### 2. **Tool Descriptions**
```python
"description": "Get the current weather for a location",
"parameters": {
    "type": "object",
    "properties": {
        "latitude": {"type": "number", "description": "The latitude coordinate"},
        "longitude": {"type": "number", "description": "The longitude coordinate"}
    },
    "required": ["latitude", "longitude"]
}
```
- **Clear descriptions**: AI understands what each tool does
- **Parameter definitions**: AI knows what information each tool needs
- **Required vs. optional**: AI knows what's necessary to make the tool work
- **Type safety**: AI provides the right kind of data

#### 3. **Function Execution**
```python
# Execute the appropriate function
if function_name == "get_weather":
    result = get_weather(**function_args)
elif function_name == "get_time":
    result = get_time()
elif function_name == "set_timer":
    result = set_timer(**function_args)
```
- **Smart routing**: System automatically calls the right function
- **Parameter passing**: Arguments from AI are safely passed to functions
- **Result handling**: Function results are sent back to AI for response
- **Error handling**: Graceful failure if something goes wrong

---

##  **File Structure**

```
07_function_calling/
├── main.py              # Main function calling application
├── audio.py             # Audio recording functions
├── chat.py              # ChatGPT integration with function calling
├── speak.py             # Text-to-speech functions
├── tools.py             # Available functions and tools
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

---

## The Two-Step API Pattern

This is the most important concept in this module. When tools are involved, one request to ChatGPT is not enough:

```
You ask: "Jarvis, what's the weather?"
         │
         ▼
  ChatGPT (with tools) ──► Does it need a tool?
         │                        │
         │                     YES: returns tool_calls (not text yet)
         │                        │
         ▼                        ▼
  No tool needed          We run get_weather()
  → Speak response              │
                                ▼
                        Add result to messages
                                │
                                ▼
                        ChatGPT again (now has real data)
                                │
                                ▼
                        Returns natural language response
                                │
                                ▼
                        Jarvis speaks it
```

The first API call tells us *what* to do. The second API call produces the *response* using the real data.

## How It Works

### **Step 1: AI Sees Available Tools**
```python
# 1. AI receives your request and sees available tools
response = get_chatgpt_response(messages, tools)

# 2. AI decides if it needs to use any tools
if response.tool_calls:
    print(" Executing function calls...")
```

**What happens:**
- You ask Jarvis something like "What's the weather like?"
- AI sees the available tools and recognizes it needs weather data
- AI decides to call the `get_weather` function
- System prepares to execute the function

### **Step 2: Function Execution**
```python
# 1. For each tool call the AI wants to make
for tool_call in response.tool_calls:
    function_name = tool_call.function.name
    function_args = eval(tool_call.function.arguments)
    
    # 2. Execute the appropriate function
    if function_name == "get_weather":
        result = get_weather(**function_args)
    elif function_name == "set_timer":
        result = set_timer(**function_args)
```

**What happens:**
- AI provides the function name and arguments
- System safely executes the function with those arguments
- Function returns real data (weather info, timer confirmation, etc.)
- Results are collected for the AI to use

### **Step 3: AI Incorporates Results**
```python
# 1. Add function results to conversation
messages.append({
    "role": "tool",
    "tool_call_id": tool_call.id,
    "content": str(result)
})

# 2. Get AI response incorporating the results
response = get_chatgpt_response(messages, tools)
```

**What happens:**
- Function results are added to the conversation
- AI gets a new response that includes the real data
- AI can now give you accurate, helpful information
- Response is spoken back to you

---

##  **Running the Code**

### **1. Navigate to the folder**
```bash
cd 07_function_calling
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

### **5. Test the superpowers!**
- **" Listening for trigger word 'Jarvis'..."** - System is ready
- **"Jarvis, what's the weather like?"** - AI will call weather function
- **" Executing function calls..."** - Functions are running
- **" Jarvis: [response with real data]"** - AI speaks results
- **" Listening..."** - Ready for next command

---

##  **Experiments to Try**

### **Basic Function Testing**
1. **Weather**: "Jarvis, what's the weather like in New York?"
2. **Time**: "Jarvis, what time is it right now?"
3. **Timers**: "Jarvis, set a timer for 5 minutes"

### **Advanced Function Testing**
1. **Multiple functions**: "Jarvis, what's the weather and what time is it?"
2. **Complex requests**: "Jarvis, set a timer for 10 minutes and tell me the weather"
3. **Follow-up questions**: Ask about timer status or weather details

### **Edge Case Testing**
1. **Invalid inputs**: "Jarvis, what's the weather like on Mars?"
2. **Missing information**: "Jarvis, set a timer" (without specifying time)
3. **Function combinations**: See how AI handles multiple tool calls

---

##  **Understanding the Output**

### **What You'll See**
```
 Listening for trigger word 'Jarvis'...
 You said: Jarvis, what's the weather like?
 Trigger word detected! Processing request...
 Executing function calls...
 Calling get_weather with args: {'latitude': 40.7128, 'longitude': -74.006}
 Weather retrieved: Partly cloudy, 22.5°C
 Jarvis: The current weather is partly cloudy with a temperature of 22.5°C...
 Speaking complete.
 Listening for trigger word 'Jarvis'...
```

### **What Each Line Means**
- ****: System listening for wake word
- ****: Your request transcribed
- ****: Wake word detected
- ****: Functions being executed
- ****: Specific function being called
- ****: Function result
- ****: AI response incorporating results
- ****: TTS playback
- ****: Back to listening

---

##  **Common Issues & Solutions**

### **"Function not working"**
- **Check internet**: Weather API needs internet connection
- **Verify coordinates**: Make sure latitude/longitude are valid numbers
- **Check API limits**: Some APIs have rate limits

### **"AI not using functions"**
- **Be specific**: "What's the weather?" vs "Tell me about the weather"
- **Check tool descriptions**: Make sure AI understands what tools do
- **Verify tool definitions**: Check that tools are properly defined

### **"Function errors"**
- **Check parameters**: Make sure required parameters are provided
- **Verify function code**: Check that functions handle errors gracefully
- **Test functions directly**: Try calling functions manually to debug

---

##  **Wait, How Does Function Calling Actually Work?**

Great question! Let me explain this in a way that makes sense without getting too technical.

### **The Magic Behind the Scenes**

Think of function calling like giving your really smart friend (Jarvis) access to a toolbox full of specialized tools. Before, Jarvis could only talk about things it learned from books and conversations. Now, Jarvis can actually use tools to get real-time information and perform actions in the real world.

**Here's what's happening:**
When you ask Jarvis "What's the weather like?", it's like asking a friend who's sitting inside a house. Before function calling, Jarvis might say "I can't see outside, but I can tell you about weather in general." But now, Jarvis can say "Let me check the weather for you!" and actually go look outside (or in this case, call a weather API).

**Why this is so powerful:**
Instead of Jarvis just being a knowledgeable conversationalist, it becomes a helpful assistant that can actually do things for you. It's like the difference between talking to someone who knows a lot about cooking versus having someone who can actually cook dinner for you!

### **Real-World Example**
Think about asking a smart home assistant "Turn on the lights." Without function calling, the AI might say "I understand you want the lights on, but I can't actually control your house." With function calling, the AI can say "I'll turn on the lights for you!" and actually send the command to your smart home system.

**The key insight:** Function calling bridges the gap between AI intelligence and real-world action. The AI handles understanding what you want, and the functions handle actually doing it. It's like having a brilliant strategist who can also execute the plan!

---

## Stretch Challenges

1. **Add a new tool** — write a `get_joke()` function in `tools.py` that returns a joke from a free API (or just hardcodes a few). Register it in the `tools` list in `main.py`. Ask Jarvis to tell you a joke.
2. **Add a search tool** — create a `search_web(query)` function. Even a simple one that opens a browser with `webbrowser.open(f"https://google.com/search?q={query}")` shows the concept.
3. **Test the AI's judgment** — ask "Jarvis, what time is it and what's the weather?" Does it call both functions? Look at the `response.tool_calls` list to see.
4. **Handle a bad tool call** — what happens if the weather API is down? Add a `try/except` in `get_weather()` and see how Jarvis handles it gracefully.

## What's Next

This is the final lesson module. The `raspberry_pi_production/` folder shows a production-ready version of the same system with hardware indicators, system monitoring, and auto-start on boot.

---

##  **Pro Tips**

1. **Be specific in requests**: Clear requests help AI choose the right tools
2. **Test function combinations**: See how AI handles multiple tool calls
3. **Monitor API usage**: Function calls use more tokens than regular conversations
4. **Add new functions**: Create custom tools for your specific needs
5. **Error handling**: Make sure functions handle edge cases gracefully

---

##  **Learning Check**

**Before moving to Module 8, you should be able to:**
-  Explain what function calling is and why it's powerful
-  Understand how AI chooses which tools to use
-  Successfully use Jarvis with function calling capabilities
-  Explain the difference between AI responses and function results
-  Troubleshoot common function calling issues
-  Understand how to add new functions to the system

---

** Phenomenal! You've now mastered function calling. Your voice assistant isn't just smart - it's capable! Jarvis can now check the weather, set timers, tell you the time, and perform real actions. This is a truly intelligent, useful AI assistant!**
