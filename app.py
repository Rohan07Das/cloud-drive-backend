import os
import requests  # Required for sending HTTP POST requests to Brevo
from flask import Flask, request, jsonify
from supabase import create_client
from flask_cors import CORS
from functools import wraps

# ─── EXTRACTION LAYER: AUTO LOAD VARIABLES FROM .ENV ───
from dotenv import load_dotenv
load_dotenv()  # Injects your .env keys into system environment memory automatically

app = Flask(__name__)

# ─────────────────────────────────────────────
# CORS (UPDATED TO ALLOW CUSTOM HEADERS NATIVELY)
# ─────────────────────────────────────────────
CORS(app, resources={
    r"/*": {
        "origins": [
            "http://localhost:3000",
            "https://cloud-drive-frontend-theta.vercel.app"
        ],
        "allow_headers": ["Content-Type", "Authorization"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "supports_credentials": True
    }
})

# ─────────────────────────────────────────────
# SUPABASE & BREVO CONFIGURATIONS
# ─────────────────────────────────────────────
SUPABASE_URL = "https://kfjhespnobypmizhpszd.supabase.co"
SUPABASE_KEY = "sb_publishable_M1olt9EaUS7JqvY_Izv1cw_Y7GwEAcO"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

BUCKET = "files"

# Secrets are now requested securely from the operating environment
BREVO_API_KEY = os.environ.get("BREVO_API_KEY")
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "aisenticpulse@gmail.com")

# ─────────────────────────────────────────────
# BREVO SYSTEM PIPELINE UTILITIES
# ─────────────────────────────────────────────
def dispatch_admin_notification(client_name, client_email, message_content):
    """Sends the user's query to your inbox with reply-to configuration."""
    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json"
    }
    
    payload = {
        "sender": {"name": "Cloud Portal Alerts", "email": ADMIN_EMAIL},
        "to": [{"email": ADMIN_EMAIL, "name": "Admin Support"}],
        "replyTo": {"email": client_email, "name": client_name},
        "subject": f"New Contact Inquiry from {client_name}",
        "htmlContent": f"""
        <div style="font-family: sans-serif; padding: 20px; color: #333; line-height: 1.6;">
            <h2 style="color: #4f46e5; border-bottom: 2px solid #e5e7eb; padding-bottom: 10px;">New Message Received</h2>
            <p><strong>Sender Name:</strong> {client_name}</p>
            <p><strong>Sender Email:</strong> {client_email}</p>
            <div style="background-color: #f3f4f6; padding: 15px; border-left: 4px solid #4f46e5; margin-top: 15px; border-radius: 4px;">
                <p style="margin: 0; white-space: pre-wrap;">{message_content}</p>
            </div>
            <p style="font-size: 12px; color: #6b7280; margin-top: 20px;">💡 Tip: You can reply directly to this email to respond to the sender.</p>
        </div>
        """
    }
    return requests.post(url, json=payload, headers=headers)

