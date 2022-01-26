from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    cycles = db.relationship('Cycle')

class Cycle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cycle_year = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
