from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, Response
from flask_login import current_user, login_required
from . import db, form_options, mail
from .models import Cycle, School, School_Profiles_Data
import json
from datetime import datetime, date
import re
from .visualizations import dot, line, bar, sankey, map
import pandas as pd
from .helpers import import_list_funcs, categorize_stats, school_stats_calculators
from flask_mail import Message
dashboard = Blueprint('dashboard', __name__)


@dashboard.route('/cycles', methods=['GET', 'POST'])
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
                base_format = "(?P<month>[0-9]{2})/(?P<year>[0-9]{4})"
                if re.match(base_format, birth):
                    month = int(re.search(base_format, birth).group('month'))
                    year = int(re.search(base_format, birth).group('year'))
                    # Make sure input is valid
                    if month >= 1 and month <= 12 and year >= (
                            date.today().year - 60) and year <= date.today().year - 17:
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
                        flash('Please make sure you enter a Chemistry/Physics MCAT score between 118 and 132.',
                              category='error')
                except Exception as e:
                    flash('Please make sure you enter a Chemistry/Physics MCAT score between 118 and 132.',
                          category='error')
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

    # Check if have stats filled out using cGPA as representative info
    empty_cycles = []
    for cycle in current_user.cycles:
        if not cycle.cgpa:
            empty_cycles.append(str(cycle.cycle_year))

    return render_template('cycles.html', user=current_user, cycle_options=form_options.VALID_CYCLES,
                           sex_options=form_options.SEX_OPTIONS, gender_options=form_options.GENDER_OPTIONS,
                           race_ethnicity_options=form_options.RACE_ETHNICITY_OPTIONS,
                           state_options=form_options.STATE_OPTIONS, empty_cycles=", ".join(empty_cycles))


