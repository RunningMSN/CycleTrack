from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, Response
from flask_login import current_user, login_required
from . import db, form_options, mail
from .models import User, Cycle, School
import json
from datetime import datetime, date
import re
from .visualizations import dot, line, bar, sankey, map, agg_map, school_table, school_graphs
import pandas as pd
from .helpers import import_list_funcs, school_info_calcs
from flask_mail import Message
import statistics

pages = Blueprint('pages', __name__)

@pages.route('/')
def index():
    user_count = db.session.query(User.id).count()
    app_count = db.session.query(School.id).count()
    school_count = db.session.query(School).group_by(School.name).count()
    map_data = pd.read_sql(School.query.statement, db.session.bind).drop(['id','cycle_id','user_id','school_type','phd'], axis=1)
    # Drop empty columns
    map_data = map_data.dropna(axis=1, how='all')
    if len(map_data) > 0:
        graphJSON = agg_map.generate(map_data)
    else:
        graphJSON = None
    return render_template('index.html', user=current_user, user_count=user_count, school_count=school_count,
                           app_count=app_count, graphJSON=graphJSON)

@pages.route('/about')
def about():
    return render_template('about.html', user=current_user)

@pages.route('/explorer', methods=['GET', 'POST'])
def explorer():
    # Query database for schools
    schools = db.session.query(School).group_by(School.name).all()
    # Dataframe with info about schools
    school_profiles = pd.read_csv('website/static/csv/SchoolProfiles.csv')
    # Dict to convert into dataframe with final results
    build_df = {'name': [], 'type': [], 'reg_apps': [], 'reg_med_mcat': [], 'reg_med_gpa': [],
                'phd_apps': [], 'logo_link' : [], 'city' : [], 'state' : [], 'envt' : [], 'pub_pri' : []}
    for school in schools:
        build_df['name'].append(school.name)
        build_df['type'].append(school.school_type)
        # Build lookup for school info
        school_info = school_profiles[school_profiles['School'] == school.name].reset_index()
        # Grab logo and school info
        build_df['logo_link'].append(school_info['Logo_File_Name'][0])
        build_df['city'].append(school_info['City'][0])
        build_df['state'].append(school_info['State'][0])
        build_df['envt'].append(school_info['Envt_Type'][0])
        build_df['pub_pri'].append(school_info['Private_Public'][0])

        # Grab stats data
        query = db.session.query(School, Cycle).filter(School.name == school.name).join(Cycle, School.cycle_id == Cycle.id)
        reg_data = pd.read_sql(query.filter(School.phd == False).statement, db.session.bind)
        # Get number of applications
        build_df['reg_apps'].append(len(reg_data))
        build_df['phd_apps'].append(query.filter(School.phd == True).count())

        # Grab median cGPA and MCAT accepted for reg applications
        accepted = reg_data[pd.notna(reg_data['acceptance'])]
        if len(accepted['cgpa'].dropna(axis=0)) > 4:
            build_df['reg_med_gpa'].append('{:.2f}'.format(statistics.median(accepted['cgpa'].dropna(axis=0))))
        else:
            build_df['reg_med_gpa'].append('X.XX')
        if len(accepted['mcat_total'].dropna(axis=0)) > 4:
            build_df['reg_med_mcat'].append('{:.1f}'.format(statistics.median(accepted['mcat_total'].dropna(axis=0))))
        else:
            build_df['reg_med_mcat'].append('XXX')

    # Generate dataframe
    df = pd.DataFrame(build_df).sort_values('name')

    # Perform filtering
    if request.method == 'POST':
        # Filter type
        if request.form.get('school_type') != "All":
            df = df[df['type'] == request.form.get('school_type')]
        if request.form.get('state') != "All":
            if request.form.get('state') != "Canada": # Will need to change this on implementing canadian schools
                df = df[df['state'] == form_options.STATE_ABBREV[request.form.get('state')]]

    if len(df) == 0: df = None
    # Render page
    return render_template('explorer.html', user=current_user, state_options=form_options.STATES_WITH_SCHOOLS, schools=df)

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

    # Check if have stats filled out using cGPA as representative info
    empty_cycles = []
    for cycle in current_user.cycles:
        if not cycle.cgpa:
            empty_cycles.append(str(cycle.cycle_year))

    return render_template('cycles.html', user=current_user, cycle_options=form_options.VALID_CYCLES,
                           sex_options=form_options.SEX_OPTIONS, gender_options=form_options.GENDER_OPTIONS,
                           race_ethnicity_options=form_options.RACE_ETHNICITY_OPTIONS,
                           state_options=form_options.STATE_OPTIONS, empty_cycles=", ".join(empty_cycles))

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

    # Check if PhD applicant for message about MD/DO-only consideration
    if School.query.filter_by(cycle_id=cycle.id, phd=True).first():
        phd_applicant = True
    else:
        phd_applicant = False

    return render_template('lists.html', user=current_user, cycle=cycle, md_school_list=form_options.MD_SCHOOL_LIST,
                           do_school_list=form_options.DO_SCHOOL_LIST, phd_applicant=phd_applicant)

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
        color_type = request.form.get("color_type")
        cycle = Cycle.query.filter_by(id=cycle_id).first()
        cycle_data = pd.read_sql(School.query.filter_by(cycle_id=cycle.id).statement, db.session.bind)

        # Grab filter
        filter = request.form.get('filter')
        # Filter dual degree
        if filter == 'reg' or filter == 'md' or filter == 'do':
            cycle_data = cycle_data[cycle_data['phd'] == False]
        elif filter == 'phd'or filter == 'md-phd' or filter == 'do-phd':
            cycle_data = cycle_data[cycle_data['phd'] == True]
        # Filter program type
        if filter == 'md' or filter == 'md-phd':
            cycle_data = cycle_data[cycle_data['school_type'] == 'MD']
        elif filter == 'do' or filter == 'do-phd':
            cycle_data = cycle_data[cycle_data['school_type'] == 'DO']

        cycle_data = cycle_data.drop(['id','cycle_id','user_id','school_type','phd'], axis=1)

        # Drop empty columns
        cycle_data = cycle_data.dropna(axis=1, how='all')

        if len(cycle_data.columns) > 1:
            if vis_type.lower() == 'dot':
                graphJSON = dot.generate(cycle_data, plot_title,color=color_type.lower())
            elif vis_type.lower() == 'line':
                graphJSON = line.generate(cycle_data, plot_title,color=color_type.lower())
            elif vis_type.lower() == 'bar':
                graphJSON = bar.generate(cycle_data, plot_title,color=color_type.lower())
            elif vis_type.lower() == 'sankey':
                graphJSON = sankey.generate(cycle_data, plot_title,color=color_type.lower())
            elif vis_type.lower() == 'map':
                graphJSON = map.generate(cycle_data,plot_title,color=color_type.lower())
        else:
            flash(f'Your selected school list for {cycle.cycle_year} does not have any dates yet!', category='error')
    return render_template('visualizations.html', user=current_user, vis_types=form_options.VIS_TYPES, color_types = form_options.COLOR_TYPES, graphJSON=graphJSON)

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

