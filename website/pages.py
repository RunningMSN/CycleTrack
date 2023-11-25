from flask import Blueprint, render_template, flash, Markup, url_for
from flask_login import current_user
from . import db
from .models import User, School, School_Profiles_Data
from datetime import datetime, timedelta

pages = Blueprint('pages', __name__)

@pages.before_app_request
def privacy_announcement():
    if current_user.is_authenticated:
        if current_user.privacy_announce == False:
            flash(Markup('Our privacy policy has changed as of 9/9/2022. You can review our new policy <a href="https://cycletrack.org/privacy">here</a>.'), category='warning')
            current_user.privacy_announce = True
            db.session.commit()

@pages.before_app_request
def verification_required():
    if current_user.is_authenticated and current_user.email_verified == False:
        flash(Markup(f'Please verify your email address. If your email is not verified by {(current_user.create_date + timedelta(days=14)).strftime("%m/%d/%Y")}, your account will be deleted. <a href={url_for("authentication.resend_email",email=current_user.email)}>Resend verification email</a>.'), category='warning')

@pages.route('/')
def index():
    user_count = db.session.query(User.id).count()
    app_count = db.session.query(School.id).count()
    school_count = db.session.query(School).group_by(School.name).count()
    return render_template('index.html', user=current_user, user_count=user_count, school_count=school_count,
                           app_count=app_count)

@pages.route('/about')
def about():
    return render_template('about.html', user=current_user)

@pages.route('/privacy')
def privacy():
    return render_template('privacy.html', user=current_user)

@pages.route('/terms')
def terms():
    return render_template('terms.html', user=current_user)

@pages.route('/changelog')
def changelog():
    return render_template('changelog.html', user=current_user)

@pages.route('/lors')
def lors():
    usmd_schools = School_Profiles_Data.query.filter_by(md_or_do='MD', country='USA').order_by(School_Profiles_Data.school).all()
    camd_schools = School_Profiles_Data.query.filter_by(md_or_do='MD', country='CAN').order_by(School_Profiles_Data.school).all()
    do_schools = School_Profiles_Data.query.filter_by(md_or_do='DO').order_by(School_Profiles_Data.school).all()
    return render_template('lors.html', user=current_user, usmd_schools=usmd_schools, camd_schools=camd_schools, do_schools=do_schools)

@pages.route('/resources')
def resources():
    return render_template('resources.html', user=current_user)