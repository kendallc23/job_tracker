from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# create database instace
db = SQLAlchemy()

# password hashing
bcrypt = Bcrypt()

# handle login/logout functionality
login_manager = LoginManager()
