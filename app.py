import os
from flask import Flask, request, render_template, redirect, flash, jsonify, session
from models import db, connect_db, User
from forms import RegistrationForm


DEFAULT_IMAGE_URL = "https://tinyurl.com/demo-cupcake"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'postgresql:///cupcakes')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['API_SECRET_KEY'] = 'this_is_secret'

connect_db(app)


@app.get('/')
def redirect_home():
    """Redirects to /register"""

    return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def handle_register():
    """Register user if POST, show registration form otherwise"""

    form = RegistrationForm()

    if form.validate_on_submit():

        user = User.register(
            username=form.username.data,
            password=form.password.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data
            )

        return redirect('/secret', user=user)

    else:
        return render_template('register.html', form=form)
