# This file creates the database models

# . imports from the current package (website, namely __init__.py)
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    # id column is filled automatically (incrementally)
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    index = db.Column(db.Integer, default=func.now())
    # using 'default' fills this column automatically

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # 'one to many' - one user has many notes
    # user.id connects to id field in the User model (note case change)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

    notes = db.relationship('Note')
    # Stores all notes as a list for each user

    # UserMixin allows us to flask_login.current_user in auth.py
    # to access information about the currently logged in user