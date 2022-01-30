from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import current_user, login_required
from . import db, form_options
from .models import User,Cycle, School
import json
from datetime import datetime

pages = Blueprint('pages', __name__)

@pages.route('/')
def index():
    user_count = db.session.query(User.id).count()
    app_count = db.session.query(School.id).count()
    return render_template('index.html', user=current_user, user_count=user_count, app_count=app_count)

@pages.route('/explorer')
def explorer():
    return render_template('explorer.html', user=current_user)

@pages.route('/cycles', methods=['GET', 'POST'])
@login_required
def cycles():
    # Manage all requests for updating information
    if request.method == 'POST':
        # Adding cycle
        add_cycle = request.form.get('add_cycle')
        if add_cycle:
            # Check if added cycle already exists
            cycle = Cycle.query.filter_by(cycle_year=int(add_cycle), user_id=current_user.id).first()
            if cycle:
                flash('You already have this cycle added.', category='error')
            else:
                db.session.add(Cycle(cycle_year=int(add_cycle), user_id=current_user.id))
                db.session.commit()
    return render_template('cycles.html', user=current_user, cycle_options=form_options.VALID_CYCLES,
                           sex_options=form_options.SEX_OPTIONS, gender_options=form_options.GENDER_OPTIONS,
                           race_ethnicity_options=form_options.RACE_ETHNICITY_OPTIONS,
                           state_options=form_options.STATE_OPTIONS)

@pages.route('/lists', methods=['GET','POST'])
@login_required
def lists():
    # If GET request then did not provide a school
    if request.method == 'GET':
        if len(current_user.cycles) > 1:
            flash('Please select a cycle before viewing your school list.', category='error')
            return redirect(url_for('pages.cycles'))
        elif len(current_user.cycles) == 0:
            flash('Please add a cycle first.', category='error')
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

    # Handle editing schools
    school_id = request.form.get('school_id')
    if school_id:
        school = School.query.filter_by(id=int(school_id)).first()
        primary = request.form.get('primary')
        if primary:
            school.primary = datetime.strptime(primary, '%Y-%m-%d')
        else:
            school.primary = None
        secondary_received = request.form.get('secondary_received')
        if secondary_received:
            school.secondary_received = datetime.strptime(secondary_received, '%Y-%m-%d')
        else:
            school.secondary_received = None
        application_complete = request.form.get('application_complete')
        if application_complete:
            school.application_complete = datetime.strptime(application_complete, '%Y-%m-%d')
        else:
            school.application_complete = None
        interview_received = request.form.get('interview_received')
        if interview_received:
            school.interview_received = datetime.strptime(interview_received, '%Y-%m-%d')
        else:
            school.interview_received = None
        interview_date = request.form.get('interview_date')
        if interview_date:
            school.interview_date = datetime.strptime(interview_date, '%Y-%m-%d')
        else:
            school.interview_date = None
        rejection = request.form.get('rejection')
        if rejection:
            school.rejection = datetime.strptime(rejection, '%Y-%m-%d')
        else:
            school.rejection = None
        waitlist = request.form.get('waitlist')
        if waitlist:
            school.waitlist = datetime.strptime(waitlist, '%Y-%m-%d')
        else:
            school.waitlist = None
        acceptance = request.form.get('acceptance')
        if acceptance:
            school.acceptance = datetime.strptime(acceptance, '%Y-%m-%d')
        else:
            school.acceptance = None
        withdrawn = request.form.get('withdrawn')
        if withdrawn:
            school.withdrawn = datetime.strptime(withdrawn, '%Y-%m-%d')
        else:
            school.withdrawn = None
        db.session.commit()

    return render_template('lists.html', user=current_user, cycle=cycle, school_list=form_options.SCHOOL_LIST)

@pages.route('/visualizations')
@login_required
def visualizations():
    return render_template('visualizations.html', user=current_user)

@pages.route('/privacy')
def privacy():
    return render_template('privacy.html', user=current_user)

@pages.route('/delete-cycle', methods=['POST'])
def delete_cycle():
    cycle = json.loads(request.data)
    cycleId = cycle['cycleId']
    cycle = Cycle.query.get(cycleId)
    if cycle:
        if cycle.user_id == current_user.id:
            for school in cycle.schools:
                db.session.delete(school)
            db.session.delete(cycle)
            db.session.commit()
            return jsonify({})

@pages.route('/delete-school', methods=['POST'])
def delete_school():
    school = json.loads(request.data)
    schoolId = school['schoolId']
    school = School.query.get(schoolId)
    if school:
        if school.user_id == current_user.id:
            db.session.delete(school)
            db.session.commit()
            return jsonify({})