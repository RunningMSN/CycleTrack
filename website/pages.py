from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import current_user, login_required
from . import db, form_options
from .models import User,Cycle, School
import json
from datetime import datetime, date
import re
from .visualizations import dot, line
import pandas as pd

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
        # Handle editing cycle profile
        cycle_id = request.form.get('cycle_id_edit')
        if cycle_id:
            cycle = Cycle.query.filter_by(id=int(cycle_id)).first()
            gender = request.form.get('gender')
            if len(gender) > 0 and gender in form_options.GENDER_OPTIONS:
                cycle.gender = gender
            else:
                cycle.gender = None
            sex = request.form.get('sex')
            if len(sex) > 0 and sex in form_options.SEX_OPTIONS:
                cycle.sex = sex
            else:
                cycle.sex = None
            birth = request.form.get('birth_month_year')
            if birth:
                # Check that formatting is generally right
                base_format="(?P<month>[0-9]{2})/(?P<year>[0-9]{4})"
                if re.match(base_format, birth):
                    month = int(re.search(base_format, birth).group('month'))
                    year = int(re.search(base_format, birth).group('year'))
                    # Make sure input is valid
                    if month >= 1 and month <= 12 and year >= (date.today().year - 60) and year <= date.today().year - 17:
                        cycle.birth_month = month
                        cycle.birth_year = year
                    else:
                        flash('Please enter a valid birth month and year in the form "MM/YYYY"', category='error')
                else:
                    flash('Please enter a valid birth month and year in the form "MM/YYYY"', category='error')
            else:
                cycle.birth_month = None
                cycle.birth_year = None
            race_ethnicity = request.form.get('race_ethnicity')
            if len(race_ethnicity) > 0 and race_ethnicity in form_options.RACE_ETHNICITY_OPTIONS:
                cycle.race_ethnicity = race_ethnicity
            else:
                cycle.race_ethnicity = None
            home_state = request.form.get('home_state')
            if len(home_state) > 0 and home_state in form_options.STATE_OPTIONS:
                cycle.home_state = home_state
            else:
                cycle.home_state = None
            cgpa = request.form.get('cgpa')
            if cgpa:
                if float(cgpa) > 0 and float(cgpa) <= 4:
                    cycle.cgpa = float(cgpa)
                else:
                    flash('Please make sure you enter a cGPA between 0 and 4.', category='error')
            else:
                cycle.cgpa = None
            sgpa = request.form.get('sgpa')
            if sgpa:
                if float(sgpa) > 0 and float(sgpa) <= 4:
                    cycle.sgpa = float(sgpa)
                else:
                    flash('Please make sure you enter a sGPA between 0 and 4.', category='error')
            else:
                cycle.sgpa = None
            mcat_total = request.form.get('mcat_total')
            if mcat_total:
                try:
                    if int(mcat_total) >= 472 and int(mcat_total) <= 528:
                        cycle.mcat_total = int(mcat_total)
                    else:
                        flash('Please make sure you enter a total MCAT score between 472 and 528.', category='error')
                except Exception as e:
                    flash('Please make sure you enter a total MCAT score between 472 and 528.', category='error')
            else:
                cycle.mcat_total = None
            mcat_cp = request.form.get('mcat_cp')
            if mcat_cp:
                try:
                    if int(mcat_cp) >= 118 and int(mcat_cp) <= 132:
                        cycle.mcat_cp = int(mcat_cp)
                    else:
                        flash('Please make sure you enter a Chemistry/Physics MCAT score between 118 and 132.', category='error')
                except Exception as e:
                    flash('Please make sure you enter a Chemistry/Physics MCAT score between 118 and 132.', category='error')
            else:
                cycle.mcat_cp = None
            mcat_cars = request.form.get('mcat_cars')
            if mcat_cars:
                try:
                    if int(mcat_cars) >= 118 and int(mcat_cars) <= 132:
                        cycle.mcat_cars = int(mcat_cars)
                    else:
                        flash('Please make sure you enter a CARS MCAT score between 118 and 132.',
                              category='error')
                except Exception as e:
                    flash('Please make sure you enter a CARS MCAT score between 118 and 132.',
                          category='error')
            else:
                cycle.mcat_cars = None
            mcat_bb = request.form.get('mcat_bb')
            if mcat_bb:
                try:
                    if int(mcat_bb) >= 118 and int(mcat_bb) <= 132:
                        cycle.mcat_bb = int(mcat_bb)
                    else:
                        flash('Please make sure you enter a Biology/Biochemistry MCAT score between 118 and 132.',
                              category='error')
                except Exception as e:
                    flash('Please make sure you enter a Biology/Biochemistry MCAT score between 118 and 132.',
                          category='error')
            else:
                cycle.mcat_bb = None
            mcat_ps = request.form.get('mcat_ps')
            if mcat_ps:
                try:
                    if int(mcat_ps) >= 118 and int(mcat_ps) <= 132:
                        cycle.mcat_ps = int(mcat_ps)
                    else:
                        flash('Please make sure you enter a Psychology/Sociology MCAT score between 118 and 132.',
                              category='error')
                except Exception as e:
                    flash('Please make sure you enter a Psychology/Sociology MCAT score between 118 and 132.',
                          category='error')
            else:
                cycle.mcat_ps = None
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
        if request.form.get('phd'):
            dual_degree_phd = True
        else:
            dual_degree_phd = False

        school_type = request.form.get('school_type')
        # Check if school already exists
        school = School.query.filter_by(name=add_school_name, cycle_id=cycle.id, phd=dual_degree_phd).first()
        if school:
            flash('You cannot add the same program twice.', category='error')
        else:
            db.session.add(School(name=add_school_name, cycle_id=cycle.id, user_id=current_user.id, phd=dual_degree_phd, school_type=school_type))
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

    return render_template('lists.html', user=current_user, cycle=cycle, md_school_list=form_options.MD_SCHOOL_LIST, do_school_list=form_options.DO_SCHOOL_LIST)

@pages.route('/visualizations', methods=['GET', 'POST'])
@login_required
def visualizations():
    vis_type = request.form.get('vis_type')
    if vis_type:
        cycle_id = int(request.form.get('cycle_id'))
        cycle = Cycle.query.filter_by(id=cycle_id).first()
        cycle_data = pd.read_sql(School.query.filter_by(cycle_id=cycle.id).statement, db.session.bind).drop(['id','cycle_id','user_id','school_type','phd'], axis=1)
        if vis_type.lower() == 'dot':
            graphJSON = dot.generate(cycle_data)
        elif vis_type.lower() == 'line':
            graphJSON = line.generate(cycle_data)
        elif vis_type.lower() == 'bar':
            # TODO: implement this
            graphJSON = None
        else:
            graphJSON = None
    else:
        graphJSON = None
    return render_template('visualizations.html', user=current_user, vis_types=form_options.VIS_TYPES, graphJSON=graphJSON)

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