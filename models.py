from extensions import db
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from flask import current_app
import datetime

# create User Table in database


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String(100), nullable=False)
    last = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), default="user", nullable=False)

    def generate_password_token(self):
        serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        return serializer.dumps(self.email, salt=self.password)

    @staticmethod
    def validate_reset_pass_token(token, user_id):
        # check if user with this id exists
        user = db.session.get(User, user_id)
        if user is None:
            return None

        # check validity of token
        serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        try:
            token_user_email = serializer.loads(
                token,
                max_age=current_app.config["RESET_PASS_TOKEN_MAX_AGE"],
                salt=user.password

            )
        except (BadSignature, SignatureExpired):
            return None

        # check that email corresponding to token matches the user's email in the database
        if token_user_email != user.email:
            return None

        return user


# Create Parts Table -> allow admins to add new parts with their surface area
    # Can you store images in sql databases ? Maybe a link to an image that can be rendered in html?
class Part(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    part_name = db.Column(db.String(50), nullable=False)
    surface_area = db.Column(db.Float, nullable=False)


# Create Jobs Table
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    part_id = db.Column(db.Integer, nullable=False)
    part_name = db.Column(db.String(50), nullable=False)
    num_batches = db.Column(db.Integer, nullable=False)
    num_per_batch = db.Column(db.Integer, nullable=False)
    task = db.Column(db.String(50), nullable=False)
    paint_type = db.Column(db.String(50))
    # store seconds for analysis
    total_time = db.Column(db.Float, nullable=False)
    avg_time_per_batch = db.Column(db.Float, nullable=False)
    avg_time_per_part = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    # connect user table and job table
    user = db.relationship('User', backref='jobs')
