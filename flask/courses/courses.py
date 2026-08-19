from flask import Blueprint, jsonify, request
from slugify import slugify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import get_connection

courses_bp = Blueprint("courses", __name__)

@courses_bp.route("/", methods=["GET"])
def home():
    return "<p>Welcome to Flask</p>"


# @courses_bp.route("/courses", methods=["GET"])
# def get_courses():
#     return "<p>Welcome to course endpoint</p>"

@courses_bp("/course", methods=["POST"])
@jwt_required
def course():

    data = request.get_json()

    title = data.get('title')
    price = data.get('price', 0)
    currency = data.get('currency', 'NGN')
    free_count = data.get('free_count', 1)
    slug = slugify(title)
    
    if not title:
        return jsonify({"success": False, "message":"Course title must be proovided"}), 400
    if not currency:
        return jsonify({"success": False, "message":"Currency must be proovided"}), 400
    if price <= 0:
        return jsonify({"success": False, "message":"Price must be greater than"}), 400
    
    # if free_count 
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE id = %s", (get_jwt_identity()))
    except Exception as e:
        return jsonify({"error": e})
    print(data)
    return jsonify({"message": "Welcome to courses"})