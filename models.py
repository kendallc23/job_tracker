from extensions import db
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from flask import current_app

# create User Table in database


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String(100), nullable=False)
    last = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)

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
