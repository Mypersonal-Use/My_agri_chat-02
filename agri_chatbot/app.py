from flask import Flask, request, jsonify, render_template
from agri_chatbot import AgriChatbot
import os
from dotenv import load_dotenv

app = Flask(__name__)
chatbot = AgriChatbot()
load_dotenv()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('message', '')
    api_key = data.get('api_key')  # Only use the API key provided by the user
    response = chatbot.get_response(user_input, gemini_api_key=api_key)
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)