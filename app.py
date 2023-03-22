import os
from flask import Flask, render_template, redirect, session, flash
from models import db, connect_db, User
from forms import RegistrationForm, LoginForm, OnlyCSRFForm
from werkzeug.exceptions import Unauthorized


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'postgresql:///notes')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['API_SECRET_KEY'] = 'this_is_secret'
app.config['SECRET_KEY'] = 'q348u0-952v3459pn8'
connect_db(app)


@app.get('/')
def redirect_to_register():
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


        session['username'] = user.username

        return redirect(f'/users/{user.username}')

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

            return redirect(f'/users/{user.username}')

        else:
            form.username.errors = ['Invalid username and/or password']

    return render_template('login.html', form=form)


@app.get('/users/<username>')
def show_user_page(username):
    """Shows user page if logged in, otherwise redirects with error"""
    user = User.query.get_or_404(username)

    form = OnlyCSRFForm()

    if session["username"] != user.username:
        raise Unauthorized()

    else:

        return render_template('user.html', user=user, form=form)


@app.post('/logout')
def logout_user():
    """Logs out user"""

    form = OnlyCSRFForm()

    if form.validate_on_submit():
        session.pop("username", None)

    return redirect('/')

##################################################################

@app.post('/users/<username>/delete')
def delete_user(username):
    """Deletes user notes and account entirely"""

    user = User.query.get_or_404(username)

    if session["username"] != user.username:
        raise Unauthorized()

    else:
        form = OnlyCSRFForm()
        if form.validate_on_submit():

            del user.notes
            del user
            flash(f"{user.username} deleted :(")

        return redirect('/')


@app.route("/users/<username>/notes/add", methods = ["GET", "POST"])
def add_note(username):

