import os
import json
import pandas as pd
import requests
from dotenv import load_dotenv
from pinecone import Pinecone
from groq import Groq

# Load environment variables
load_dotenv()

# Initialize Clients
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
index = pc.Index("ayurveda-db")
HF_TOKEN = os.environ.get("HF_TOKEN")

def get_embedding(text):
    """Sends text to Hugging Face Cloud with the verified 2026 Router URL."""
    # The EXACT URL that just worked in your test
    URL = "https://router.huggingface.co/hf-inference/models/sentence-transformers/all-MiniLM-L6-v2/pipeline/feature-extraction"
    
    headers = {
        "Authorization": f"Bearer {os.getenv('HF_TOKEN')}",
        "Content-Type": "application/json"
    }
    
    payload = {"inputs": [text]}
    response = requests.post(URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        # The router returns a list of lists [[...]], so we take the first one [0]
        return response.json()[0]
    else:
        raise ValueError(f"Hugging Face Error: {response.status_code} - {response.text}")
    
    return response.json()

def search_knowledge_base(query):
    """Searches Pinecone cloud vector database."""
    # 1. Turn text into a vector
    query_vector = get_embedding(query)
    
    # 2. Query Pinecone
    results = index.query(
        vector=query_vector,
        top_k=5,
        include_metadata=True
    )
    
    # 3. Extract text from metadata
    context_chunks = [match['metadata']['text'] for match in results['matches']]
    return "\n".join(context_chunks)

def generate_rag_plan(age, weight, goal, dosha):
    """Generates the full 7-day and 30-day plan using Pinecone context."""
    
    # Search for both specific foods AND general principles from the cloud
    search_query = f"How to balance {dosha} for {goal} and what foods to eat?"
    context = search_knowledge_base(search_query)

    system_prompt = "You are a Master Ayurvedic Physician. You must respond strictly in JSON format."
    
    user_prompt = f"""
    User: {age}yrs, {weight}kg, {dosha}, Goal: {goal}.
    Knowledge from Ancient Texts: {context}

    Task:
    1. Create a 7-day unique meal rotation based on the principles.
    2. Suggest how to adapt this into a 30-day strategy.
    
    JSON Structure (camelCase):
    {{
        "userProfile": "string",
        "ayurvedicInsight": {{
            "coreFocus": "string",
            "foodsToAvoid": "string",
            "dinacharyaRoutine": "string"
        }},
        "dailyPlan": {{ 
            "breakfast": {{"name": "string", "calories": 300, "time": "8:00 AM"}},
            "lunch": {{"name": "string", "calories": 600, "time": "1:00 PM"}},
            "dinner": {{"name": "string", "calories": 450, "time": "7:00 PM"}},
            "snacks": ["option1", "option2"]
        }},
        "weeklyRotation": [
            {{"day": "Day 1", "breakfast": "...", "lunch": "...", "dinner": "..."}}
        ],
        "thirtyDayStrategy": "Detailed explanation of swaps.",
        "macronutrients": {{"protein": "20%", "carbs": "50%", "fats": "30%"}},
        "hydrationGoal": "e.g. 2.5L",
        "recommendedFoods": ["food1", "food2"]
    }}
    """

    response = client.chat.completions.create(
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
        model="llama-3.3-70b-versatile",
        response_format={ "type": "json_object" }
    )
    return json.loads(response.choices[0].message.content)

def generate_recipe_from_ingredients(ingredients, meal_type, dosha, goal):
    """Standard recipe generation remains the same."""
    prompt = f"""
    You are an Ayurvedic Master Chef. 
    Ingredients: {ingredients}.
    Request: {meal_type} optimized for {dosha} dosha. Goal: {goal}.

    Return STRICTLY in JSON:
    {{
        "recipeName": "Creative Name",
        "ayurvedicBenefit": "Reasoning",
        "prepTime": "15 mins",
        "ingredientsList": ["item 1"],
        "stepByStep": ["Step 1"]
    }}
    """
    
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)