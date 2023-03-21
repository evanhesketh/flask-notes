import os
from flask import Flask, request, render_template, redirect, flash, jsonify, session
from models import db, connect_db, User
from forms import RegistrationForm, LoginForm


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'postgresql:///notes')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['API_SECRET_KEY'] = 'this_is_secret'
app.config['SECRET_KEY'] = 'q348u0-952v3459pn8'
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

        db.session.add(user)
        db.session.commit()

        return redirect('/secret')

    else:
        return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def handle_login():
    """Login a user if POST, show login form otherwise"""

    form = LoginForm()

    if form.validate_on_submit():

        user = User.authenticate(
            username=form.username.data,
            password=form.password.data
        )

        if user:
            session['username'] = user.username

            return redirect('/secret')

        else:
            form.username.errors =  ['Invalid username and/or password']

    else:
        return render_template('login.html', form=form)

@app.get('/secret')
def secret():

    return render_template('secret.html')