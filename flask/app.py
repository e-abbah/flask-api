from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from extension import bcrypt, mail, jwt, oauth
from auth.auth import auth_bp
from courses.courses import courses_bp
from config import Config
from flask_cors import CORS


app = Flask(__name__)

# Trust the proxy headers sent by Render.
# This allows Flask to correctly detect HTTPS in production.
app.wsgi_app = ProxyFix(
    app.wsgi_app,
    x_proto=1,
    x_host=1
)

app.secret_key = Config.SECRET_KEY
app.config.from_object(Config)


# Initialize extensions
bcrypt.init_app(app)
mail.init_app(app)
jwt.init_app(app)
oauth.init_app(app)


# CORS configuration
CORS(
    app,
    origins=[
        "http://localhost:5173",
        "https://flask-api-sigma-pied.vercel.app"
    ],
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    supports_credentials=True
)


# Register authentication routes
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(courses_bp, url_prefix="/")


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )