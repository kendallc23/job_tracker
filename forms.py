from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, DataRequired, EqualTo
from models import User

# create Registration Form


class RegisterForm(FlaskForm):
    # first - string between 1 and 100 chars, required field
    first = StringField(validators=[InputRequired(), Length(
        min=1, max=100)], render_kw={"placeholder": "first name"})

    # last - string between 1 and 100 chars, required field
    last = StringField(validators=[InputRequired(), Length(
        min=1, max=100)], render_kw={"placeholder": "last name"})

    # email - string between 6 and 100 chars, required field
    email = StringField(validators=[InputRequired(), Length(
        min=6, max=100)], render_kw={"placeholder": "email address"})

    # username - string between 4 and 20 chars, required field
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "username"})

    # password - string between 4 and 20 chars, required field
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "password"})

    # role - string (admin or user), required field
    role = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "user or admin"})

    # submit button
    submit = SubmitField("Register Account")

    # validate unique username
    def validate_username(self, username):
        existing_username = User.query.filter_by(
            username=username.data).first()
        if existing_username:
            raise ValidationError(
                "That username already exists. Please select a different one.")

# create Login Form


class LoginForm(FlaskForm):
    # username - string between 4 and 20 chars, required field
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "username"})

    # password - string between 4 and 20 chars, required field
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "password"})

    # submit button
    submit = SubmitField("Login")


# create password reset forms
class PasswordResetRequestForm(FlaskForm):
    # email - string between 6 and 100 chars, required field
    email = StringField(validators=[InputRequired(), Length(
        min=6, max=100)], render_kw={"placeholder": "email address"})

    # submit button
    submit = SubmitField("Send Reset Link")


class PasswordResetForm(FlaskForm):
    # enter new passwords
    password = PasswordField("New Password", validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "new password"})

    password2 = PasswordField("Repeat Password", validators=[InputRequired(
    ), EqualTo("password")], render_kw={"placeholder": "new password"})

    # submit button
    submit = SubmitField("Confirm Password Reset")
