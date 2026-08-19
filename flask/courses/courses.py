from flask import Blueprint

courses_bp = Blueprint("courses", __name__)

@courses_bp.route("/", methods=["GET"])
def home():
    return "<p>Welcome to Flask</p>"


@courses_bp.route("/courses", methods=["GET"])
def get_courses():
    return "<p>Welcome to course endpoint</p>"