@pages.route('/terms')
def terms():
    return render_template('terms.html', user=current_user)

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

@pages.route('/explorer/<school_name>')
def explore_school(school_name):
    # Find school
    school_name = school_name.replace('%20', ' ')
    if school_name not in form_options.MD_SCHOOL_LIST and school_name not in form_options.DO_SCHOOL_LIST:
        flash(f'Could not find {school_name}. Please navigate to your school using the explorer.', category='error')
        return redirect(url_for('pages.explorer'))

    # Build AAMC tables
    school_profiles = pd.read_csv('website/static/csv/SchoolProfiles.csv')
    school_info = school_profiles[school_profiles['School'] == school_name].reset_index()
    table_md, table_mdphd = school_table.generate(school_name)

    # Query info about the school
    query = db.session.query(School, Cycle).filter(School.name == school_name).join(Cycle, School.cycle_id == Cycle.id)
    reg_data = pd.read_sql(query.filter(School.phd == False).statement, db.session.bind)
    phd_data = pd.read_sql(query.filter(School.phd == True).statement, db.session.bind)

    # Dictionaries with all information about the school
    reg_info = {'aamc_table': table_md, 'cycle_status_json': school_graphs.cycle_progress(reg_data),
                'interview_graph': school_graphs.interview_acceptance_histogram(reg_data, 'interview_received'),
                'acceptance_graph': school_graphs.interview_acceptance_histogram(reg_data, 'acceptance')}
    phd_info = {'aamc_table': table_mdphd, 'cycle_status_json': school_graphs.cycle_progress(phd_data),
                'interview_graph': school_graphs.interview_acceptance_histogram(phd_data, 'interview_received'),
                'acceptance_graph': school_graphs.interview_acceptance_histogram(phd_data, 'acceptance')}

    # Get current cycle status graph
    cycle_status_reg_json = school_graphs.cycle_progress(reg_data)
    cycle_status_phd_json = school_graphs.cycle_progress(phd_data)

    # Calculate interview information
    school_info_calcs.interview_calculations(reg_data, reg_info)
    school_info_calcs.interview_calculations(phd_data, phd_info)

    # Calculate acceptance information
    school_info_calcs.acceptance_calculations(reg_data, reg_info)
    school_info_calcs.acceptance_calculations(phd_data, phd_info)

    return render_template('school_template.html', user=current_user, school_info=school_info, table_md=table_md,
                           table_mdphd=table_mdphd, reg_info=reg_info, phd_info=phd_info)

@pages.route('/suggestions', methods=['GET', 'POST'])
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
                email = Message(f'{form_type} on {date.today().strftime("%B %d, %Y")}', sender=(f'CycleTrack {form_type}',
                                                                       f'admin@docs2be.org'),
                                                                       recipients=['admin@docs2be.org'])
                email.body = f'Form Type: {form_type}\n\nAllow Contact: {contact}\n\nEmail: {current_user.email}' \
                             f'\n\nMessage:\n{content}'
                mail.send(email)

                if contact == 'yes':
                    flash(f'Your {form_type.lower()} has been received. We may contact you if we have further questions.',
                          category='success')
                else:
                    flash(f'Your {form_type.lower()} has been received.', category='success')
                return redirect(url_for('pages.cycles'))
            else:
                flash('You did not answer our security question correctly.', category='error')
        else:
            flash(f'Please make sure to fill out all request fields.', category='error')

    return render_template('suggestions.html', user=current_user)