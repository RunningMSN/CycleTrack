from flask import Blueprint, render_template, request, flash
from flask_login import current_user, login_required
from . import db

pages = Blueprint('pages', __name__)

@pages.route('/')
def index():
    return render_template('index.html', user=current_user)

@pages.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)