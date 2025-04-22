from flask import Flask, request, jsonify, send_from_directory, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3, os
from Main import generate_video

app = Flask(__name__)
app.secret_key = 'supersecretkey'
CORS(app, supports_credentials=True)

VIDEO_FOLDER = "videos"
os.makedirs(VIDEO_FOLDER, exist_ok=True)

def get_db():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

# def get_db():
#     db_path = app.config.get('DB_PATH', 'users.db')
#     conn = sqlite3.connect(db_path, check_same_thread=False)
#     conn.row_factory = sqlite3.Row
#     return conn


@app.before_request
def init_db():
    db = get_db()
    db.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')
    db.execute('''CREATE TABLE IF NOT EXISTS videos (
        id INTEGER PRIMARY KEY, user_id INTEGER, prompt TEXT, filename TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id))''')
    db.commit()

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data["username"]
    password = generate_password_hash(data["password"])
    try:
        db = get_db()
        db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        db.commit()
        return jsonify({"message": "User registered!"})
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username already taken"}), 400

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data["username"]
    password = data["password"]
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    if user and check_password_hash(user["password"], password):
        session["user_id"] = user["id"]
        return jsonify({"message": "Logged in", "username": username})
    return jsonify({"error": "Invalid credentials"}), 401

@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id", None)
    return jsonify({"message": "Logged out"})

@app.route("/generate-video", methods=["POST"])
def generate_video_route():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    prompt = request.json.get("prompt", "")
    user_id = session["user_id"]
    video_file = generate_video(prompt)

    if video_file and os.path.exists(video_file):
        filename = os.path.basename(video_file)
        final_path = os.path.join(VIDEO_FOLDER, filename)
        os.rename(video_file, final_path)

        db = get_db()
        db.execute("INSERT INTO videos (user_id, prompt, filename) VALUES (?, ?, ?)", (user_id, prompt, filename))
        db.commit()

        return jsonify({"video_url": f"http://localhost:5000/videos/{filename}"})
    return jsonify({"error": "Video generation failed"}), 500

@app.route("/videos/<path:filename>")
def serve_video(filename):
    return send_from_directory(VIDEO_FOLDER, filename)

@app.route("/my-history", methods=["GET"])
def my_history():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    user_id = session["user_id"]
    db = get_db()
    videos = db.execute("SELECT prompt, filename FROM videos WHERE user_id = ?", (user_id,)).fetchall()

    return jsonify([{
        "prompt": v["prompt"],
        "video_url": f"http://localhost:5000/videos/{v['filename']}"
    } for v in videos])

if __name__ == "__main__":
    app.run(debug=True)
    
    
#     from flask import Flask, request, jsonify, send_from_directory
# import os
# from Single_Main import generate_video  # assuming this is the function from your main script

# app = Flask(__name__)
# VIDEO_FOLDER = "videos"
# os.makedirs(VIDEO_FOLDER, exist_ok=True)

# @app.route("/generate-video", methods=["POST"])
# def generate_video_route():
#     data = request.get_json()
#     prompt = data.get("prompt", "")

#     # Generate the video
#     video_file = generate_video(prompt)

#     if video_file and os.path.exists(video_file):
#         # Move video to a public folder (e.g., "videos/")
#         filename = os.path.basename(video_file)
#         final_path = os.path.join(VIDEO_FOLDER, filename)
#         os.rename(video_file, final_path)

#         return jsonify({
#             "video_url": f"http://localhost:5000/videos/{filename}"
#         })
#     else:
#         return jsonify({"error": "Video generation failed"}), 500

# @app.route("/videos/<path:filename>")
# def serve_video(filename):
#     return send_from_directory(VIDEO_FOLDER, filename)

