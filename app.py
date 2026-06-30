from flask import Flask, render_template, request
from dotenv import load_dotenv
from PyPDF2 import PdfReader
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
pdf_text = ""

def ask_ai(question):

    global pdf_text

    prompt = f"""
Use the study notes below to answer the question.

Study Notes:
{pdf_text}

Question:
{question}

If the answer is not in the notes, say:
'I couldn't find that information in the uploaded notes.'
"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": prompt
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

    global pdf_text

    if "file" not in request.files:
        return render_template(
            "index.html",
            chat_history=chat_history
        )

    file = request.files["file"]

    if file.filename == "":
        return render_template(
            "index.html",
            chat_history=chat_history
        )

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(filepath)

    reader = PdfReader(filepath)

    pdf_text = ""

    for page in reader.pages:

        text = page.extract_text()

        if text:
            pdf_text += text + "\n"

    print("========== PDF CONTENT ==========")
    print(pdf_text)
    print("=================================")

    return render_template(
        "index.html",
        chat_history=chat_history
    )

if __name__ == "__main__":
    app.run(debug=True)