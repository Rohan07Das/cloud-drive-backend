import os
from flask import Flask, request, jsonify, send_from_directory
from supabase import create_client
from flask_cors import CORS
from functools import wraps

app = Flask(__name__)

# --- SECURE CORS ---
# This tells Flask it is safe to accept login requests specifically from your React app
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

SUPABASE_URL = "https://kfjhespnobypmizhpszd.supabase.co"
# (Note: In a production app, keep this key hidden in a .env file!)
SUPABASE_KEY = "sb_publishable_M1olt9EaUS7JqvY_Izv1cw_Y7GwEAcO"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
BUCKET = "files"

# --- SECURITY LOCK: Verify Token with Supabase ---
def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Unauthorized access"}), 401
        
        token = auth_header.split(" ")[1]
        
        try:
            # Ask Supabase if this token is valid and belongs to a real user
            user_response = supabase.auth.get_user(token)
            if not user_response:
                return jsonify({"error": "Invalid token"}), 401
        except Exception as e:
            return jsonify({"error": "Session expired or invalid"}), 401
            
        return f(*args, **kwargs)
    return decorated

# --- SERVE THE HTML DASHBOARD ---
@app.route("/")
def home():
    # This automatically finds and serves your index.html file from the same folder!
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 'index.html')

# --- SUPABASE LOGIN ROUTE ---
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    
    try:
        # Send credentials to Supabase Auth
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        
        # Extract the secure access token provided by Supabase
        access_token = response.session.access_token
        return jsonify({"token": access_token, "message": "Login successful"})
        
    except Exception as e:
        # Supabase will throw an error if the password/email is wrong
        return jsonify({"error": "Invalid email or password"}), 401


# --- PROTECTED ROUTES ---

@app.route("/upload", methods=["POST"])
@require_auth
def upload_file():
    file = request.files["file"]
    supabase.storage.from_(BUCKET).upload(
        f"files/{file.filename}",
        file.read(),
        {"content-type": file.content_type, "upsert": "true"}
    )
    return jsonify({"message": "File uploaded"})

@app.route("/files")
@require_auth
def list_files():
    response = supabase.storage.from_(BUCKET).list("files")
    files = []
    for f in response:
        size = f.get("metadata", {}).get("size", 0) if f.get("metadata") else 0
        files.append({"name": f["name"], "size": size})
    return jsonify(files)

@app.route("/delete/<filename>", methods=["DELETE"])
@require_auth
def delete_file(filename):
    supabase.storage.from_(BUCKET).move(f"files/{filename}", f"recycle/{filename}")
    return jsonify({"message":"Moved to recycle bin"})

@app.route("/recycle")
@require_auth
def recycle_files():
    response = supabase.storage.from_(BUCKET).list("recycle")
    files = []
    for f in response:
        size = f.get("metadata", {}).get("size", 0) if f.get("metadata") else 0
        files.append({"name": f["name"], "size": size})
    return jsonify(files)

@app.route("/restore/<filename>", methods=["POST"])
@require_auth
def restore_file(filename):
    supabase.storage.from_(BUCKET).move(f"recycle/{filename}", f"files/{filename}")
    return jsonify({"message":"File restored"})

@app.route("/permanent_delete/<filename>", methods=["DELETE"])
@require_auth
def permanent_delete(filename):
    supabase.storage.from_(BUCKET).remove([f"recycle/{filename}"])
    return jsonify({"message":"File permanently deleted"})

@app.route("/download/<filename>")
@require_auth
def download_file(filename):
    url = supabase.storage.from_(BUCKET).get_public_url(f"files/{filename}")
    download_url = f"{url}?download="
    return jsonify({"download_url": download_url})


if __name__ == "__main__":
    app.run(debug=True)