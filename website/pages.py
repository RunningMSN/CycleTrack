from flask import Blueprint, render_template, request, flash
from flask_login import current_user, login_required
from . import db, site_settings
from .models import Cycle

pages = Blueprint('pages', __name__)

@pages.route('/')
def index():
    return render_template('index.html', user=current_user)

@pages.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    # Manage all requests for updating information
    if request.method == 'POST':
        add_cycle = request.form.get('add_cycle')
        db.session.add(Cycle(cycle_year=int(add_cycle), user_id=current_user.id))
        db.session.commit()
        flash('Cycle added.', category='success')
    return render_template('dashboard.html', user=current_user, cycles=site_settings.VALID_CYCLES)