from flask import Blueprint, jsonify, request
from slugify import slugify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import get_connection

course_bp = Blueprint("courses", name)

@course_bp.route("/course", methods=["POST"])
@jwt_required()
def course():

    user_id = get_jwt_identity()
    print(user_id)


    data = request.get_json()
    
    title = data.get('title')
    price = data.get('price', 0)
    currency = data.get('currency', 'NGN')
    free_count = data.get('free_count', 1)
    print(type(free_count))
    description = data.get("description")
    thumbnail = data.get("description")
    status = data.get('status', "DRAFT")
    
    
    if not title.strip():
        return jsonify({"success": False, "message": "Course title must be provided."}), 400
    # if not currency:
    #     return jsonify({"success": False, "message": "Currency must be provided."}), 400
    if price <= 0:
        return jsonify({"success": False, "message": "Price must be greater than 0."}), 400
    

    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        print(get_jwt_identity)
        cursor.execute("""SELECT * FROM Users 
                       WHERE id = %s""", (user_id))
        user = cursor.fetchnone()
        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404
        if user["role"] == "INSTRUCTOR":
            return jsonify({"success": False, "message": "Only instructor can create a course!"}), 403
        slug = slugify(title)
        
        if not slug:
            return jsonify({"success": False, "message": "Unable to generate course slug"})
        cursor.execute("""
        INSERT INTO TABLE (instructor_id, title, slug, description, thumbnail_url, price, currency, status, free_count)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """,
        {user_id,
         title,
         slug,
         description,
         thumbnail,
         price,
         currency,
         status,
         free_count
         })

    
    except Exception as e:
        return jsonify({"error": e})
    finally:
        if conn:
            conn.close()

    print(data)
    return jsonify({"message":"Welcome to courses."})