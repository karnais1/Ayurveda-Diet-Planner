🌿 Ayurveda AI: Full-Stack RAG-Powered Dietary Blueprint

🚀 View Live Demo (Note: As this is hosted on a free Render tier, the backend may take 30-50 seconds to "wake up" on the first request.)

📖 Overview

Ayurveda AI is a sophisticated, full-stack application designed to bridge ancient Ayurvedic wisdom with modern AI technology. By leveraging Retrieval-Augmented Generation (RAG), the platform provides users with hyper-personalized nutrition plans, 30-day meal strategies, and a real-time pantry-aware recipe generator.

The system doesn't just "hallucinate" advice; it queries a curated knowledge base of Ayurvedic principles and nutritional data to ensure every recommendation balances the user's specific Dosha (Vata, Pitta, or Kapha).

✨ Key Features

👤 Personalized Dosha Blueprint

Users provide their age, weight, and health goals (Fat Loss, Muscle Gain, Balance). The AI analyzes these against their dominant Dosha to create:

Daily Schedules: Timed meals (Breakfast, Lunch, Dinner) with calorie counts.

7-Day Base Rotation: A variety of meals to prevent dietary fatigue.

30-Day Sustenance Strategy: Long-term advice for maintaining metabolic health.

Hydration Goals: Precise water intake recommendations tailored to body weight.

🍳 Smart Pantry Chef

Input whatever ingredients are currently in your kitchen (e.g., "Rice, Spinach, Ghee"). The AI generates a unique recipe that:

Uses only your available ingredients.

Tailors the cooking style (Light vs. Heavy) to your preference.

Ensures the final dish balances your specific Dosha.

💬 Ayurvedic Sous-Chef (Chatbot)

A persistent, floating AI assistant that remembers your context. Ask it about ingredient substitutes, the benefits of specific spices, or how to manage your energy levels throughout the day.

🧠 Hybrid RAG Engine

The "brain" of the app uses ChromaDB as a Vector Database to search through:

Structured Data (diet_data.csv): For precise calorie and macronutrient accuracy.

Unstructured Data (ayurveda_guide.txt): For deep philosophical and medicinal Ayurvedic context.

🛠️ Technical Stack

Layer

Technology

Frontend

React 18, TypeScript, Tailwind CSS, Lucide Icons, Vite

Backend

Python 3.x, Flask, Gunicorn

AI / LLM

Groq Cloud (Llama 3.3 70B & 3.1 8B Models)

Database

ChromaDB (Vector Store for RAG)

Deployment

Render (Unified Python/React Host)

🚀 Installation & Local Setup

1. Prerequisites

Node.js (v18+)

Python (v3.9+)

A Groq Cloud API Key

2. Backend Configuration

Navigate to the root directory:

# Install dependencies
pip install -r requirements.txt

# Create environment file
touch .env


Add your key to the .env file:

GROQ_API_KEY=gsk_your_actual_key_here


3. Frontend Configuration

Navigate to your frontend source folder:

npm install
npm run build  # This generates the /dist folder for the Flask server


4. Run the App

Return to the root directory and start the server:

python app.py


Visit http://localhost:5000 in your browser.

📂 Project Structure

AYURVEDA/
├── app.py              # Flask Server & API Endpoints
├── rag_engine.py       # RAG Logic & ChromaDB Integration
├── diet_data.csv       # Nutritional Dataset
├── ayurveda_guide.txt  # Ayurvedic Knowledge Base
├── requirements.txt    # Python Dependencies
├── .env                # API Keys (Excluded from Git)
├── .gitignore          # File exclusions
├── README.md           # Project Documentation
└── dist/               # Compiled React Frontend (Production)


🛡️ Security & Environment

This project implements strict security protocols:

Secret Scanning: API keys are managed via .env and excluded from version control via .gitignore.

CORS Management: Flask-CORS is configured to handle cross-origin requests safely.

Production Server: Uses Gunicorn for robust deployment on Render.


📜 License

This project is for educational purposes as part of a Full-Stack AI development portfolio.
