from datetime import datetime

from flask import Blueprint, request, jsonify
from email_validator import validate_email, EmailNotValidError
from extension import bcrypt
from db import get_connection
import secrets
from email_service import send_verification_email
from flask_jwt_extended import create_access_token


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
            "message": "Email is required"
        }), 400

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, fullname, email FROM users WHERE email=%s",
            (email,)
        )
        user = cursor.fetchone()

        if not user:
            return jsonify({
                "success": False,
                "message": "Email not found"
            }), 404

        # Generate a password reset token (you can use a library like `secrets` for this)
        reset_token = create_access_token(identity=str(user["id"]), expires_delta=datetime.timedelta(minutes=30))

        # Store the reset token in the database
        cursor.execute(
            "UPDATE users SET password_reset_token=%s WHERE id=%s",
            (reset_token, user["id"])
        )
        conn.commit()

        # Send the password reset email
        reset_link = f"https://flask-api-chqu.onrender.com/api/auth/reset-password/{reset_token}"
        subject = "Reset Your Password"
        html = f"<h2>Reset Your Password</h2><p>Please click the link below to reset your password:</p><p><a href=\"{reset_link}\">Reset Password</a></p>"

        send_verification_email(email, subject, html)

        return jsonify({
            "success": True,
            "message": "Password reset instructions sent to your email."
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

    finally:
        cursor.close()
        conn.close()