import os
import asyncio
import sys
import json
import requests
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv('/home/aqsagulllinux/Todo-app/phase-2/backend/.env')

def test_openrouter_directly():
    """Test the OpenRouter API directly without the agents SDK."""
    print("Testing OpenRouter API directly...")
    
    # Get the API key and configuration from environment
    api_key = os.getenv('OPENROUTER_API_KEY')
    base_url = os.getenv('OPENROUTER_BASE_URL', 'https://openrouter.ai/api/v1')
    model = os.getenv('OPENROUTER_MODEL', 'mistralai/devstral-2512:free')
    
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY not found in environment variables.")
        return False
    
    print(f"Using model: {model}")
    
    # Make a simple request to the OpenRouter API
    url = f"{base_url}/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Reduced the max_tokens to meet the credit limit constraints
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": "Hello, can you confirm that you are responding through the OpenRouter API?"
            }
        ],
        "max_tokens": 500  # Limit the token usage to avoid credit issues
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if 'choices' in data and len(data['choices']) > 0:
                bot_response = data['choices'][0]['message']['content']
                print(f"SUCCESS: OpenRouter responded to the message!")
                print(f"Bot's response: {bot_response}")
                return True
            else:
                print("WARNING: API returned 200 but no choices in response")
                print(f"Full response: {data}")
                return False
        else:
            print(f"FAILURE: API returned status code {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"ERROR: Failed to connect to OpenRouter API - {str(e)}")
        return False

if __name__ == "__main__":
    test_openrouter_directly()