@dashboard.route('/list', methods=['GET', 'POST'])
@login_required
def lists():
    # If GET request then did not provide a school
    if request.method == 'GET':
        if len(current_user.cycles) > 1:
            flash('Please select a cycle before viewing your school list.', category='error')
            return redirect(url_for('dashboard.cycles'))
        elif len(current_user.cycles) == 0:
            flash('Please add a cycle first.', category='error')
            return redirect(url_for('dashboard.cycles'))
        else:
            cycle_id = current_user.cycles[0].id
    # If POST then grab cycle ID
    else:
        cycle_id = request.form.get('cycle_id')

    cycle = Cycle.query.filter_by(id=cycle_id).first()
    schools = db.session.query(School, School_Profiles_Data).filter(School.cycle_id == cycle_id)\
        .join(School, School.name == School_Profiles_Data.school).order_by(School.rejection.asc(), School.withdrawn.asc(), School.acceptance.asc(), School.name.asc())

    # Check if PhD applicant for message about MD/DO-only consideration
    if School.query.filter_by(cycle_id=cycle.id, phd=True).first():
        phd_applicant = True
    else:
        phd_applicant = False

    # Handle adding school
    add_school_name = request.form.get('add_school')
    if add_school_name and len(add_school_name) > 0:
        if request.form.get('phd'):
            dual_degree_phd = True
        else:
            dual_degree_phd = False

        school_type = School_Profiles_Data.query.filter_by(school=add_school_name).first().md_or_do

        # Check if school already exists
        school = School.query.filter_by(name=add_school_name, cycle_id=cycle.id, phd=dual_degree_phd).first()
        if school:
            flash('You cannot add the same program twice.', category='error')
        else:
            db.session.add(
                School(name=add_school_name, cycle_id=cycle.id, user_id=current_user.id, phd=dual_degree_phd,
                       school_type=school_type))
            db.session.commit()

            # Update the application counter
            if dual_degree_phd:
                school_stats_calculators.count_apps_phd(add_school_name)
            else:
                school_stats_calculators.count_apps_reg(add_school_name)
            school_stats_calculators.update_all_schools()

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
        note = request.form.get('note')
        if note:
            school.note = note
        else:
            school.note = None
        db.session.commit()

    # Handle bulk edit
    for key in request.form:
        school_id = key.partition("-")[-1]
        if key.startswith('primary1'):
            primary_pre = request.form.get("primary0-" + school_id)
            if primary_pre == "":
                primary_pre = ""
            else:
                primary_pre = datetime.strptime(request.form.get("primary0-" + school_id), '%Y-%m-%d')
            primary_post = request.form.get("primary1-" + school_id)
            if primary_post == "":
                primary_post = ""
            else:
                primary_post = datetime.strptime(request.form.get("primary1-" + school_id), '%m/%d/%y')
            if primary_post != primary_pre:
                if primary_post != "":
                    primary_update = primary_post
                else:
                    primary_update = None
                school = School.query.filter_by(id=int(school_id)).first()
                school.primary = primary_update
        elif key.startswith('secondary_received1'):
            secondary_received_pre = request.form.get("secondary_received0-" + school_id)
            if secondary_received_pre == "":
                secondary_received_pre = ""
            else:
                secondary_received_pre = datetime.strptime(request.form.get("secondary_received0-" + school_id),
                                                           '%Y-%m-%d')
            secondary_received_post = request.form.get("secondary_received1-" + school_id)
            if secondary_received_post == "":
                secondary_received_post = ""
            else:
                secondary_received_post = datetime.strptime(request.form.get("secondary_received1-" + school_id),
                                                            '%m/%d/%y')
            if secondary_received_post != secondary_received_pre:
                if secondary_received_post != "":
                    secondary_received_update = secondary_received_post
                else:
                    secondary_received_update = None
                school = School.query.filter_by(id=int(school_id)).first()
                school.secondary_received = secondary_received_update
        elif key.startswith('application_complete1'):
            application_complete_pre = request.form.get("application_complete0-" + school_id)
            if application_complete_pre == "":
                application_complete_pre = ""
            else:
                application_complete_pre = datetime.strptime(request.form.get("application_complete0-" + school_id),
                                                             '%Y-%m-%d')
            application_complete_post = request.form.get("application_complete1-" + school_id)
            if application_complete_post == "":
                application_complete_post = ""
            else:
                application_complete_post = datetime.strptime(
                    request.form.get("application_complete1-" + school_id), '%m/%d/%y')
            if application_complete_post != application_complete_pre:
                if application_complete_post != "":
                    application_complete_update = application_complete_post
                else:
                    application_complete_update = None
                school = School.query.filter_by(id=int(school_id)).first()
                school.application_complete = application_complete_update
        elif key.startswith("interview_received1"):
            interview_received_pre = request.form.get("interview_received0-" + school_id)
            if interview_received_pre == "":
                interview_received_pre = ""
            else:
                interview_received_pre = datetime.strptime(request.form.get("interview_received0-" + school_id),
                                                           '%Y-%m-%d')
            interview_received_post = request.form.get("interview_received1-" + school_id)
            if interview_received_post == "":
                interview_received_post = ""
            else:
                interview_received_post = datetime.strptime(request.form.get("interview_received1-" + school_id),
                                                            '%m/%d/%y')
            if interview_received_post != interview_received_pre:
                if interview_received_post != "":
                    interview_received_update = interview_received_post
                else:
                    interview_received_update = None
                school = School.query.filter_by(id=int(school_id)).first()
                school.interview_received = interview_received_update
        elif key.startswith("interview_date1"):
            interview_date_pre = request.form.get("interview_date0-" + school_id)
            if interview_date_pre == "":
                interview_date_pre = ""
            else:
                interview_date_pre = datetime.strptime(request.form.get("interview_date0-" + school_id), '%Y-%m-%d')
            interview_date_post = request.form.get("interview_date1-" + school_id)
            if interview_date_post == "":
                interview_date_post = ""
            else:
                interview_date_post = datetime.strptime(request.form.get("interview_date1-" + school_id),
                                                        '%m/%d/%y')
            if interview_date_post != interview_date_pre:
                if interview_date_post != "":
                    interview_date_update = interview_date_post
                else:
                    interview_date_update = None
                school = School.query.filter_by(id=int(school_id)).first()
                school.interview_date = interview_date_update
        elif key.startswith("rejection1"):
            rejection_pre = request.form.get("rejection0-" + school_id)
            if rejection_pre == "":
                rejection_pre = ""
            else:
                rejection_pre = datetime.strptime(request.form.get("rejection0-" + school_id), '%Y-%m-%d')
            rejection_post = request.form.get("rejection1-" + school_id)
            if rejection_post == "":
                rejection_post = ""
            else:
                rejection_post = datetime.strptime(request.form.get("rejection1-" + school_id), '%m/%d/%y')
            if rejection_post != rejection_pre:
                if rejection_post != "":
                    rejection_update = rejection_post
                else:
                    rejection_update = None
                school = School.query.filter_by(id=int(school_id)).first()
                school.rejection = rejection_update
        elif key.startswith("waitlist1"):
            waitlist_pre = request.form.get("waitlist0-" + school_id)
            if waitlist_pre == "":
                waitlist_pre = ""
            else:
                waitlist_pre = datetime.strptime(request.form.get("waitlist0-" + school_id), '%Y-%m-%d')
            waitlist_post = request.form.get("waitlist1-" + school_id)
            if waitlist_post == "":
                waitlist_post = ""
            else:
                waitlist_post = datetime.strptime(request.form.get("waitlist1-" + school_id), '%m/%d/%y')
            if waitlist_post != waitlist_pre:
                if waitlist_post != "":
                    waitlist_update = waitlist_post
                else:
                    waitlist_update = None
                school = School.query.filter_by(id=int(school_id)).first()
                school.waitlist = waitlist_update
        elif key.startswith("acceptance1"):
            acceptance_pre = request.form.get("acceptance0-" + school_id)
            if acceptance_pre == "":
                acceptance_pre = ""
            else:
                acceptance_pre = datetime.strptime(request.form.get("acceptance0-" + school_id), '%Y-%m-%d')
            acceptance_post = request.form.get("acceptance1-" + school_id)
            if acceptance_post == "":
                acceptance_post = ""
            else:
                acceptance_post = datetime.strptime(request.form.get("acceptance1-" + school_id), '%m/%d/%y')
            if acceptance_post != acceptance_pre:
                if acceptance_post != "":
                    acceptance_update = acceptance_post
                else:
                    acceptance_update = None
                school = School.query.filter_by(id=int(school_id)).first()
                school.acceptance = acceptance_update
        elif key.startswith("withdrawn1"):
            withdrawn_pre = request.form.get("withdrawn0-" + school_id)
            if withdrawn_pre == "":
                withdrawn_pre = ""
            else:
                withdrawn_pre = datetime.strptime(request.form.get("withdrawn0-" + school_id), '%Y-%m-%d')
            withdrawn_post = request.form.get("withdrawn1-" + school_id)
            if withdrawn_post == "":
                withdrawn_post = ""
            else:
                withdrawn_post = datetime.strptime(request.form.get("withdrawn1-" + school_id), '%m/%d/%y')
            if withdrawn_post != withdrawn_pre:
                if withdrawn_post != "":
                    withdrawn_update = withdrawn_post
                else:
                    withdrawn_update = None
                school = School.query.filter_by(id=int(school_id)).first()
                school.withdrawn = withdrawn_update
        elif key.startswith("delete"):
            school = School.query.get(school_id)
            if school:
                if school.user_id == current_user.id:
                    db.session.delete(school)
        else:
            continue
        db.session.commit()

    return render_template('lists.html', user=current_user, cycle=cycle, schools=schools, phd_applicant=phd_applicant,
                           usmd_school_list=form_options.get_md_schools('USA'),
                           camd_school_list=form_options.get_md_schools('CAN'),
                           do_school_list=form_options.get_do_schools())


