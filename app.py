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
# BREVO SYSTEM PIPELINE UTILITIES (NEO-BRUTALIST THEME ALIGNED)
# ─────────────────────────────────────────────
def dispatch_admin_notification(client_name, client_email, message_content):
    """Sends the user's query to your inbox styled with the Neo-Brutalist card layout."""
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
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="color-scheme" content="light">
    <meta name="supported-color-schemes" content="light">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
</head>
<body style="margin: 0; padding: 0; background-color: #f6f3ea; font-family: 'Space Grotesk', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
    
    <table width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color: #f6f3ea; padding: 40px 20px;">
        <tr>
            <td align="center">
                
                <table width="550" border="0" cellspacing="0" cellpadding="0" style="background-color: #ffffff; border: 3px solid #000000; border-radius: 32px; box-shadow: 10px 10px 0px #000000; overflow: hidden; margin-bottom: 24px;">
                    
                    <tr>
                        <td style="padding: 36px 32px 10px 32px; text-align: left; background-color: #FFFDF1;">
                            
                            <div style="background-color: #FFFDF1; display: inline-block; padding: 4px 12px; border: 2px solid #000000; border-radius: 8px; margin-bottom: 12px; box-shadow: 2px 2px 0px #000000;">
                                <h1 style="font-family: 'Space Grotesk', Arial Black, Gadget, sans-serif; font-size: 24px; font-weight: 700; color: #000000; text-transform: uppercase; margin: 0; letter-spacing: -0.5px;">
                                    USER INQUIRY ❓
                                </h1>
                            </div>
                            <div style="height: 3px; background-color: #000000; margin-bottom: 24px; width: 100%;"></div>
                            
                            <p style="font-family: 'Space Grotesk', sans-serif; font-size: 11px; font-weight: 700; color: #7a8a9e; text-transform: uppercase; margin: 0 0 6px 4px; letter-spacing: 0.5px;">
                                IDENTITY NAME
                            </p>
                            <div style="background-color: #ffffff; border: 2px solid #000000; border-radius: 16px; padding: 14px 16px; font-family: 'Space Grotesk', sans-serif; font-size: 16px; color: #000000; font-weight: 700; margin-bottom: 20px; box-shadow: 3px 3px 0px #000000;">
                                {client_name}
                            </div>

                            <p style="font-family: 'Space Grotesk', sans-serif; font-size: 11px; font-weight: 700; color: #7a8a9e; text-transform: uppercase; margin: 0 0 6px 4px; letter-spacing: 0.5px;">
                                ROUTING EMAIL SOURCE
                            </p>
                            <div style="background-color: #ffffff; border: 2px solid #000000; border-radius: 16px; padding: 14px 16px; font-family: 'Space Grotesk', sans-serif; font-size: 16px; color: #000000; font-weight: 700; margin-bottom: 10px; box-shadow: 3px 3px 0px #000000;">
                                {client_email}
                            </div>

                        </td>
                    </tr>
                    
                    <tr>
                        <td background="https://thumbs.dreamstime.com/z/question-doodles-10980766.jpg" 
                            style="padding: 20px 32px 36px 32px; text-align: left; background-color: #ffffff; background-image: url('https://thumbs.dreamstime.com/z/question-doodles-10980766.jpg'); background-repeat: repeat; background-position: center top; background-size: 280px auto;">
                            
                            <p style="margin: 0 0 6px 4px;">
                                <span style="background-color: #ffffff; padding: 2px 6px; border: 2px solid #000000; border-radius: 4px; box-shadow: 1px 1px 0px #000000; font-family: 'Space Grotesk', sans-serif; font-size: 11px; font-weight: 700; color: #111111; text-transform: uppercase; letter-spacing: 0.5px;">PAYLOAD MESSAGE CONTENT</span>
                            </p>
                            <div style="background-color: #ffffff; border: 2px solid #000000; border-radius: 16px; padding: 16px; margin-bottom: 28px; box-shadow: 3px 3px 0px #000000; min-height: 80px;">
                                <p style="color: #000000; margin: 0; font-family: 'Space Grotesk', sans-serif; font-size: 15px; line-height: 1.6; font-weight: 500; white-space: pre-wrap;">{message_content}</p>
                            </div>
                            
                            <table width="100%" border="0" cellspacing="0" cellpadding="0">
                                <tr>
                                    <td>
                                        <a href="mailto:{client_email}" style="display: block; text-decoration: none; background-color: #ffffff; border: 2px solid #000000; border-radius: 16px; padding: 16px; color: #000000; font-family: 'Space Grotesk', Arial Black, Gadget, sans-serif; font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; box-shadow: 4px 4px 0px #F4C542; text-align: center;">
                                            🗯️ REPLY / GIVE SOLUTIONS
                                        </a>
                                    </td>
                                </tr>
                            </table>

                        </td>
                    </tr>
                </table>

                <table width="530" border="0" cellspacing="0" cellpadding="0" style="background-color: #000000; border-radius: 14px; box-shadow: 3px 3px 0px #000000;">
                    <tr>
                        <td style="padding: 12px; text-align: center; background-color: #000000; border-radius: 14px;">
                            <p style="color: #ffffff; font-family: 'Space Grotesk', sans-serif; font-size: 11px; margin: 0; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px;">
                                SYSTEM TRACK NODE // INBOUND ROUTING
                            </p>
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

