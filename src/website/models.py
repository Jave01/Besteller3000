from . import db
from flask_login import UserMixin


class Level:
    ADMIN = 0
    SYSADMIN = 1
    USER = 2
    GUEST = 3


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    secure_name = db.Column(db.String(150))
    user_role = db.Column(db.Integer)
    max_members = db.Column(db.Integer)
    password = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    data = db.Column(db.JSON)


class Template(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    data = db.Column(db.JSON)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(150))
    access_lvl = db.Column(db.Integer)
    email = db.Column(db.String(150))   # not used yet
    personal_folder = db.Column(db.String(500))
    personal_information = db.Column(db.JSON)
    # one to many relationship
    templates = db.relationship('Template', backref='user', lazy=True)
    groups = db.relationship('Group', backref="user", lazy=True)