@dashboard.route('/import-list', methods=["GET", "POST"])
@login_required
def import_list():
    # If GET request then did not provide a cycle
    if request.method == 'GET':
        # If not one cycle redirect
        if len(current_user.cycles) > 1:
            flash('Please select a cycle before importing a list.', category='error')
            return redirect(url_for('dashboard.cycles'))
        elif len(current_user.cycles) == 0:
            flash('Please add a cycle first.', category='error')
            return redirect(url_for('dashboard.cycles'))
        # Continue by assuming the one cycle person has
        else:
            cycle_id = current_user.cycles[0].id
            cycle = Cycle.query.filter_by(id=cycle_id).first()
    # Process POST request
    else:
        # Wrap entire section to catch any errors during the process
        try:
            cycle_id = request.form.get('cycle_id')
            cycle = Cycle.query.filter_by(id=cycle_id).first()
            if not cycle:
                flash("Please select a school list before importing.", category='error')
                return redirect(url_for('dashboard.cycles'))
            # Receiving an excel table
            if request.files:
                table = request.files.get('table')
                if table.filename.endswith('xlsx'):
                    cycle_data = pd.read_excel(table, engine='openpyxl')
                elif table.filename.endswith('csv'):
                    cycle_data = pd.read_csv(table)
                # Break out of processing and send user back to page.
                else:
                    flash('Please upload a valid excel or CSV file.', category='error')
                    return render_template('import-list.html', user=current_user, cycle=cycle)
                # Drop any unused rows/columns
                cycle_data = cycle_data.dropna(axis=0, how='all')
                cycle_data = cycle_data.dropna(axis=1, how='all')
                cycle_data = import_list_funcs.convert_columns_date(cycle_data)
                colnames = cycle_data.columns
                tableJSON = cycle_data.to_json()
                return render_template('import-list.html', user=current_user, cycle=cycle, tableJSON=tableJSON,
                                       colnames=colnames, column_types=form_options.COLUMN_TYPES)
            # Process google
            elif request.form.get('upload_google_link'):
                link = request.form.get('upload_google_link')
                cycle_data = import_list_funcs.read_google(link)
                # Drop any unused rows/columns
                cycle_data = cycle_data.dropna(axis=0, how='all')
                cycle_data = cycle_data.dropna(axis=1, how='all')
                colnames = cycle_data.columns
                tableJSON = cycle_data.to_json()
                return render_template('import-list.html', user=current_user, cycle=cycle, tableJSON=tableJSON,
                                       colnames=colnames, column_types=form_options.COLUMN_TYPES)
            # Process assigned labels
            if request.form.get('labeled-columns'):
                # Reconstruct pandas table
                cycle_data = pd.read_json(request.form.get('tableJSON'))
                new_labels = []
                drop_columns = []
                for item in request.form:
                    if item.startswith('column->'):
                        original_column_label = item.split('->')[1]
                        label_assigned = request.form.get(item)
                        if len(label_assigned) > 0:
                            new_labels.append(form_options.COLUMN_LABEL_CONVERT_SQL[label_assigned])
                        else:
                            drop_columns.append(original_column_label)
                cycle_data = cycle_data.drop(columns=drop_columns)
                cycle_data.columns = new_labels
                tableJSON = cycle_data.to_json()

                # Grab list of best matches
                best_matches = {}
                for school in cycle_data['name']:
                    best_match = import_list_funcs.best_match(school, import_list_funcs.school_nicknames_dict.keys(),
                                                              0.7)
                    if best_match:
                        best_matches[school] = import_list_funcs.school_nicknames_dict[best_match]
                    else:
                        best_matches[school] = None

                # Require to have a names column
                if not 'name' in cycle_data.columns:
                    flash('Your spreadsheet must have a column with school names. Please try again.', category='error')
                    return redirect(url_for('dashboard.cycles'))
                return render_template('import-list.html', user=current_user, cycle=cycle, tableJSON=tableJSON,
                                       school_names=cycle_data['name'], md_school_list=form_options.get_md_schools(),
                                       do_school_list=form_options.get_do_schools(), best_matches=best_matches)
            # Final processing step
            if request.form.get('named-schools'):
                # Hold corrected names and schools with dual degree phd
                correct_names = {}
                phds = []
                for item in request.form:
                    if item.startswith('corrected_name->'):
                        correct_names[item.split('->')[1]] = request.form.get(item)
                    elif item.startswith('phd->'):
                        phds.append(item.split('->')[1])
                # Reconstruct table
                cycle_data = pd.read_json(request.form.get('tableJSON'))
                # Convert from timestamps
                for column in cycle_data.columns:
                    if column != 'name':
                        cycle_data[column] = pd.to_datetime(cycle_data[column], unit='ms')
                for index, row in cycle_data.iterrows():
                    school_name = correct_names[row['name']]
                    # Check input for PhD
                    if row['name'] in phds:
                        dual_degree_phd = True
                    else:
                        dual_degree_phd = False
                    # Get program type
                    if school_name in form_options.get_md_schools():
                        school_type = 'MD'
                    elif school_name in form_options.get_do_schools():
                        school_type = 'DO'

                    # Obtain all other dates
                    try:
                        primary = row['primary']
                        if pd.isnull(primary): primary = None
                    except Exception:
                        primary = None
                    try:
                        secondary_received = row['secondary_received']
                        if pd.isnull(secondary_received): secondary_received = None
                    except Exception:
                        secondary_received = None
                    try:
                        application_complete = row['application_complete']
                        if pd.isnull(application_complete): application_complete = None
                    except Exception:
                        application_complete = None
                    try:
                        interview_received = row['interview_received']
                        if pd.isnull(interview_received): interview_received = None
                    except Exception:
                        interview_received = None
                    try:
                        interview_date = row['interview_date']
                        if pd.isnull(interview_date): interview_date = None
                    except Exception:
                        interview_date = None
                    try:
                        rejection = row['rejection']
                        if pd.isnull(rejection): rejection = None
                    except Exception:
                        rejection = None
                    try:
                        waitlist = row['waitlist']
                        if pd.isnull(waitlist): waitlist = None
                    except Exception:
                        waitlist = None
                    try:
                        acceptance = row['acceptance']
                        if pd.isnull(acceptance): acceptance = None
                    except Exception:
                        acceptance = None
                    try:
                        withdrawn = row['withdrawn']
                        if pd.isnull(withdrawn): withdrawn = None
                    except Exception:
                        withdrawn = None

                    # Try to find if school is already in the list
                    school = School.query.filter_by(name=school_name, phd=dual_degree_phd, cycle_id=cycle_id).first()
                    if school:
                        if primary: school.primary = primary
                        if secondary_received: school.secondary_received = secondary_received
                        if application_complete: school.application_complete = application_complete
                        if interview_received: school.interview_received = interview_received
                        if interview_date: school.interview_date = interview_date
                        if rejection: school.rejection = rejection
                        if waitlist: school.waitlist = waitlist
                        if acceptance: school.acceptance = acceptance
                        if withdrawn: school.withdrawn = withdrawn
                        db.session.commit()
                    else:
                        db.session.add(School(name=school_name, user_id=current_user.id, cycle_id=cycle.id,
                                              school_type=school_type, phd=dual_degree_phd, primary=primary,
                                              secondary_received=secondary_received,
                                              application_complete=application_complete,
                                              interview_received=interview_received, interview_date=interview_date,
                                              rejection=rejection, waitlist=waitlist, acceptance=acceptance,
                                              withdrawn=withdrawn))
                        db.session.commit()
                # Success message and redirect
                flash('Successfully imported your school list.', category='success')
                if len(current_user.cycles) > 1:
                    return redirect(url_for('dashboard.cycles'))
                else:
                    return redirect(url_for('dashboard.lists'))
        except Exception:
            flash('We encountered an error while trying to import your school list. Please make sure to follow the '
                  'instructions with respect to formatting your spreadsheet to make sure that it is imported correctly.',
                  category='error')
            return redirect(url_for('dashboard.cycles'))
    return render_template('import-list.html', user=current_user, cycle=cycle)


