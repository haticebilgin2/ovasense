import openai
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# OpenAI API key (replace with your own key)
openai.api_key = "sk-"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_message = request.json.get('message')

    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    try:
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

        # Extracting the response from the OpenAI API response
        bot_message = response['choices'][0]['message']['content']
        return jsonify({'response': bot_message})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)