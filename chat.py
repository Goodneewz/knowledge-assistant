import os
import requests
from dotenv import load_dotenv
import time


load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-3.5-flash-lite"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"

def ask(messages, system="You are a helpful assistant.", temperature=0.2):
    body = {
        "system_instruction": {"parts": [{"text": system}]},
        "contents": messages,
        "generationConfig": {"temperature": temperature},
    }
    r = requests.post(URL, json=body, headers={"x-goog-api-key": API_KEY}, timeout=60)
    r.raise_for_status()
    data = r.json()
    return data["candidates"][0]["content"]["parts"][0]["text"], data["usageMetadata"]

def ask_with_retry(messages, tries=3):
    for attempt in range(tries):
        try:
            return ask(messages)
        except requests.exceptions.HTTPError as e:
            code = e.response.status_code
            if code not in (429, 500, 503) or attempt == tries - 1:
                raise
            print(f"Server busy ({code}). Retrying...")
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            if attempt == tries - 1:
                raise
            print("Network slow or dropped. Retrying...")
        time.sleep(2 ** attempt * 3)


messages = [{"role": "user", "parts": [{"text": "Hi"}]}]
text, usage = ask_with_retry(messages)
# print(text)
print(usage)

messages.append({"role": "model", "parts": [{"text": text}]})
messages.append({"role": "user", "parts": [{"text": "What is my name?"}]})
print(ask_with_retry(messages)[0])

messages = []
print("Type 'quit' to exit, 'reset' to forget.")

while True:
    user_text = input("You: ")
    if user_text == "quit":
        break
    if user_text == "reset":
        messages = []
        print("Memory cleared.")
        continue
    messages.append({"role": "user", "parts": [{"text": user_text}]})
    # TODO 1: if user_text is "quit", stop the loop
    # TODO 2: if user_text is "reset", empty messages and continue
    # TODO 3: append the user's message to messages

    try:
        text, usage = ask_with_retry(messages)
    except Exception as e:
        print("Something went wrong:", e)
        if hasattr(e, "response") and e.response is not None:
            print(e.response.text)
        messages.pop()   # TODO 4: undo the user message
        continue
    # TODO 5: print the reply, then print usage["totalTokenCount"]
    print(text)
    print(usage["totalTokenCount"])
    # TODO 6: append {"role": "model", "parts": [{"text": text}]} to messages