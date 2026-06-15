import os
import time

# To use Gemini, you will need to install the SDK: `pip install google-generativeai`
try:
    import google.generativeai as genai
except ImportError:
    genai = None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPT_FILE = os.path.join(BASE_DIR, "prompt.txt")
RESPONSE_FILE = os.path.join(BASE_DIR, "response.txt")

# ==========================================
# PASTE YOUR GEMINI API KEY HERE
# ==========================================
GEMINI_API_KEY = "YOUR_API_KEY_HERE"

if genai and GEMINI_API_KEY != "YOUR_API_KEY_HERE":
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-pro-latest') # or your preferred model
else:
    model = None

def main_loop():
    print("Etherdesk Listener Started. Waiting for prompts...")
    # This loop monitors prompt.txt for new commands sent from the phone.
    
    while True:
        if os.path.exists(PROMPT_FILE):
            with open(PROMPT_FILE, "r", encoding="utf-8") as f:
                prompt_content = f.read().strip()
                
            if prompt_content:
                print(f"New prompt received from phone: {prompt_content}")
                
                if model:
                    try:
                        print("Sending to Gemini API...")
                        response = model.generate_content(prompt_content)
                        ai_response = response.text
                    except Exception as e:
                        ai_response = f"Failed to get response from Gemini: {e}"
                else:
                    # Mock response if API key is not set
                    ai_response = f"Received your command: '{prompt_content}'.\n\n[Setup your Gemini API key in listener.py and install google-generativeai to get real AI replies!]"
                
                with open(RESPONSE_FILE, "w", encoding="utf-8") as f:
                    f.write(ai_response)
                
                # Clear the prompt file so we don't process it again
                with open(PROMPT_FILE, "w", encoding="utf-8") as f:
                    f.write("")
                    
        time.sleep(2)

if __name__ == "__main__":
    main_loop()