def dispatch_client_greeting(client_name, client_email):
    """Sends a responsive dark-themed greeting back to the visitor."""
    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json"
    }
    
    payload = {
        "sender": {"name": "SenticPulse Support", "email": ADMIN_EMAIL},
        "to": [{"email": client_email, "name": client_name}],
        "subject": "Thank you for reaching out to SenticPulse AI",
        "htmlContent": f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
        </head>
        <body style="margin: 0; padding: 0; background-color: #0b0f19; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
            <table width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color: #0b0f19; padding: 40px 20px;">
                <tr>
                    <td align="center">
                        <table width="600" border="0" cellspacing="0" cellpadding="0" style="background-color: #111827; border: 1px solid #1f2937; border-radius: 12px; overflow: hidden; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.3);">
                            <tr><td height="4" style="background: linear-gradient(90deg, #4f46e5, #06b6d4);"></td></tr>
                            <tr>
                                <td style="padding: 40px, 30px; text-align: left; padding: 40px;">
                                    <h2 style="color: #ffffff; margin-top: 0; font-size: 24px; font-weight: 600; letter-spacing: -0.025em;">Hello {client_name},</h2>
                                    <p style="color: #9ca3af; font-size: 16px; line-height: 1.7; margin-bottom: 24px;">
                                        Thank you for contacting us! We've received your inquiry through our platform portal. Our team is reviewing the payload details and will get back to you shortly.
                                    </p>
                                    <div style="background: rgba(79, 70, 229, 0.1); border: 1px solid rgba(79, 70, 229, 0.2); border-radius: 8px; padding: 16px; margin-bottom: 24px; text-align: center;">
                                        <span style="color: #818cf8; font-size: 14px; font-weight: 500;">⚡ Case Transmission Logged Successfully</span>
                                    </div>
                                    <p style="color: #9ca3af; font-size: 15px; margin-bottom: 0;">
                                        Best regards,<br>
                                        <span style="color: #ffffff; font-weight: 600;">SenticPulse Core Engine Tech Team</span>
                                    </p>
                                </td>
                            </tr>
                            <tr>
                                <td style="background-color: #0f172a; padding: 20px; text-align: center; border-top: 1px solid #1f2937;">
                                    <p style="color: #6b7280; font-size: 12px; margin: 0;">This is an automated operational confirmation. Please do not reply directly to this notice.</p>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """
    }
    return requests.post(url, json=payload, headers=headers)

# ─────────────────────────────────────────────
# AUTH
# ─────────────────────────────────────────────
def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Unauthorized"}), 401

        token = auth_header.split(" ")[1]

        try:
            user_response = supabase.auth.get_user(token)

            if not user_response:
                return jsonify({"error": "Invalid token"}), 401

        except Exception:
            return jsonify({"error": "Session expired"}), 401

        return f(*args, **kwargs)

    return decorated

# ─────────────────────────────────────────────
# HEALTH
# ─────────────────────────────────────────────
@app.route("/")
def home():
    return jsonify({
        "status": "healthy",
        "message": "Cloud Drive API running"
    })

# ─────────────────────────────────────────────
# CONTACT FORM SUBMISSION ENDPOINT (CORS OPTIMIZED)
# ─────────────────────────────────────────────
@app.route("/api/contact", methods=["POST"])
def contact():
    data = request.json
    if not data:
        return jsonify({"error": "Payload missing"}), 400

    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    if not name or not email or not message:
        return jsonify({"error": "All explicit parameters (name, email, message) are required"}), 400

    try:
        # 1. Forward the user message to your admin email
        admin_res = dispatch_admin_notification(name, email, message)
        
        # 2. Fire the themed confirmation to the customer
        dispatch_client_greeting(name, email)

        if admin_res.status_code in [200, 201]:
            return jsonify({
                "success": True,
                "message": "Email delivery transaction processed cleanly via Brevo."
            }), 200
        else:
            return jsonify({
                "error": "Brevo communication gateway failure",
                "details": admin_res.text
            }), 500

    except Exception as e:
        return jsonify({
            "error": "Server error while processing email delivery",
            "details": str(e)
        }), 500

# ─────────────────────────────────────────────
# LOGIN
# ─────────────────────────────────────────────
@app.route("/login", methods=["POST"])
def login():

    data = request.json

    email = data.get("email")
    password = data.get("password")

    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        access_token = response.session.access_token

        return jsonify({
            "token": access_token,
            "message": "Login successful"
        })

    except Exception:
        return jsonify({
            "error": "Invalid email or password"
        }), 401

# ─────────────────────────────────────────────
# CREATE FOLDER
# ─────────────────────────────────────────────
@app.route("/create-folder", methods=["POST"])
@require_auth
def create_folder():

    data = request.json
    folder_name = data.get("folder")

    if not folder_name:
        return jsonify({"error": "Folder name required"}), 400

    try:
        # Create empty placeholder file
        supabase.storage.from_(BUCKET).upload(
            f"folders/{folder_name}/.keep",
            b"",
            {
                "content-type": "text/plain",
                "upsert": "true"
            }
        )

        return jsonify({
            "message": "Folder created"
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

# ─────────────────────────────────────────────
# LIST FOLDERS
# ─────────────────────────────────────────────
@app.route("/folders")
@require_auth
def list_folders():

    try:
        response = supabase.storage.from_(BUCKET).list("folders")

        folders = []

        for item in response:

            item_id = item.get("id")

            if item_id is None:
                folders.append({
                    "name": item["name"]
                })

        return jsonify(folders)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

# ─────────────────────────────────────────────
# UPLOAD FILE
# ─────────────────────────────────────────────
@app.route("/upload", methods=["POST"])
@require_auth
def upload_file():

    try:
        file = request.files["file"]

        folder = request.form.get("folder", "")

        if folder.strip() != "":
            upload_path = f"folders/{folder}/{file.filename}"
        else:
            upload_path = f"files/{file.filename}"

        supabase.storage.from_(BUCKET).upload(
            upload_path,
            file.read(),
            {
                "content-type": file.content_type,
                "upsert": "true"
            }
        )

        return jsonify({
            "message": "File uploaded"
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

# ─────────────────────────────────────────────
# LIST ROOT FILES
# ─────────────────────────────────────────────
@app.route("/files")
@require_auth
def list_files():

    try:
        response = supabase.storage.from_(BUCKET).list("files")

        files = []

        for f in response:

            if f["name"] == ".emptyFolderPlaceholder":
                continue

            size = 0

            if f.get("metadata"):
                size = f["metadata"].get("size", 0)

            files.append({
                "name": f["name"],
                "size": size
            })

        return jsonify(files)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

# ─────────────────────────────────────────────
# LIST FILES INSIDE FOLDER
# ─────────────────────────────────────────────
@app.route("/folder-files/<folder_name>")
@require_auth
def folder_files(folder_name):

    try:
        response = supabase.storage.from_(BUCKET).list(
            f"folders/{folder_name}"
        )

        files = []

        for f in response:

            if f["name"] == ".keep":
                continue

            size = 0

            if f.get("metadata"):
                size = f["metadata"].get("size", 0)

            files.append({
                "name": f["name"],
                "size": size,
                "folder": folder_name
            })

        return jsonify(files)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

# ─────────────────────────────────────────────
# DELETE FILE
# ─────────────────────────────────────────────
@app.route("/delete/<filename>", methods=["DELETE"])
@require_auth
def delete_file(filename):

    try:
        supabase.storage.from_(BUCKET).move(
            f"files/{filename}",
            f"recycle/{filename}"
        )

        return jsonify({
            "message": "Moved to recycle"
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500
    
# ─────────────────────────────────────────────
# DELETE FILE FROM FOLDER
# ─────────────────────────────────────────────
@app.route("/delete-folder-file/<folder>/<filename>", methods=["DELETE"])
@require_auth
def delete_folder_file(folder, filename):

    try:

        source_path = f"folders/{folder}/{filename}"

        recycle_path = f"recycle/folders/{folder}/{filename}"

        # CREATE RECYCLE FOLDER STRUCTURE
        supabase.storage.from_(BUCKET).move(
            source_path,
            recycle_path
        )

        return jsonify({
            "message": "Moved to recycle"
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500

# ─────────────────────────────────────────────
# RECYCLE LIST
# ─────────────────────────────────────────────
@app.route("/recycle")
@require_auth
def recycle_files():

    try:

        files = []

        # ROOT RECYCLE FILES
        root_response = supabase.storage.from_(BUCKET).list("recycle")

        for f in root_response:

            # SKIP FOLDER CONTAINER
            if f.get("id") is None:
                continue

            size = 0

            if f.get("metadata"):
                size = f["metadata"].get("size", 0)

            files.append({
                "name": f["name"],
                "size": size,
                "folder": None
            })

        # RECYCLE FOLDER FILES
        folders_response = supabase.storage.from_(BUCKET).list("recycle/folders")

        for folder in folders_response:

            folder_name = folder["name"]

            folder_files = supabase.storage.from_(BUCKET).list(
                f"recycle/folders/{folder_name}"
            )

            for f in folder_files:

                size = 0

                if f.get("metadata"):
                    size = f["metadata"].get("size", 0)

                files.append({
                    "name": f["name"],
                    "size": size,
                    "folder": folder_name
                })

        return jsonify(files)

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500

# ─────────────────────────────────────────────
# RESTORE ROOT FILE
# ─────────────────────────────────────────────
@app.route("/restore/<filename>", methods=["POST"])
@require_auth
def restore_file(filename):

    try:

        supabase.storage.from_(BUCKET).move(
            f"recycle/{filename}",
            f"files/{filename}"
        )

        return jsonify({
            "message": "Restored"
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500
    
# ─────────────────────────────────────────────
# RESTORE FOLDER FILE
# ─────────────────────────────────────────────
@app.route("/restore-folder-file/<folder>/<filename>", methods=["POST"])
@require_auth
def restore_folder_file(folder, filename):

    try:

        supabase.storage.from_(BUCKET).move(
            f"recycle/folders/{folder}/{filename}",
            f"folders/{folder}/{filename}"
        )

        return jsonify({
            "message": "Folder file restored"
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500

# ─────────────────────────────────────────────
# PERMANENT DELETE
# ─────────────────────────────────────────────
@app.route("/permanent_delete/<filename>", methods=["DELETE"])
@require_auth
def permanent_delete(filename):

    try:
        supabase.storage.from_(BUCKET).remove([
            f"recycle/{filename}"
        ])

        return jsonify({
            "message": "Deleted permanently"
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

# ─────────────────────────────────────────────
# DOWNLOAD ROOT FILE
# ─────────────────────────────────────────────
@app.route("/download/<filename>")
@require_auth
def download_file(filename):

    try:
        url = supabase.storage.from_(BUCKET).get_public_url(
            f"files/{filename}"
        )

        download_url = f"{url}?download="

        return jsonify({
            "download_url": download_url
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

# ─────────────────────────────────────────────
# DOWNLOAD FILE FROM FOLDER
# ─────────────────────────────────────────────
@app.route("/download-folder-file/<folder>/<filename>")
@require_auth
def download_folder_file(folder, filename):

    try:
        url = supabase.storage.from_(BUCKET).get_public_url(
            f"folders/{folder}/{filename}"
        )

        download_url = f"{url}?download="

        return jsonify({
            "download_url": download_url
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

# ─────────────────────────────────────────────
# START SERVER
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)
