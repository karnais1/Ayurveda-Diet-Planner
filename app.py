import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
app = Flask(__name__)
CORS(app) # This allows all origins to talk to your API
from rag_engine import generate_rag_plan, generate_recipe_from_ingredients

app = Flask(__name__, static_folder='dist')
CORS(app)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

@app.route("/api/personal", methods=["POST"])
def personal_plan():
    try:
        data = request.get_json()
        plan = generate_rag_plan(data['age'], data['weight'], data['goal'], data['dosha'])
        return jsonify({"status": "success", "data": plan})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/api/recipe-from-ingredients", methods=["POST"])
def recipe_from_ingredients():
    try:
        data = request.get_json()
        ingredients = data.get("ingredients", "")
        meal_type = data.get("mealType", "Light")
        dosha = data.get("dosha", "Vata")
        goal = data.get("goal", "Balance")

        recipe = generate_recipe_from_ingredients(ingredients, meal_type, dosha, goal)
        return jsonify({"status": "success", "data": recipe}), 200

    except Exception as e:
        print(f"RECIPE ERROR: {str(e)}") # This will print the exact issue to your terminal
        return jsonify({"status": "error", "message": str(e)}), 400
@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        message = data.get("message")
        dosha = data.get("dosha", "Vata")
        
        # We define the client call right here for a quick text response (no JSON formatting needed)
        from rag_engine import client 
        
        system_prompt = f"You are a helpful Ayurvedic Chef. The user is a {dosha} dosha. Keep answers under 3 sentences."
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            model="llama-3.1-8b-instant", # Using the fast model for chat!
        )
        
        return jsonify({"status": "success", "reply": response.choices[0].message.content}), 200
    except Exception as e:
        print(f"CHAT ERROR: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 400

import os

if __name__ == "__main__":
    # Render provides a PORT environment variable. We must use it.
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)