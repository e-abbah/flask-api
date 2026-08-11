from flask import Blueprint, request, jsonify
from email_validator import validate_email, EmailNotValidError
from extension import bcrypt
from db import get_connection
import secrets
from email_service import send_verification_email
from flask_jwt_extended import create_access_token
from datetime import datetime, timedelta


auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/", methods=["GET"])
def home():
    return "Flask is running"


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    fullname = data.get("fullname")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    # Validate required fields
    if not fullname or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    # Validate email
    try:
        validate_email(email)
    except EmailNotValidError as e:
        return jsonify({"error": str(e)}), 400
    

    conn = None
    cursor = None
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id from users where email = %s",
            (email, ),
        )
    # conn.commit()
    if cursor.fetchone():
        return jsonify({"success": False, "message": "Email already exists"}), 400


    # Validate password length
    if len(password) < 8:
        return jsonify({
            "success": False,
            "message": "Password must be at least 8 characters long"
        }), 400

    # Hash password
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    verification_token = secrets.token_urlsafe(32)



    

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (fullname, email, password, role, verification_token) VALUES (%s, %s, %s, %s, %s)",
            (fullname, email, hashed_password, role, verification_token)
        )

        conn.commit()
        verification_link = (f"https://flask-api-chqu.onrender.com/api/auth/verify-email/{verification_token}")
        subject = "Verify your email"
        html = f"<h2>Welcome {fullname}</h2><p>Please verify your email by clicking the link below:</p><p><a href=\"{verification_link}\">Verify Email</a></p>"

        send_verification_email(email, subject, html)

        return jsonify({
            "success": True,
            "message": "User registered successfully"
        }), 201

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

@auth_bp.route("/verify-email/<token>", methods=["GET"])
def verify_email(token):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT id
            FROM users
            WHERE verification_token = %s
            """, (token,))

        user = cursor.fetchone()

        if not user:
            return jsonify({
                "success": False,
                "message": "Invalid verification link."
            }), 400

        cursor.execute("""
            UPDATE users
            SET
                is_verified = TRUE,
                verification_token = NULL
            WHERE id = %s
        """, (user["id"],))

        # print(cursor.fetchone())

        conn.commit()

        return jsonify({
            "success": True,
            "message": "Email verified successfully."
        }), 200

    finally:
        cursor.close()
        conn.close()
from flask_jwt_extended import create_access_token

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email= data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "success": False,
            "message": "Email and password are required"
        }), 400
    
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id,
                   fullname,
                   email,
                   password,
                   role,
                   is_verified
                   FROM users
                   WHERE email=%s
                """, (email,))
        user = cursor.fetchone()
        if not user:
            return jsonify({
                "success": False,
                "message": "Invalid email or password"
            }), 401

        if not bcrypt.check_password_hash(user["password"], password):
            return jsonify({
                "success": False,
                "message": "Invalid email or password."
            }), 401

        if not user["is_verified"]:
            return jsonify({
                "success": False,
                "message": "Please verify your email before logging in"
            }), 403

        access_token = create_access_token(
            identity=str(user["id"]),
            additional_claims={
                "role": user["role"],
                "email": user["email"]
            }
        )

        return jsonify(
            {
               "success": True,
                "message": "Login successful",
                "access_token": access_token,
                "user": {
                    "id": user["id"],
                    "fullname": user["fullname"],
                    "email": user["email"],
                    "role": user["role"]
                }  
            }), 200

    finally:
        cursor.close()
        conn.close()

@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({
            "success": False,
            "message": "Email is required."
        }), 400
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, fullname, email
            FROM users
            WHERE email=%s
        """, (email,))

        user = cursor.fetchone()
        if not user:
            return jsonify({
                "success": False,
                "message": "Email not found."
            }), 404
        
        reset_token = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(minutes=30)

        cursor.execute("""
            UPDATE users
            SET reset_token = %s, expire_date = %s
            WHERE id = %s
        """, (reset_token, expires_at, user["id"]))



        reset_link = f"https://flask-api-sigma-pied.vercel.app/reset-password/{reset_token}"

        html = f"""
        <h2>Password Reset Request</h2>
        <p>Hello {user['fullname']},</p>
        <p>We received a request to reset your password.</p>
        <p>
            <a href="{reset_link}"
               style="
                    background:#2563eb;
                    color:white;
                    padding:12px 20px;
                    text-decoration:none;
                    border-radius:6px;">
                Reset Password
            </a>
        </p>
        <p>This link will expire in <strong>30 minutes</strong>.</p>
        <p>If you didn't request a password reset, you can safely ignore this email.</p>
        <br>
        <p>Learning Platform Team</p>
        """

        send_verification_email(
            email,
            "Password Reset",
            html
        )

        return jsonify({
            "success": True,
            "message": "Password reset link sent to your email."
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:
        cursor.close()
        conn.close()


@auth_bp.route("/reset-password/<token>", methods=["POST"])
def reset_password(token):
    data = request.get_json()
    new_password = data.get("new_password")

    if not new_password:
        return jsonify({
            "success": False,
            "message": "New password is required."
        }), 400

    if new_password < 6:
        return jsonify({
            "success": False,
            "message": "Password must be at least 6 characters long."
        }), 400
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id
            FROM users
            WHERE reset_token = %s AND expire_date > NOW()
        """, (token,))

        user = cursor.fetchone()
        if not user:
            return jsonify({
                "success": False,
                "message": "Invalid or expired token."
            }), 400

        hashed_password = bcrypt.generate_password_hash(new_password).decode("utf-8")

        cursor.execute("""
            UPDATE users
            SET password = %s, reset_token = NULL, expire_date = NULL
            WHERE id = %s
        """, (hashed_password, user["id"]))

        return jsonify({
            "success": True,
            "message": "Password reset successful."
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:
        cursor.close()
        conn.close()
@auth_bp.route("/google", methods=["POST"])
def google_login():
    redirect_uri = url_for("auth.google_callback", _external=True)
    return auth.google.authorize_redirect(redirect_uri)

@auth_bp.route("/google/callback", methods=["GET"])
def google_callback():
    token = auth.google.authorize_access_token()
    user_info = auth.google.parse_id_token(token)

    email = user_info.get("email")
    fullname = user_info.get("name")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, fullname, email, role FROM users WHERE email=%s",
        (email,)
    )
    user = cursor.fetchone()

    if not user:
        # User does not exist, create a new user
        cursor.execute(
            "INSERT INTO users (fullname, email, is_verified) VALUES (%s, %s, TRUE)",
            (fullname, email)
        )
        conn.commit()
        user_id = cursor.lastrowid
        role = "user"  # Default role for new users
    else:
        user_id = user["id"]
        role = user["role"]

    access_token = create_access_token(
        identity=str(user_id),
        additional_claims={
            "role": role,
            "email": email
        }
    )

    return jsonify({
        "success": True,
        "message": "Login successful",
        "access_token": access_token,
        "user": {
            "id": user_id,
            "fullname": fullname,
            "email": email,
            "role": role
        }
    }), 200