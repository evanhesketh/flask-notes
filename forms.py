from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, EmailField
from wtforms.validators import InputRequired, Email, Length

class RegistrationForm(FlaskForm):
    """Form for new user registration"""

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(max=20)])

    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(max=100)])

    email = EmailField(
        "Email",
        validators=[InputRequired(), Email(), Length(max=50)])

    first_name = StringField(
        "First name",
        validators= [InputRequired(), Length(max=30)])

    last_name = StringField(
        "Last name",
        validators= [InputRequired(), Length(max=30)])

class LoginForm(FlaskForm):
    """Login form"""

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(max=20)])

    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(max=100)])