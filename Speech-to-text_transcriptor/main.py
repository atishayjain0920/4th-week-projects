from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import speech_recognition as sr
import os

# Serve files from the 'frontend' directory
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend"))

app = Flask(__name__, static_folder=frontend_dir, static_url_path="")
CORS(app)

# Serve index.html
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

# Serve static assets like JS, CSS, images, etc.
@app.route("/<path:filename>")
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

# Speech recognition endpoint
@app.route("/transcribe", methods=["GET"])
def transcribe_audio():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("🎙 Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source)
            print("🎧 Listening...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print("📝 Transcribing...")
            text = recognizer.recognize_google(audio)
            return jsonify({"success": True, "text": text})
    except sr.WaitTimeoutError:
        return jsonify({"success": False, "error": "⏰ Timeout: No speech detected."})
    except sr.UnknownValueError:
        return jsonify({"success": False, "error": "😕 Could not understand the audio."})
    except sr.RequestError:
        return jsonify({"success": False, "error": "🚫 Could not connect to Google API."})
    except Exception as e:
        return jsonify({"success": False, "error": f"Unexpected error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
