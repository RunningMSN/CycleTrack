from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    cycles = db.relationship('Cycle')
    email_verified = db.Column(db.Boolean, default=False)

class Cycle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cycle_year = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    schools = db.relationship('School')
    gender = db.Column(db.String(150), nullable=True)
    sex = db.Column(db.String(150), nullable=True)
    birth_month = db.Column(db.Integer, nullable=True)
    birth_year = db.Column(db.Integer, nullable=True)
    race_ethnicity = db.Column(db.String(150), nullable=True)
    home_state = db.Column(db.String(150), nullable=True)
    cgpa = db.Column(db.Float, nullable=True)
    sgpa = db.Column(db.Float, nullable=True)
    mcat_total = db.Column(db.Integer, nullable=True)
    mcat_cp = db.Column(db.Integer, nullable=True)
    mcat_cars = db.Column(db.Integer, nullable=True)
    mcat_bb = db.Column(db.Integer, nullable=True)
    mcat_ps = db.Column(db.Integer, nullable=True)

class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cycle_id = db.Column(db.Integer, db.ForeignKey('cycle.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(150))
    school_type = db.Column(db.String(150)) # MD/DO
    phd = db.Column(db.Boolean) # Dual degree w/ PhD or not
    primary = db.Column(db.DateTime(timezone=True), nullable=True)
    secondary_received = db.Column(db.DateTime(timezone=True), nullable=True)
    application_complete = db.Column(db.DateTime(timezone=True), nullable=True)
    interview_received = db.Column(db.DateTime(timezone=True), nullable=True)
    interview_date = db.Column(db.DateTime(timezone=True), nullable=True)
    rejection = db.Column(db.DateTime(timezone=True), nullable=True)
    waitlist = db.Column(db.DateTime(timezone=True), nullable=True)
    acceptance = db.Column(db.DateTime(timezone=True), nullable=True)
    withdrawn = db.Column(db.DateTime(timezone=True), nullable=True)
    note = db.Column(db.Text(), nullable=True)

class School_Profiles_Data(db.Model):
    school = db.Column(db.String(150), primary_key=True)
    city = db.Column(db.String(150))
    state = db.Column(db.String(150))
    country = db.Column(db.String(150))
    envt_type = db.Column(db.String(150))
    private_public = db.Column(db.String(150))
    lat = db.Column(db.Float)
    long = db.Column(db.Float)
    md_or_do = db.Column(db.String(150))
    logo_file_name = db.Column(db.String(150))
    reg_apps_count = db.Column(db.Integer())
    phd_apps_count = db.Column(db.Integer())