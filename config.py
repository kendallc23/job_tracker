import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")

    # Security
    SECRET_KEY = os.environ.get("SECRET_KEY")
    # print("SECRET_KEY loaded:", "YES" if os.environ.get("SECRET_KEY") else "NO")

    # Email -> see docs: https://waynerv.github.io/flask-mailman/
    MAIL_SERVER = 'smtp.gmail.com'
    # set to local host by default; will likely need to change to a company server
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "True").lower() in [
        "true", "1", "yes"]
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    # will need to change to company email
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

    # Password Reset
    RESET_PASS_TOKEN_MAX_AGE = int(os.environ.get("RESET_PASS_TOKEN_MAX_AGE"))
