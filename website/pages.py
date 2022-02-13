from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, Response
from flask_login import current_user, login_required
from . import db, form_options
from .models import User,Cycle, School
import json
from datetime import datetime, date
import re
from .visualizations import dot, line, bar, sankey, map, agg_map
import pandas as pd
from .helpers import import_list_funcs
import traceback

pages = Blueprint('pages', __name__)

@pages.route('/')
def index():
    user_count = db.session.query(User.id).count()
    app_count = db.session.query(School.id).count()
    map_data = pd.read_sql(School.query.statement, db.session.bind).drop(['id','cycle_id','user_id','school_type','phd'], axis=1)
    # Drop empty columns
    map_data = map_data.dropna(axis=1, how='all')
    if len(map_data) > 0:
        graphJSON = agg_map.generate(map_data)
    else:
        graphJSON = None
    return render_template('index.html', user=current_user, user_count=user_count, app_count=app_count,graphJSON=graphJSON)

@pages.route('/explorer')
def explorer():
    # Get list of schools
    schools = db.session.query(School.name.distinct())
    # Dict to convert into dataframe
    build_df = {'name': [], 'type': [], 'reg_apps': [], 'reg_med_mcat': [], 'reg_med_gpa': [],
                'phd_apps': [], 'phd_med_mcat': [], 'phd_med_gpa': []}
    # Fill data
    for school in schools:
        build_df['name'].append(school[0])
        if school[0] in form_options.MD_SCHOOL_LIST:
            build_df['type'].append('MD')
        else:
            build_df['type'].append('DO')
        # MD/DO Data
        build_df['reg_apps'].append(School.query.filter_by(name=school[0], phd=False).count())
        build_df['reg_med_mcat'].append(None)
        build_df['reg_med_gpa'].append(None)
        # MD-PhD/DO-PhD data
        build_df['phd_apps'].append(School.query.filter_by(name=school[0], phd=True).count())
        build_df['phd_med_mcat'].append(None)
        build_df['phd_med_gpa'].append(None)
    # Generate dataframe
    df = pd.DataFrame(build_df).sort_values('name')
    print(df)
    # Render page
    return render_template('explorer.html', user=current_user, schools=df)

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

    return render_template('lists.html', user=current_user, cycle=cycle, md_school_list=form_options.MD_SCHOOL_LIST,
                           do_school_list=form_options.DO_SCHOOL_LIST)

@pages.route('/visualizations', methods=['GET', 'POST'])
@login_required
def visualizations():
    vis_type = request.form.get('vis_type')
    # Default to no graph
    graphJSON = None
    if vis_type:
        cycle_id = int(request.form.get('cycle_id'))
        if request.form.get('plot_title'):
            plot_title = request.form.get('plot_title')
        else:
            plot_title = "Application Cycle"
        cycle = Cycle.query.filter_by(id=cycle_id).first()
        cycle_data = pd.read_sql(School.query.filter_by(cycle_id=cycle.id).statement, db.session.bind).drop(['id','cycle_id','user_id','school_type','phd'], axis=1)
        # Drop empty columns
        cycle_data = cycle_data.dropna(axis=1, how='all')
        if len(cycle_data.columns) > 1:
            if vis_type.lower() == 'dot':
                graphJSON = dot.generate(cycle_data, plot_title)
            elif vis_type.lower() == 'line':
                graphJSON = line.generate(cycle_data, plot_title)
            elif vis_type.lower() == 'bar':
                graphJSON = bar.generate(cycle_data, plot_title)
            elif vis_type.lower() == 'sankey':
                graphJSON = sankey.generate(cycle_data, plot_title)
            elif vis_type.lower() == 'map':
                graphJSON = map.generate(cycle_data,plot_title)
        else:
            flash(f'Your school list for the {cycle.cycle_year} does not have any dates yet!', category='error')
    return render_template('visualizations.html', user=current_user, vis_types=form_options.VIS_TYPES, graphJSON=graphJSON)

