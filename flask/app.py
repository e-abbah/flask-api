from flask import Flask, config, render_template 
from extension import (bcrypt, mail, jwt, oauth)
from auth.auth import auth_bp
from config import Config
from flask_cors import CORS


app = Flask(__name__)
app.secret_key = Config.SECRET_KEY
app.config.from_object(Config)


bcrypt.init_app(app)
mail.init_app(app)
jwt.init_app(app)
oauth.init_app(app)


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

app.register_blueprint(auth_bp, url_prefix="/api/auth")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)