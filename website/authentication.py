from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, site_settings, mail
from flask_login import login_user, login_required, logout_user, current_user
from itsdangerous import URLSafeTimedSerializer, BadTimeSignature
from flask_mail import Message
from flask_login import current_user, login_required

authentication = Blueprint('authentication', __name__)
s = URLSafeTimedSerializer(site_settings.SECRET_KEY)

@authentication.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('pages.cycles'))
            else:
                flash('Incorrect password, please try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template('login.html', user=current_user)

@authentication.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('pages.index'))

@authentication.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # check if user already exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already in use.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            # add user to database
            new_user = User(email=email, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()

            # send verification email
            send_verification(email)

            # login and go to dashboard
            login_user(new_user, remember=True)
            return redirect(url_for('pages.cycles'))

    return render_template('register.html', user=current_user)

@authentication.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirmation')
        user = User.query.filter_by(email=email).first()
        user.email_verified = True
        db.session.commit()
        flash('Your email was successfully verified!', category='success')
        return redirect(url_for('pages.cycles'))
    except BadTimeSignature:
        flash('This email has already been verified!', category='error')
        return redirect(url_for('pages.index'))

@authentication.route('resend_email/<email>')
def resend_email(email):
    send_verification(email)
    return redirect(url_for('pages.cycles'))

@authentication.route('settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == "POST":
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