@pages.route('/import-list', methods=["GET", "POST"])
@login_required
def import_list():
    # If GET request then did not provide a cycle
    if request.method == 'GET':
        # If not one cycle redirect
        if len(current_user.cycles) > 1:
            flash('Please select a cycle before importing a list.', category='error')
            return redirect(url_for('pages.cycles'))
        elif len(current_user.cycles) == 0:
            flash('Please add a cycle first.', category='error')
            return redirect(url_for('pages.cycles'))
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
                return redirect(url_for('pages.cycles'))
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
                    best_match = import_list_funcs.best_match(school, import_list_funcs.school_nicknames_dict.keys(), 0.7)
                    if best_match:
                        best_matches[school] = import_list_funcs.school_nicknames_dict[best_match]
                    else:
                        best_matches[school] = None

                # Require to have a names column
                if not 'name' in cycle_data.columns:
                    flash('Your spreadsheet must have a column with school names. Please try again.', category='error')
                    return redirect(url_for('pages.cycles'))
                return render_template('import-list.html', user=current_user, cycle=cycle, tableJSON=tableJSON,
                                       school_names=cycle_data['name'], md_school_list=form_options.MD_SCHOOL_LIST,
                                       do_school_list=form_options.DO_SCHOOL_LIST, best_matches=best_matches)
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
                    if school_name in form_options.MD_SCHOOL_LIST:
                        school_type='MD'
                    elif school_name in form_options.DO_SCHOOL_LIST:
                        school_type='DO'

                    # Obtain all other dates
                    try:
                        primary = row['primary']
                        if pd.isnull(primary): primary= None
                    except Exception:
                        primary = None
                    try:
                        secondary_received = row['secondary_received']
                        if pd.isnull(secondary_received): secondary_received= None
                    except Exception:
                        secondary_received = None
                    try:
                        application_complete = row['application_complete']
                        if pd.isnull(application_complete): application_complete= None
                    except Exception:
                        application_complete = None
                    try:
                        interview_received = row['interview_received']
                        if pd.isnull(interview_received): interview_received= None
                    except Exception:
                        interview_received = None
                    try:
                        interview_date = row['interview_date']
                        if pd.isnull(interview_date): interview_date= None
                    except Exception:
                        interview_date = None
                    try:
                        rejection = row['rejection']
                        if pd.isnull(rejection): rejection= None
                    except Exception:
                        rejection = None
                    try:
                        waitlist = row['waitlist']
                        if pd.isnull(waitlist): waitlist= None
                    except Exception:
                        waitlist = None
                    try:
                        acceptance = row['acceptance']
                        if pd.isnull(acceptance): acceptance= None
                    except Exception:
                        acceptance = None
                    try:
                        withdrawn = row['withdrawn']
                        if pd.isnull(withdrawn): withdrawn= None
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
                                              secondary_received=secondary_received, application_complete=application_complete,
                                              interview_received=interview_received, interview_date=interview_date,
                                              rejection=rejection, waitlist=waitlist, acceptance=acceptance,
                                              withdrawn=withdrawn))
                        db.session.commit()
                # Success message and redirect
                flash('Successfully imported your school list.', category='success')
                if len(current_user.cycles) > 1:
                    return redirect(url_for('pages.cycles'))
                else:
                    return redirect(url_for('pages.lists'))
        except Exception:
            flash('We encountered an error while trying to import your school list. Please make sure to follow the '
                  'instructions with respect to formatting your spreadsheet to make sure that it is imported correctly.',
                  category='error')
            print(traceback.format_exc())
            return redirect(url_for('pages.cycles'))
    return render_template('import-list.html', user=current_user, cycle=cycle)

@pages.route('/export-list', methods=["POST"])
@login_required
def export_list():
    # Get cycle
    cycle_id = int(request.form.get('cycle_id'))
    cycle = Cycle.query.filter_by(id=cycle_id).first()
    # Create dataframe of schools for that cycle and convert to CSV
    cycle_data = pd.read_sql(School.query.filter_by(cycle_id=cycle_id).statement, db.session.bind).drop(
        ['id', 'cycle_id', 'user_id', 'school_type', 'phd'], axis=1)
    csv = cycle_data.to_csv(index=False, encoding='utf-8')
    # Generate response/download
    response = Response(csv, mimetype='text/csv')
    response.headers.set("Content-Disposition", "attachment", filename=f'{cycle.cycle_year}_school_list.csv')
    return response

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