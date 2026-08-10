import os
from dotenv import load_dotenv

load_dotenv()
class Config:
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    SECRET_KEY = os.getenv("MYSECRET_KEY")
    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT"))
    MYSQL_USER= os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
    DB_SSL_CERTIFICATE = {"ca": os.getenv("DB_SSL_CERT")}
    BREVO_API_KEY = os.getenv("BREVO_API_KEY")
    MAIL_FROM = os.getenv("MAIL_FROM")
    MAIL_FROM_TITLE = os.getenv("MAIL_FROM_TITLE")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    MY_SECRET_KEY = os.getenv("MY_SECRET_KEY")

    MAIL_SERVER = os.getenv("MAIL_SERVER")
    # MAIL_PORT = int(os.getenv("MAIL_PORT"))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
    MAIL_PORT = int(os.getenv("MAIL_PORT"))
    # RESEND_API_KEY = os.getenv("RESEND_API_KEY")