import requests
import os
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

# This is the EXACT URL required for the 2026 Router for this model
URL = "https://router.huggingface.co/hf-inference/models/sentence-transformers/all-MiniLM-L6-v2/pipeline/feature-extraction"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

# The payload is just a simple 'inputs' list or string
payload = {"inputs": ["Ayurveda diet for Vata dosha"]}

print("Testing 2026 Dedicated Feature-Extraction Router...")
try:
    response = requests.post(URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        # Success! It returns a list of lists (vectors)
        vector = response.json()[0]
        print(f"✅ SUCCESS! Vector Length: {len(vector)}")
    elif response.status_code == 401:
        print("❌ 401 Error. Double-check your .env file for extra spaces or quotes!")
        print(f"Your Token starts with: {str(HF_TOKEN)[:8]}...")
    else:
        print(f"❌ FAILED. Status: {response.status_code}")
        print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")