from extensions import db
from flask_login import UserMixin

# create User Table in database


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String(100), nullable=False)
    last = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)
