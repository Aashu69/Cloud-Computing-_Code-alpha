# chatbot_app.py

from flask import Flask, request, jsonify, render_template_string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize Flask app
app = Flask(__name__)

# Predefined Q&A for retrieval-based chatbot
qa_pairs = {
    "hi": "Hello! How can I help you?",
    "what is your name": "I am your assistant chatbot.",
    "how can I contact support": "You can reach support at support@example.com.",
    "bye": "Goodbye! Have a nice day.",
    "thank you": "You're welcome!"
}

# NLP setup
vectorizer = TfidfVectorizer()
questions = list(qa_pairs.keys())
X = vectorizer.fit_transform(questions)

# Home route - UI
@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
      <title>Chatbot</title>
      <style>
        body { font-family: Arial; background: #f0f0f0; padding: 40px; }
        #chatbox { max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 10px; }
        .msg { margin: 10px 0; }
        .user { text-align: right; font-weight: bold; }
        .bot { text-align: left; color: blue; font-weight: bold; }
        input, button { padding: 10px; font-size: 16px; margin-top: 10px; }
      </style>
    </head>
    <body>
      <div id="chatbox">
        <h2>🤖 AI Chatbot</h2>
        <div id="messages"></div>
        <input id="input" type="text" placeholder="Ask me something..." />
        <button onclick="send()">Send</button>
      </div>

      <script>
        function send() {
          const input = document.getElementById('input');
          const messages = document.getElementById('messages');
          const userText = input.value;
          messages.innerHTML += `<div class='msg user'>You: ${userText}</div>`;
          fetch('/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ message: userText })
          })
          .then(res => res.json())
          .then(data => {
            messages.innerHTML += `<div class='msg bot'>Bot: ${data.response}</div>`;
            input.value = '';
          });
        }
      </script>
    </body>
    </html>
    """)

# Chat route - backend logic
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message'].lower()
    input_vec = vectorizer.transform([user_input])
    similarity = cosine_similarity(input_vec, X)
    best_match_idx = similarity.argmax()

    if similarity[0, best_match_idx] > 0.3:
        return jsonify({"response": qa_pairs[questions[best_match_idx]]})
    else:
        return jsonify({"response": "Sorry, I didn’t understand that. Can you rephrase?"})

# Run app
if __name__ == '__main__':
    app.run(debug=True)