def dispatch_client_greeting(client_name, client_email):
    """Sends a responsive Brutalist cream-themed greeting back to the platform visitor."""
    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json"
    }
    
    payload = {
        "sender": {"name": "SenticPulse Support", "email": ADMIN_EMAIL},
        "to": [{"email": client_email, "name": client_name}],
        "subject": "Transmission Acknowledged - SenticPulse AI",
        "htmlContent": f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="color-scheme" content="light">
    <meta name="supported-color-schemes" content="light">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
</head>
<body style="margin: 0; padding: 0; background-color: #f6f3ea; font-family: 'Space Grotesk', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
    
    <table width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color: #f6f3ea; padding: 40px 20px;">
        <tr>
            <td align="center">
                
                <table width="550" border="0" cellspacing="0" cellpadding="0" style="background-color: #ffffff; border: 3px solid #000000; border-radius: 32px; box-shadow: 10px 10px 0px #000000; overflow: hidden; margin-bottom: 24px;">
                    
                    <tr>
                        <td style="padding: 36px 32px 10px 32px; text-align: left; background-color: #ffffff;">
                            
                            <h1 style="font-family: 'Space Grotesk', Arial Black, Gadget, sans-serif; font-size: 24px; font-weight: 700; color: #000000; text-transform: uppercase; margin-top: 0; margin-bottom: 12px; letter-spacing: -0.5px;">
                                GREETINGS 👋
                            </h1>
                            <div style="height: 3px; background-color: #000000; margin-bottom: 24px; width: 100%;"></div>
                            
                            <h3 style="font-family: 'Space Grotesk', sans-serif; font-size: 18px; font-weight: 700; color: #000000; margin-top: 0; margin-bottom: 12px;">
                                Hello {client_name},
                            </h3>
                            
                            <p style="font-family: 'Space Grotesk', sans-serif; color: #000000; font-size: 15px; line-height: 1.6; margin-top: 0; margin-bottom: 15px; font-weight: 500;">
                                Thank you for connecting! Your submission message payload has cleared our system ingress. Our team is processing the entry and will establish custom routing shortly.
                            </p>

                        </td>
                    </tr>
                    
                    <tr>
                        <td background="https://img.magnific.com/premium-photo/children-education-hand-drawn-doodle-illustration-set-back-school-elements-icons_1257429-42720.jpg" 
                            style="padding: 10px 32px 36px 32px; text-align: left; background-color: #ffffff; background-image: url('https://img.magnific.com/premium-photo/children-education-hand-drawn-doodle-illustration-set-back-school-elements-icons_1257429-42720.jpg'); background-repeat: repeat; background-position: center top; background-size: 320px auto;">
                            
                            <div style="background-color: #bcd9d0; border: 2px solid #000000; border-radius: 16px; padding: 14px; margin-bottom: 24px; text-align: center; box-shadow: 3px 3px 0px #000000;">
                                <span style="color: #000000; font-family: 'Space Grotesk', sans-serif; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">
                                    ☑️ YOUR QUERY WAS SECURELY RECEIVED.
                                </span>
                            </div>
                            
                            <div style="height: 2px; background-color: #000000; margin-top: 24px; margin-bottom: 16px; width: 100%;"></div>
                            
                            <div style="display: table; background-color: #ffffff; border: 2px solid #000000; border-radius: 12px; padding: 10px 14px; box-shadow: 3px 3px 0px #000000; text-align: left;">
                                <p style="font-family: 'Space Grotesk', sans-serif; font-size: 11px; color: #7a8a9e; margin: 0; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; line-height: 1.4;">
                                    CORE ROUTE:<br>
                                    <span style="color: #000000; font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 13px;">SENTICPULSE ENGINE AUTOMATION</span>
                                </p>
                            </div>
                            
                        </td>
                    </tr>
                </table>

                <table width="550" border="0" cellspacing="0" cellpadding="0" style="background-color: #f3dfdd; border: 3px solid #000000; border-radius: 20px; box-shadow: 4px 4px 0px #000000;">
                    <tr>
                        <td style="padding: 16px 20px; text-align: left; background-color: #f3dfdd; border-radius: 20px;">
                            <p style="color: #000000; font-family: 'Space Grotesk', sans-serif; font-size: 11px; margin: 0; font-weight: 700; text-transform: uppercase; line-height: 1.5; letter-spacing: 0.2px;">
                                ⚠️ NOTICE: This is an automated operational confirmation buffer. Direct terminal replies to this transmission are unmonitored.
                            </p>
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
