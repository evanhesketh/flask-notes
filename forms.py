from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, Email, Length, ValidationError
from models import User

# custom validators for unique username and unique email


def validate_username(self, field):
    if User.query.filter_by(username=field.data).first():
        raise ValidationError('Username already in use')


def validate_email(self, field):
    if User.query.filter_by(email=field.data).first():
        raise ValidationError('Email already in use')


class RegistrationForm(FlaskForm):
    """Form for new user registration"""

    username = StringField(
        "Username",
        validators=[
            InputRequired(),
            Length(max=20),
            validate_username
        ]
    )

    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(max=100)]
    )

    email = EmailField(
        "Email",
        validators=[InputRequired(),
                    Email(),
                    Length(max=50),
                    validate_email])

    first_name = StringField(
        "First name",
        validators=[InputRequired(), Length(max=30)])

    last_name = StringField(
        "Last name",
        validators=[InputRequired(), Length(max=30)])


class LoginForm(FlaskForm):
    """Login form"""

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(max=20)])

    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(max=100)])


class OnlyCSRFForm(FlaskForm):
    """Form just to add CSRF Protection"""