@dashboard.route('/export-list', methods=["POST"])
@login_required
def export_list():
    # Get cycle
    cycle_id = int(request.form.get('cycle_id'))
    cycle = Cycle.query.filter_by(id=cycle_id).first()
    # Create dataframe of schools for that cycle and convert to CSV
    cycle_data = pd.read_sql(School.query.filter_by(cycle_id=cycle_id).statement, db.session.bind).drop(
        ['id', 'cycle_id', 'user_id', 'school_type', 'phd', 'note'], axis=1)
    csv = cycle_data.to_csv(index=False, encoding='utf-8')
    # Generate response/download
    response = Response(csv, mimetype='text/csv')
    response.headers.set("Content-Disposition", "attachment", filename=f'{cycle.cycle_year}_school_list.csv')
    return response


@dashboard.route('/suggestions', methods=['GET', 'POST'])
@login_required
def suggestions():
    if request.method == 'POST':
        form_type = request.form.get('type')
        contact = request.form.get('contact')
        content = request.form.get('content')
        spam_protect = request.form.get('spam_protect')
        if form_type and contact and content and spam_protect:
            if spam_protect.lower() == 'mcat':
                # Send email to us with suggestion
                email = Message(f'{form_type} on {date.today().strftime("%B %d, %Y")}',
                                sender=(f'CycleTrack {form_type}',
                                        f'admin@docs2be.org'),
                                recipients=['admin@docs2be.org'])
                email.body = f'Form Type: {form_type}\n\nAllow Contact: {contact}\n\nEmail: {current_user.email}' \
                             f'\n\nMessage:\n{content}'
                mail.send(email)

                if contact == 'yes':
                    flash(
                        f'Your {form_type.lower()} has been received. We may contact you if we have further questions.',
                        category='success')
                else:
                    flash(f'Your {form_type.lower()} has been received.', category='success')
                return redirect(url_for('dashboard.cycles'))
            else:
                flash('You did not answer our security question correctly.', category='error')
        else:
            flash(f'Please make sure to fill out all request fields.', category='error')

    return render_template('suggestions.html', user=current_user)


