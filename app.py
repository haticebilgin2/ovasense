import openai
from flask import Flask, request, jsonify, render_template
import os
from dotenv import load_dotenv
import logging

# Initialize Flask app
app = Flask(__name__)

# Enable detailed logging
logging.basicConfig(level=logging.DEBUG)

# Load environment variables from .env file
load_dotenv()

# Fetch OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    try:
        # Check if the request has JSON data
        if request.is_json:
            user_message = request.json.get('message')
            app.logger.debug(f"Received message: {user_message}")
        else:
            app.logger.error("Request is not JSON")
            return jsonify({"error": "Request must be JSON"}), 400

        if not user_message:
            app.logger.error("No message provided")
            return jsonify({"error": "No message provided"}), 400

        # Using 'gpt-3.5-turbo' for conversation-based API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Or use "gpt-4" if available
            messages=[
                {"role": "system", "content": """Hi there! Welcome to OvaSense 🌸, your trusted companion for managing PCOS and Endometriosis with care and confidence. Whether you’re here for answers, advice, or tools to track your progress, I’m here to support you every step of the way.

                Here’s what I can help you with today:
                
                Symptom Guidance: Get answers to FAQs about common symptoms and learn when to seek medical advice.
                Dietary Tips: Receive personalized nutrition advice tailored to your preferences and health goals.
                Exercise Routines: Explore low-impact exercises designed to alleviate pain and improve hormone balance.
                Tracking Features: Log your symptoms and habits to better understand and manage your health.
                What would you like to explore first?"""},
                {"role": "user", "content": user_message}
            ]
        )

        bot_message = response['choices'][0]['message']['content']
        app.logger.debug(f"Bot response: {bot_message}")
        return jsonify({'response': bot_message})

    except Exception as e:
        app.logger.error(f"Error during OpenAI API call: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
