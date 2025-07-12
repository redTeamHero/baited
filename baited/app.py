from flask import Flask, send_from_directory, request, render_template, jsonify
import os, json
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
DATA_FILE = "logs.json"

def load_logs():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_logs(logs):
    with open(DATA_FILE, "w") as f:
        json.dump(logs, f, indent=2)

@app.route("/track/<label>")
def track(label):
    ip = request.remote_addr
    user_agent = request.headers.get("User-Agent", "")
    referer = request.headers.get("Referer", "None")
    logs = load_logs()
    logs.append({
        "ip": ip,
        "label": label,
        "user_agent": user_agent,
        "referer": referer,
        "time": datetime.utcnow().isoformat()
    })
    save_logs(logs)
    filename = secure_filename(label + ".jpg")
    return send_from_directory("static/bait", filename)

@app.route("/dashboard")
def dashboard():
    logs = load_logs()
    return render_template("dashboard.html", logs=logs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
