import openai
import time
import os

openai.api_key = "YOUR_API_KEY"

def read_last_line(filename):
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
            return lines[-1].strip() if lines else ""
    except FileNotFoundError:
        return ""

def write_response(response):
    with open("response.txt", "a") as f:
        f.write(response + "\n")

def chat_with_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if available
        messages=[
            {"role": "system", "content": "You are Ben, a helpful and polite AI assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content'].strip()

# Main loop to monitor transcription file
print("🤖 ChatGPT module running...")

last_prompt = ""
while True:
    time.sleep(1.5)  # check every 1.5 seconds
    prompt = read_last_line("transcription.txt")

    if prompt and prompt != last_prompt:
        print("💬 New message detected:", prompt)
        reply = chat_with_gpt(prompt)
        print("🧠 Ben:", reply)
        write_response(reply)
        last_prompt = prompt
