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
    schools = db.relationship('School')

class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cycle = db.Column(db.Integer, db.ForeignKey('cycle.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    primary = db.Column(db.DateTime(timezone=True), nullable=True)
    secondary_received = db.Column(db.DateTime(timezone=True), nullable=True)
    application_complete = db.Column(db.DateTime(timezone=True), nullable=True)
    interview_received = db.Column(db.DateTime(timezone=True), nullable=True)
    interview_date = db.Column(db.DateTime(timezone=True), nullable=True)
    rejection = db.Column(db.DateTime(timezone=True), nullable=True)
    waitlist = db.Column(db.DateTime(timezone=True), nullable=True)
    acceptance = db.Column(db.DateTime(timezone=True), nullable=True)
