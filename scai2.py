#!/usr/bin/env python3
import requests

##############################################################################
# 1) Configuration
##############################################################################

GEMINI_API_KEY = "AIzaSyAbBqogZcWeiF2txiAfmZ9NL7d4NapbKfo"
if not GEMINI_API_KEY:
    raise ValueError("Gemini API key not found. Please provide a valid key.")

GEMINI_ENDPOINT = (
    "https://generativelanguage.googleapis.com/v1beta/"
    "models/gemini-pro:generateContent?key=" + GEMINI_API_KEY
)

# Initialize conversation history
conversation_history = ""

##############################################################################
# 2) Function to Call Gemini
##############################################################################
def fetch_gemini_response(history, user_input):
    """
    Sends the entire conversation history and the current input to Gemini
    and requests a concise response.
    """
    # Combine history with user input for full context
    full_prompt = f"{history}\nUser: {user_input}\nGemini, respond concisely in as few words as possible."

    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {
                "parts": [
                    {"text": full_prompt}
                ]
            }
        ]
    }

    try:
        response = requests.post(GEMINI_ENDPOINT, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            if ("candidates" in result 
                and len(result["candidates"]) > 0
                and "content" in result["candidates"][0]
                and "parts" in result["candidates"][0]["content"]
                and len(result["candidates"][0]["content"]["parts"]) > 0
                and "text" in result["candidates"][0]["content"]["parts"][0]):
                return result["candidates"][0]["content"]["parts"][0]["text"].strip()
            else:
                return "[ERROR] Unexpected Gemini response structure. Check logs."
        else:
            return f"[ERROR] Gemini API returned status {response.status_code}: {response.text}"
    except Exception as e:
        return f"[ERROR] Exception while calling Gemini: {e}"

##############################################################################
# 3) Interactive Chat Loop
##############################################################################
def chat_loop():
    """
    Waits for user input, processes data only after pressing Enter,
    sends it to Gemini, and waits for the next command.
    """
    global conversation_history
    print("Type 'exit' or 'quit' to end.\n")
    while True:
        # Wait for user input (only processes when Enter is pressed)
        user_input = input("Enter your command/data: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting...")
            break

        # Fetch response from Gemini using the current user input
        gemini_reply = fetch_gemini_response(conversation_history, user_input)
        
        # Update the conversation history
        conversation_history += f"\nUser: {user_input}\nGemini: {gemini_reply}"

        # Print the reply
        print(f"\nGemini (concise): {gemini_reply}\n")

##############################################################################
# 4) Main Entry Point
##############################################################################
def main():
    print("=========================================================")
    print("   Gemini Chat - Processes Data After Enter Is Pressed   ")
    print("=========================================================\n")
    chat_loop()

if __name__ == "__main__":
    main()
