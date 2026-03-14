from flask import Flask, request, jsonify, render_template
import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

user_name = ""

# Load knowledge base
base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "knowledge.json")

with open(file_path, "r") as file:
    knowledge = json.load(file)

# Prepare questions and answers
questions = list(knowledge.keys())
answers = list(knowledge.values())

# TF-IDF setup
vectorizer = TfidfVectorizer()
question_vectors = vectorizer.fit_transform(questions)


@app.route("/")
def home():
    return render_template("design.html")


@app.route("/chat", methods=["POST"])
def chat():
    global user_name

    data = request.json
    user_message = data["message"].strip()

    # Ask for name first
    if user_name == "":
        user_name = user_message
        reply = f"👋 Nice to meet you, {user_name}! 🤖<br>" \
                "📚 What would you like to learn today?<br>" \
                "1️⃣ What is Indexing<br>" \
                "2️⃣ Types of Indexes<br>" \
                "3️⃣ Performance Tuning<br>" \
                "4️⃣ SQL Index Commands"
        return jsonify({"reply": reply})

    reply = chatbot_response(user_message, user_name)
    return jsonify({"reply": reply})


def chatbot_response(user_input, name):

    user_input = user_input.lower().strip()

    # Menu commands
    if user_input in ["help", "menu", "options"]:
        reply = "ℹ️ You can ask questions about indexing, SQL indexes, or performance tuning."

    # Menu numbers
    elif user_input in ["1", "2", "3", "4"]:
        reply = knowledge.get(user_input, "Option not available.")
        

    else:
        # Convert user input into vector
        user_vector = vectorizer.transform([user_input])

        # Compare similarity
        similarity = cosine_similarity(user_vector, question_vectors)

        best_match_index = similarity.argmax()
        best_score = similarity[0][best_match_index]

        # If similarity is good enough
        if best_score > 0.45:
            reply = answers[best_match_index]
        else:
            reply = f"😅 Sorry {name}, I couldn't understand that question."

    reply += "<br><br>📚 Menu:<br>" \
             "1️⃣ What is Indexing<br>" \
             "2️⃣ Types of Indexes<br>" \
             "3️⃣ Performance Tuning<br>" \
             "4️⃣ SQL Index Commands"

    return reply


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)


