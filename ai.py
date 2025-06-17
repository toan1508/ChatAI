from flask import Flask, render_template, request, jsonify
from gtts import gTTS
import os
import openai
import datetime

app = Flask(__name__)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


openai.api_key = "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"

language = "en"

def set_language(lang):
    global language
    language = lang
    return "Đã chuyển sang tiếng Việt." if lang == "vi" else "Language set to English."

def speak(text):
    tts = gTTS(text=text, lang=language)
    filename = "static/output.mp3"
    tts.save(filename)
    return filename

def chat_with_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.form.get("query")
    global language

    if user_input.lower() == "switch to vie":
        msg = set_language("vi")
    elif user_input.lower() == "switch to en":
        msg = set_language("en")
    elif "time" in user_input.lower() or "giờ" in user_input.lower():
        now = datetime.datetime.now().strftime("%I:%M %p")
        msg = now
    else:
        msg = chat_with_gpt(user_input)

    audio_path = speak(msg)
    return jsonify({"text": msg, "audio": audio_path})

if __name__ == "__main__":
    app.run(debug=True)
