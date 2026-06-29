from flask import Flask, render_template, request
from dotenv import load_dotenv
import requests
import os

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

chat_history = []

def ask_ai(question):

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ]
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=data
    )

    result = response.json()

    return result["choices"][0]["message"]["content"]

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        question = request.form["question"]

        answer = ask_ai(question)

        chat_history.append({
            "question": question,
            "answer": answer
        })

    return render_template(
        "index.html",
        chat_history=chat_history
    )


@app.route("/upload", methods=["POST"])
def upload():

    file = request.files["file"]

    if file:

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            file.filename
        )

        file.save(filepath)

    return render_template(
        "index.html",
        chat_history=chat_history
    )


if __name__ == "__main__":
    app.run(debug=True)