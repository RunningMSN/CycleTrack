from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import current_user, login_required
from . import db, site_settings
from .models import Cycle, School
import json

pages = Blueprint('pages', __name__)

@pages.route('/')
def index():
    return render_template('index.html', user=current_user)

@pages.route('/cycles', methods=['GET', 'POST'])
@login_required
def cycles():
    # Manage all requests for updating information
    if request.method == 'POST':
        add_cycle = request.form.get('add_cycle')
        # Check if added cycle already exists
        cycle = Cycle.query.filter_by(cycle_year=int(add_cycle), user_id=current_user.id).first()
        if cycle:
            flash('You already have this cycle added.', category='error')
        else:
            db.session.add(Cycle(cycle_year=int(add_cycle), user_id=current_user.id))
            db.session.commit()
    return render_template('cycles.html', user=current_user, cycle_options=site_settings.VALID_CYCLES)

@pages.route('/lists', methods=['GET','POST'])
@login_required
def lists():
    # If GET request then did not provide a school
    if request.method == 'GET':
        if len(current_user.cycles) > 1:
            flash('Please select a cycle before viewing your school list.', category='error')
            return redirect(url_for('pages.cycles'))
        elif len(current_user.cycles) == 0:
            flash('Please add a cycle first..', category='error')
            return redirect(url_for('pages.cycles'))
        else:
            cycle_id = current_user.cycles[0].id
    # If POST then grab cycle ID
    else:
        cycle_id = request.form.get('cycle_id')

    # Require to provide a cycle for obtaining school list for that cycle
    cycle = Cycle.query.filter_by(id=int(cycle_id)).first()

    # Handle adding school
    add_school_name = request.form.get('add_school')
    if add_school_name:
        school = School.query.filter_by(name=add_school_name, cycle_id=cycle.id, ).first()

        if school:
            flash('You cannot add a school twice.', category='error')
        else:
            db.session.add(School(name=add_school_name, cycle_id=cycle.id, user_id=current_user.id))
            db.session.commit()

    return render_template('lists.html', user=current_user, cycle=cycle, school_list=site_settings.SCHOOL_LIST)

@pages.route('/visualizations')
@login_required
def visualizations():
    return render_template('visualizations.html', user=current_user)

@pages.route('/delete-cycle', methods=['POST'])
def delete_cycle():
    cycle = json.loads(request.data)
    cycleId = cycle['cycleId']
    cycle = Cycle.query.get(cycleId)
    if cycle:
        if cycle.user_id == current_user.id:
            db.session.delete(cycle)
            db.session.commit()
            return jsonify({})