@dashboard.route('/delete-cycle', methods=['POST'])
def delete_cycle():
    cycle = json.loads(request.data)
    cycleId = cycle['cycleId']
    cycle = Cycle.query.get(cycleId)
    if cycle:
        if cycle.user_id == current_user.id:
            for school in cycle.schools:
                db.session.delete(school)
                db.session.commit()
                if school.phd:
                    school_stats_calculators.count_apps_phd(school.name)
                else:
                    school_stats_calculators.count_apps_reg(school.name)
            db.session.delete(cycle)
            db.session.commit()
            return jsonify({})


@dashboard.route('/delete-school', methods=['POST'])
def delete_school():
    school = json.loads(request.data)
    schoolId = school['schoolId']
    school = School.query.get(schoolId)
    if school:
        if school.user_id == current_user.id:
            db.session.delete(school)
            db.session.commit()
            # Remove school from count
            if school.phd:
                school_stats_calculators.count_apps_phd(school.name)
            else:
                school_stats_calculators.count_apps_reg(school.name)
            return jsonify({})


@dashboard.route('/visualizations', methods=['GET', 'POST'])
@login_required
def visualizations():
    # If GET request then did not provide a school
    if request.method == 'GET':
        if len(current_user.cycles) > 1:
            flash('Please select a cycle before creating visualizations.', category='error')
            return redirect(url_for('dashboard.cycles'))
        elif len(current_user.cycles) == 0:
            flash('Please add a cycle first.', category='error')
            return redirect(url_for('dashboard.cycles'))
        else:
            cycle_id = current_user.cycles[0].id
    # If POST then grab cycle ID
    else:
        cycle_id = request.form.get('cycle_id')

    # Grab cycle and data
    cycle = Cycle.query.filter_by(id=int(cycle_id)).first()
    cycle_data = pd.read_sql(School.query.filter_by(cycle_id=cycle.id).statement, db.session.bind)
    # Get application types
    # Dual Degree Types
    if any(cycle_data['phd']):
        app_types = ['Dual Degree']
        # If any MD/DO Only
        if not all(cycle_data['phd']):
            for type in cycle_data['school_type'].unique():
                app_types.append(f'{type} Only')
    # MD/DO Only
    else:
        app_types = list(cycle_data['school_type'].unique())
        if 'MD' in app_types and 'DO' in app_types: app_types.insert(0, 'MD or DO')

    # Vis Generation
    vis_type = request.form.get('vis_type')
    # Default to no graph and no settings saved
    save_settings = {'vis_type': None, 'app_type': None, 'color_type': None, 'plot_title': None, 'filters': None,
                     'map_type': None, 'demographics': None, 'anonymize_demographics': None, 'custom_text':None}
    graphJSON = None
    if vis_type:
        # Grab Settings
        if request.form.get('plot_title'):
            plot_title = request.form.get('plot_title')
        else:
            plot_title = "Application Cycle"
        color_type = request.form.get("color_type")
        app_type = request.form.get("app_type")
        map_type = request.form.get("map_type")
        demographics = request.form.get("demographics")
        anonymize_demographics = request.form.get("anonymize_demographics")
        custom_text = request.form.get("custom_text")
        # Default to no stats
        if demographics and not anonymize_demographics:
            if not cycle.mcat_total and not cycle.cgpa and not cycle.sgpa and not cycle.home_state:
                flash('You have not added your demographics yet. Please add them using the "cycles" page.', category='error')
                stats = None
            else:
                stats = {'mcat': cycle.mcat_total, 'cgpa': cycle.cgpa, 'sgpa': cycle.sgpa, 'state': cycle.home_state}
        elif demographics and anonymize_demographics:
            if not cycle.mcat_total and not cycle.cgpa and not cycle.sgpa and not cycle.home_state:
                flash('You have not added your demographics yet. Please add them using the "cycles" page.', category='error')
                stats = None
            else:
                stats = {'mcat': categorize_stats.categorize_mcat(cycle.mcat_total),
                         'cgpa': categorize_stats.categorize_gpa(cycle.cgpa),
                         'sgpa': categorize_stats.categorize_gpa(cycle.sgpa),
                         'state': cycle.home_state}
        else:
            stats = None


        # Save Settings
        save_settings = {'vis_type': vis_type, 'app_type': app_type, 'color_type': color_type, 'plot_title': plot_title,
                         'map_type': map_type, 'demographics': demographics,
                         'anonymize_demographics': anonymize_demographics, 'filters': {},'custom_text':custom_text}

        # Grab filters
        filter_types = {'primary': None, 'secondary_received': None, 'application_complete': None,
                        'interview_received': None, 'interview_date': None, 'rejection': None, 'waitlist': None,
                        'acceptance': None, 'withdrawn': None}

        # Apply data filters and save
        for filter in filter_types.keys():
            if request.form.get(f'exclude-{filter}'):
                cycle_data = cycle_data.drop([filter], axis=1)
                save_settings['filters'][filter] = True
            else:
                save_settings['filters'][filter] = False

        # Filter by PhD
        if app_type == 'Dual Degree':
            cycle_data = cycle_data[cycle_data['phd'] == True]
        else:
            cycle_data = cycle_data[cycle_data['phd'] == False]

        # Filter MD or DO
        if app_type == 'MD' or app_type == 'MD Only':
            cycle_data = cycle_data[cycle_data['school_type'] == 'MD']
        elif app_type == 'DO' or app_type == 'DO Only':
            cycle_data = cycle_data[cycle_data['school_type'] == 'DO']

        # Drop extra information
        cycle_data = cycle_data.drop(['id', 'cycle_id', 'user_id', 'school_type', 'phd', 'note'], axis=1)
        # Drop empty columns
        cycle_data = cycle_data.dropna(axis=1, how='all')
        # Get visualization JSON
        if len(cycle_data.columns) > 1:
            if vis_type.lower() == 'dot':
                graphJSON = dot.generate(cycle_data, plot_title, stats, color=color_type.lower(),custom_text=save_settings['custom_text'])
            elif vis_type.lower() == 'line':
                graphJSON = line.generate(cycle_data, plot_title, stats, color=color_type.lower(),custom_text=save_settings['custom_text'])
            elif vis_type.lower() == 'bar':
                graphJSON = bar.generate(cycle_data, plot_title, stats, color=color_type.lower(),custom_text=save_settings['custom_text'])
            elif vis_type.lower() == 'sankey':
                graphJSON = sankey.generate(cycle_data, plot_title, stats, color=color_type.lower(),custom_text=save_settings['custom_text'])
            elif vis_type.lower() == 'map':
                graphJSON = map.generate(cycle_data, plot_title, stats, color=color_type.lower(),map_scope=map_type.lower(),custom_text=save_settings['custom_text'])
        else:
            flash(f'Your selected school list for {cycle.cycle_year} does not have any dates yet!', category='error')

    return render_template('visualizations.html', user=current_user, cycle=cycle, app_types=app_types,
                           vis_types=form_options.VIS_TYPES, color_types=form_options.COLOR_TYPES, graphJSON=graphJSON,
                           save_settings=save_settings, map_types=form_options.MAP_TYPES)
