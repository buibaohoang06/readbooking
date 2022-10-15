from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from app import app

db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), nullable=False, primary_key=True, unique=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    hashed_password = db.Column(db.String(), nullable=False, unique=False)
    balance = db.Column(db.Integer(), nullable=False, unique=False, default=0)
    email = db.Column(db.String(), nullable=False, unique=True)
    userid = db.Column(db.String(), nullable=False, unique=True)
    is_admin = db.Column(db.Boolean(), nullable=False, unique=False, default=True)

class Post(db.Model):
    id = db.Column(db.Integer(), nullable=False, primary_key=True, unique=True)
    uuid = db.Column(db.String(), nullable=False, unique=True)
    author = db.Column(db.String(), nullable=False, unique=False)
    link = db.Column(db.String(), nullable=False, unique=True)
    title = db.Column(db.String(), nullable=False, unique=False)
    description = db.Column(db.String(), nullable=False, unique=False)
    content = db.Column(db.Text(), nullable=False, unique=False)
    image = db.Column(db.String(), nullable=False, unique=False)
    time = db.Column(db.DateTime(), nullable=False, unique=False)
