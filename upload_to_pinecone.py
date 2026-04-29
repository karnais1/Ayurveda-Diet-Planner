import os
import pandas as pd
import requests
from pinecone import Pinecone
from dotenv import load_dotenv

# 1. Load your keys
load_dotenv()
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
HF_TOKEN = os.environ.get("HF_TOKEN")

# 2. Setup Pinecone & Hugging Face URL
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("ayurveda-db")
# This is the correct, updated URL:
# Use this exact URL:
# Use this exact URL structure
# Use this exact URL - it is the most reliable one for this model
HF_API_URL = "https://router.huggingface.co/hf-inference/models/sentence-transformers/all-MiniLM-L6-v2/pipeline/feature-extraction"

def get_embedding(text):
    """Sends text to Hugging Face Cloud."""
    # We must include the Bearer prefix and NO extra spaces
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    # We add a small timeout to handle network lag
    response = requests.post(HF_API_URL, headers=headers, json={"inputs": text}, timeout=20)
    
    if response.status_code != 200:
        # If this still fails, it will print the specific error from Hugging Face
        print(f"DEBUG: Status {response.status_code} - {response.text}")
        raise ValueError(f"Hugging Face Error")
    
    return response.json()
# 3. Load your CSV
CSV_FILE = "diet_data.csv" # Ensure this matches your filename!

if not os.path.exists(CSV_FILE):
    print(f"❌ Error: {CSV_FILE} not found in this folder!")
    exit()

df = pd.read_csv(CSV_FILE)
print(f"Reading {len(df)} rows from {CSV_FILE}...")

vectors_to_upload = []

# 4. Loop through data and convert to vectors
for i, row in df.iterrows():
    # This mashes all your columns (Age, Weight, Goal, Dosha, Food) into one sentence
    text_chunk = " ".join([f"{col}: {row[col]}" for col in df.columns])
    
    try:
        print(f"Processing row {i}...")
        vector = get_embedding(text_chunk)
        
        vectors_to_upload.append({
            "id": f"row_{i}",
            "values": vector,
            "metadata": {"text": text_chunk}
        })
    except Exception as e:
        print(f"⚠️ Skipping row {i} due to error: {e}")

# 5. Push to the Cloud
if vectors_to_upload:
    print(f"Pushing {len(vectors_to_upload)} items to Pinecone Cloud...")
    index.upsert(vectors=vectors_to_upload)
    print("✅ SUCCESS! Your Ayurveda data is now live in the cloud database.")
else:
    print("❌ No data was prepared for upload.")