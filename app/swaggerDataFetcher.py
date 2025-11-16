import requests
import json
import os

API_URL = "https://november7-730026606190.europe-west1.run.app/messages"

def fetch_messages():
    """
    Fetch all messages from the public API and save to messages.json
    """
    print("Fetching messages from API...")
    
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        
        messages = response.json()
        print(f"Successfully fetched {len(messages)} messages")
        
        # Save to local file
        os.makedirs("app", exist_ok=True)
        with open("app/messages.json", "w", encoding="utf-8") as f:
            json.dump(messages, f, indent=2, ensure_ascii=False)
        
        print("Messages saved to app/messages.json")
        return messages
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching messages: {e}")
        return None

if __name__ == "__main__":
    fetch_messages()