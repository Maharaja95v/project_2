# from flask import Flask, render_template
import google.generativeai as genai
from flask import Flask, request, jsonify,render_template
from flask_cors import CORS
import os
from dotenv import load_dotenv



load_dotenv()

app = Flask(__name__)
CORS(app)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

anthony_prompt = """You are now embodying Anthony Bridgerton, a character from the series Bridgerton. Your demeanor is charming, romantic, and sophisticated, with a sharp wit and a penchant for grandiose, heartfelt declarations. Your mission is to flirt with Gopika, who is celebrating her birthday today, and make her feel like the most cherished and adored person in the world. Every response must reflect Anthony's mannerisms, speech patterns, and values, focusing on elegance, subtlety, and passion. Aim to win her over with your words and actions, ensuring that each reply elevates her spirits and leaves her utterly captivated."""
# Initialize chat history with Gojo's flirty opening
chat = model.start_chat(
    history=[
        # {"role": "system", "parts": anthony_prompt},
        {"role": "user", "parts": anthony_prompt},
        {
            "role": "model",
            "parts": "Ah, hello there, Gopika. It is a pleasure to meet a lady as radiant as yourself, especially on such a momentous occasion as your birthday. Tell me, how may I make this day even more extraordinary for you?",
        },
    ]
)

def generate_response(user_message):
    global chat  # Access the global chat variable

    try:
      response = chat.send_message(user_message)
      return response.text
    except Exception as e:
      print(f"Error in processing the response : {e}")
      return "My sincerest apologies, dear Gopika, but it appears I am momentarily incapable of forming a response befitting your elegance. Allow me a moment to collect myself before we continue our conversation."

@app.route("/chat", methods=["POST"])
def chat_endpoint():
    data = request.get_json()
    if "message" not in data:
        return jsonify({"error": "Message is required"}), 400

    user_message = data["message"]
    bot_response = generate_response(user_message)

    return jsonify({"response": bot_response})

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, port=5001)