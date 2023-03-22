from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()
#TODO: reorder

def connect_db(app):
    """Connect this database to provided Flask app."""

    app.app_context().push()
    db.app = app
    db.init_app(app)


class User(db.Model):
    """Model for a user."""

    __tablename__ = 'users'

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register user w/ hashed password and return user"""

        hashed = bcrypt.generate_password_hash(password).decode('utf8')
        return cls(
            username=username,
            password=hashed,
            email=email,
            first_name=first_name,
            last_name=last_name,

            )

    @classmethod
    def authenticate(cls, username, password):
        """Validate username and password
        Return user if valid; else return False.
        """

        user = cls.query.filter_by(username=username).one_or_none()

        if user and bcrypt.check_password_hash(user.password, password):
            return user

        else:
            return False


    username = db.Column(
        db.String(20),
        primary_key=True
    )

    password = db.Column(
        db.Text,
        nullable=False
    )

    email = db.Column(
        db.String(50),
        nullable=False,
        unique=True
    )

    first_name = db.Column(
        db.String(30),
        nullable=False
    )

    last_name = db.Column(
        db.String(30),
        nullable=False
    )

    def __repr__(self):
        return f'<username = {self.username}>'


class Note(db.Model):
    """Model for a note."""

    __tablename__ = 'notes'

    id = db.Column(
        db.Integer,
        autoincrement=True,
        primary_key=True
    )

    title = db.Column(
        db.String(100),
        nullable=False
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    owner = db.Column(
        db.String(20),
        db.ForeignKey('users.username')
    )

    user = db.relationship('User', backref='notes')