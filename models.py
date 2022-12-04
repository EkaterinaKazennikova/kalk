# models.py

from flask_login import UserMixin
from sqlalchemy import ForeignKey

from . import db


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    parameters = db.relationship('Parameters', backref='author', lazy='dynamic')


class Parameters(db.Model):
    __tablename__ = "parameters"
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey("user.id"))


class Nutrition(db.Model):
    __tablename__ = "nutrition"
    id = db.Column(db.Integer, primary_key=True)
    food = db.Column(db.String, nullable=False)
    water = db.Column(db.Integer, nullable=False)
    workout = db.Column(db.String, nullable=False)
