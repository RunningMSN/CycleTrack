import itsdangerous
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, User_Profiles
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, site_settings, mail
from flask_login import login_user, logout_user
from itsdangerous import URLSafeTimedSerializer, BadTimeSignature
from flask_mail import Message
from flask_login import current_user, login_required
from datetime import datetime

authentication = Blueprint('authentication', __name__)
s = URLSafeTimedSerializer(site_settings.SECRET_KEY)

@authentication.before_app_request
def last_visit():
    if current_user.is_authenticated:
        current_user.last_visited = datetime.now()
        db.session.commit()

@authentication.route('/login', methods=['GET', 'POST'])
def login():
    # If user already logged in, redirect
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.cycles'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('dashboard.cycles'))
            else:
                flash('Incorrect password, please try again.', category='error')
        else:
            flash('No accounts with this email were found.', category='error')

    return render_template('login.html', user=current_user)

@authentication.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('pages.index'))

@authentication.route('/register', methods=['GET', 'POST'])
def register():
    # If user already logged in, redirect
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.cycles'))

    if request.method == 'POST':
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        terms_response = request.form.get('terms_agree')
        # check if user already exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already in use.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif not password_meets_criteria(password1, password2):
            pass
        # Check that agreed to privacy/terms
        elif not terms_response == 'agree':
            flash('You must agree to the privacy policy and terms and conditions to register.', category='error')
        else:
            # add user to database
            now = datetime.now()
            new_user = User(email=email, password=generate_password_hash(password1, method='sha256'),create_date=now,
                            privacy_announce=True)
            db.session.add(new_user)
            db.session.commit()

            # send verification email
            send_verification(email)

            # login and go to dashboard
            login_user(new_user, remember=True)
            return redirect(url_for('dashboard.cycles'))

    return render_template('register.html', user=current_user)

@authentication.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirmation')
        user = User.query.filter_by(email=email).first()
        user.email_verified = True
        db.session.commit()
        flash('Your email was successfully verified!', category='success')
        return redirect(url_for('dashboard.cycles'))
    except BadTimeSignature:
        flash('This email has already been verified!', category='error')
        return redirect(url_for('pages.index'))

@authentication.route('/resend_email/<email>')
def resend_email(email):
    send_verification(email)
    return redirect(url_for('dashboard.cycles'))

@authentication.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == "POST":
        flash('If your email is registered, you will receive an email from us shortly.', category='success')
        email = request.form.get('email')
        if User.query.filter_by(email=email).first():
            if '%40' in email:
                email = email.replace('%40', '@')
            token = s.dumps(email, salt='reset-password')
            verification_email = Message('Reset CycleTrack Password', sender=('CycleTrack', 'CycleTrack@docs2be.org'),
                                         recipients=[email])
            link = url_for('authentication.reset_password', token=token, _external=True)
            verification_email.body = f'You are receiving this email because you requested to reset your password on CycleTrack. Please click the following link to reset your password. This will expire in 15 minutes.\n\nReset Password: {link}\n\nIf you did not request this email, please ignore it.'
            mail.send(verification_email)
    return render_template('forgot_password.html', user=current_user)

@authentication.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if request.method == "POST":
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password_meets_criteria(password, confirm_password):
            try:
                email = s.loads(token, salt='reset-password', max_age=900)
                user = User.query.filter_by(email=email).first()
                user.password = generate_password_hash(password, method='sha256')
                db.session.commit()
                login_user(user, remember=True)
                return redirect(url_for('dashboard.cycles'))
            except itsdangerous.SignatureExpired:
                flash('Your password reset request has expired. Please request another link.', category='error')
                return redirect(url_for('authentication.forgot_password'))
            except Exception as e:
                flash('We encountered an error resetting your password. Please try again.', category='error')
                return redirect(url_for('authentication.forgot_password'))

    try:
        email = s.loads(token, salt='reset-password', max_age=900)
        return render_template('change_password.html', user=current_user)
    except itsdangerous.SignatureExpired:
        flash('Your password reset request has expired. Please request another link.', category='error')
        return redirect(url_for('authentication.forgot_password'))
    except Exception as e:
        flash('We encountered an error resetting your password. Please try again.', category='error')
        return redirect(url_for('authentication.forgot_password'))

@authentication.route('settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == "POST":
        # Start with any account deletion
        if request.form.get('del_password'):
            # Check for correct password
            if not check_password_hash(current_user.password, request.form.get('del_password')):
                flash('You did not enter your current password correctly. Please try again.', category='error')
                return redirect(url_for('authentication.settings'))
            else:
                # Delete all user info
                for cycle in current_user.cycles:
                    for school in cycle.schools:
                        db.session.delete(school)
                    db.session.delete(cycle)
                for profile_item in User_Profiles.query.filter_by(user_id=current_user.id).all():
                    db.session.delete(profile_item)
                db.session.delete(current_user)
                db.session.commit()
                logout_user()
                flash('Your account was successfully deleted.', category='success')
                return redirect(url_for('pages.index'))
        # Grab form input
        new_email = request.form.get('email')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('new_password_confirm')
        current_password = request.form.get('current_password')

        # Check password, if it is correct, proceed to making changes
        if current_password:
            if not check_password_hash(current_user.password, current_password):
                flash('You did not enter your current password correctly. Please try again.', category='error')
                return redirect(url_for('authentication.settings'))
        else:
            flash('You did not enter your current password correctly. Please try again.', category='error')
            return redirect(url_for('authentication.settings'))

        flash_updates_messages = []
        if new_email:
            if new_email != current_user.email:
                # Check if email already exists
                check_email_user = User.query.filter_by(email=new_email).first()
                if check_email_user:
                    flash('Sorry, that email is already registered in our system.')
                    return redirect(url_for('authentication.settings'))
                else:
                    current_user.email = new_email
                    flash_updates_messages.append("Email")
        if new_password and confirm_password:
            if new_password == confirm_password:
                current_user.password = generate_password_hash(new_password, method='sha256')
                flash_updates_messages.append("Password")
        db.session.commit()
        flash(f'{(", ").join(flash_updates_messages)} updated successfully!', category='success')
    return render_template('settings.html', user=current_user)

def send_verification(email):
    if '%40' in email:
        email = email.replace('%40', '@')
    token = s.dumps(email, salt='email-confirmation')
    verification_email = Message('Confirm CycleTrack Email', sender=('CycleTrack', 'CycleTrack@docs2be.org'), recipients=[email])
    link = url_for('authentication.confirm_email', token=token, _external=True)
    verification_email.body = f'Hi! You are receiving this email because you recently registered or changed your email address on CycleTrack. Please click the following verification link to confirm your email address.\n\nYour verification link is: {link}\n\nIf you did not request this email, you may ignore it.'
    mail.send(verification_email)

def password_meets_criteria(password, confirm_password):
    if password != confirm_password:
        flash("Passwords did not match.", category='error')
        return False
    elif len(password) < 7:
        flash("Password must be at least 7 characters.", category='error')
        return False
    return True