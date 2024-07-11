from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, Response, Markup, escape
from flask_login import current_user, login_required
from . import db, form_options, mail
from .models import Cycle, School, School_Profiles_Data, Courses, User_Profiles, School_Stats, Secondary_Costs
import json
from datetime import datetime, date, timedelta
import dateutil.parser
import re
from .visualizations import dot, line, bar, sankey, map, gpa_graph, horz_bar
import pandas as pd
from .helpers import import_list_funcs, categorize_stats, gpa_calculators, combine_app_types
from flask_mail import Message

dashboard = Blueprint('dashboard', __name__)


@dashboard.route('/cycles', methods=['GET', 'POST'])
@login_required
def cycles():
    # Manage all requests for updating information
    if request.method == 'POST':
        # Find that person is editing a cycle
        cycle_id = request.form.get('cycle_id_edit')

        # Find that is adding a new cycle
        add_cycle = request.form.get('new_cycle_year')
        if add_cycle:
            # Check if added cycle already exists
            cycle = Cycle.query.filter_by(cycle_year=int(add_cycle), user_id=current_user.id).first()
            if cycle:
                flash(f'You already have a cycle for {add_cycle}.', category='error')
            else:
                new_cycle = Cycle(cycle_year=int(add_cycle), user_id=current_user.id, mentoring_message=False)
                db.session.add(new_cycle)
                db.session.commit()

                # Add a cycle_id to send any demographics, etc. into the editing
                cycle_id = new_cycle.id

        if cycle_id:
            cycle = Cycle.query.filter_by(id=int(cycle_id)).first()
            gender = request.form.get('gender')
            if len(gender) > 0 and gender in form_options.GENDER_OPTIONS:
                cycle.gender = gender
            else:
                cycle.gender = None
            other_gender = request.form.get('other_gender')
            if len(other_gender) > 0:
                cycle.other_gender = other_gender
            else:
                cycle.other_gender = None
            sex = request.form.get('sex')
            if len(sex) > 0 and sex in form_options.SEX_OPTIONS:
                cycle.sex = sex
            else:
                cycle.sex = None
            other_sex = request.form.get('other_sex')
            if len(other_sex) > 0:
                cycle.other_sex = other_sex
            else:
                cycle.other_sex = None
            age = request.form.get('age')
            if age:
                try:
                    age = int(age)
                    if age >15 and age <50:
                        cycle.age = age
                except Exception as e:
                    flash('Please make sure your age is an integer.', category='error')
            else:
                cycle.age = None
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
            other_race_ethnicity = request.form.get('other_race_ethnicity')
            if len(other_race_ethnicity) > 0:
                cycle.other_race_ethnicity = other_race_ethnicity
            else:
                cycle.other_race_ethnicity = None
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
            casper = request.form.get('casper')
            if casper:
                try:
                    if int(casper) >= 1 and int(casper) <= 4:
                        cycle.casper = int(casper)
                    else:
                        flash('Please make sure you enter a CASPer quartile between 1 and 4.',
                              category='error')
                except Exception as e:
                    flash('Please make sure you enter a CASPer quartile between 1 and 4.',
                          category='error')
            else:
                cycle.casper = None
            preview_score = request.form.get('preview_score')
            if preview_score:
                try:
                    if int(preview_score) >= 1 and int(preview_score) <= 9:
                        cycle.preview_score = int(preview_score)
                    else:
                        flash('Please make sure you enter a PREview score between 1 and 9.',
                              category='error')
                except Exception as e:
                    flash('Please make sure you enter a CASPer quartile between 1 and 4.',
                          category='error')
            else:
                cycle.preview_score = None
            preview_percentile = request.form.get('preview_percentile')
            if preview_percentile:
                try:
                    if int(preview_percentile) >= 0 and int(preview_percentile) <= 100:
                        cycle.preview_percentile = int(preview_percentile)
                    else:
                        flash('Please make sure you enter a PREview percentile between 0 and 100.',
                              category='error')
                except Exception as e:
                    flash('Please make sure you enter a PREview percentile between 0 and 100.',
                          category='error')
            else:
                cycle.preview_percentile = None
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
    schools = db.session.query(School, School_Profiles_Data).filter(School.cycle_id == cycle_id) \
        .join(School, School.name == School_Profiles_Data.school).order_by(School.rejection.asc(),
                                                                           School.withdrawn.asc(),
                                                                           School.acceptance.asc(), School.name.asc())

    # Handle adding schools
    if request.form.get('school_names'):
        schools_add = request.form.get('school_names').split('<>')
        phds_add = request.form.get('phd_values').split('<>')

        for i in range(0, len(schools_add)):
            school_profile = School_Profiles_Data.query.filter_by(school=schools_add[i]).first()
            school_type = school_profile.md_or_do
            school_id = school_profile.school_id

            # Check if school already exists
            if phds_add[i] == 'true':
                dual_degree_phd=True
            else:
                dual_degree_phd = False
            school = School.query.filter_by(school_id=school_id, cycle_id=cycle.id, phd=dual_degree_phd).first()
            if(not school):
                db.session.add(
                    School(name=schools_add[i], cycle_id=cycle.id, user_id=current_user.id, phd=dual_degree_phd,
                           school_type=school_type, school_id=school_id))
                db.session.commit()

    # Handle bulk edit
    if request.form.get('bulk_edit'):
        if len(request.form.get("edited_schools")) > 0:
            edited_schools = request.form.get("edited_schools").split(sep=",")

            for school in edited_schools:
                school_id = school.partition("-")[0]
                action = school.partition("-")[-1]

                # Grab the school
                school = School.query.filter_by(id=int(school_id)).first()
                if action == "primary":
                    primary = request.form.get("primary-" + school_id)
                    if primary:
                        school.primary = dateutil.parser.parse(primary)
                    else:
                        school.primary = None
                elif action == "secondary_received":
                    secondary_received = request.form.get("secondary_received-" + school_id)
                    if secondary_received:
                        school.secondary_received = dateutil.parser.parse(secondary_received)
                    else:
                        school.secondary_received = None
                elif action == "application_complete":
                    application_complete = request.form.get("application_complete-" + school_id)
                    if application_complete:
                        school.application_complete = dateutil.parser.parse(application_complete)
                    else:
                        school.application_complete = None
                elif action == "pre_int_hold":
                    pre_int_hold = request.form.get("pre_int_hold-" + school_id)
                    if pre_int_hold:
                        school.pre_int_hold = dateutil.parser.parse(pre_int_hold)
                    else:
                        school.pre_int_hold = None
                elif action == "interview_received":
                    interview_received = request.form.get("interview_received-" + school_id)
                    if interview_received:
                        school.interview_received = dateutil.parser.parse(interview_received)
                    else:
                        school.interview_received = None
                elif action == "interview_date":
                    interview_date = request.form.get("interview_date-" + school_id)
                    if interview_date:
                        school.interview_date = dateutil.parser.parse(interview_date)
                    else:
                        school.interview_date = None
                elif action == "rejection":
                    rejection = request.form.get("rejection-" + school_id)
                    if rejection:
                        school.rejection = dateutil.parser.parse(rejection)
                    else:
                        school.rejection = None
                elif action == "waitlist":
                    waitlist = request.form.get("waitlist-" + school_id)
                    if waitlist:
                        school.waitlist = dateutil.parser.parse(waitlist)
                    else:
                        school.waitlist = None
                elif action == "acceptance":
                    acceptance = request.form.get("acceptance-" + school_id)
                    if acceptance:
                        school.acceptance = dateutil.parser.parse(acceptance)
                    else:
                        school.acceptance = None
                elif action == "withdrawn":
                    withdrawn = request.form.get("withdrawn-" + school_id)
                    if withdrawn:
                        school.withdrawn = dateutil.parser.parse(withdrawn)
                    else:
                        school.withdrawn = None
                elif action == "note":
                    note = request.form.get("note-" + school_id)
                    school.note = escape(note)
        else:
            flash(Markup("We've detected that your updates may not have saved correctly. If this is indeed an error, please try "
                  "<a href='https://www.umass.edu/afsystems/sites/default/files/resources/how-do-i-clear-my-web-browser.pdf'>clearing your browser's cache</a>. If the problem persists, please send us a bug report."), category="warning")
        db.session.commit()

    # Handle updating costs
    if request.form.get('input_cost'):
        for item in request.form:
            if item.startswith("cost-"):
                school_details = item.split('-')
                secondary_cost = Secondary_Costs.query.filter_by(school_id=school_details[1],
                                                                 cycle_year=cycle.cycle_year).first()
                try:
                    value = int(request.form.get(item))
                except Exception:
                    value = None

                if (value is not None) and (not current_user.id in secondary_cost.contributors.split(',')):
                    secondary_cost.contributors += f"{current_user.id},"
                    if school_details[2] == 'Reg':
                        if secondary_cost.reg_cost == value:
                            secondary_cost.reg_cost_confirmed = True
                        else:
                            secondary_cost.reg_cost = value
                    elif school_details[2] == 'PhD':
                        if secondary_cost.phd_cost == value:
                            secondary_cost.phd_cost_confirmed = True
                        else:
                            secondary_cost.phd_cost = value
                    elif school_details[2] == 'Reg_to_PhD':
                        if secondary_cost.reg_to_phd == value:
                            secondary_cost.reg_to_phd_confirmed = True
                        else:
                            secondary_cost.reg_to_phd = value
                    db.session.commit()

    # Check if there are schools person can add secondary cost to
    schools_to_add_secondary_cost = pd.DataFrame(columns=['school_id', 'name', 'type', 'prog_type'])
    for school, profile in schools:
        # Check if cost entry exists
        secondary_cost = Secondary_Costs.query.filter_by(school_id=school.school_id, cycle_year=cycle.cycle_year).first()
        # If cost entry doesn't exist, create one for the school
        if not secondary_cost:
            secondary_cost = Secondary_Costs(school_id=school.school_id, cycle_year=cycle.cycle_year, contributors="")
            db.session.add(secondary_cost)
            db.session.commit()
        # Check if user has contributed to cost entry already
        cost_contributors = secondary_cost.contributors.split(',')
        if not str(current_user.id) in cost_contributors:
            # If applying PhD
            if school.phd and not secondary_cost.phd_cost_confirmed and school.application_complete:
                new_row = pd.DataFrame({'school_id': [school.school_id],
                                        'name': [school.name],
                                        'type': ['PhD'],
                                        'prog_type': [school.school_type]})
                schools_to_add_secondary_cost = pd.concat([schools_to_add_secondary_cost, new_row], ignore_index=True)

                # Assume it is concurrent application to 2 programs if the application complete date is the same for both
                reg_check = School.query.filter_by(school_id=school.school_id, phd=False, cycle_id=school.cycle_id,
                                                   application_complete=school.application_complete).first()
                if reg_check and not secondary_cost.reg_to_phd_confirmed and reg_check.application_complete:
                    new_row = pd.DataFrame({'school_id': [school.school_id],
                                            'name': [school.name],
                                            'type': ['Reg_to_PhD'],
                                            'prog_type': [school.school_type]})
                    schools_to_add_secondary_cost = pd.concat([schools_to_add_secondary_cost, new_row],
                                                              ignore_index=True)
            else:
                # Make sure don't have PhD application, if have a PhD application, move on
                phd_check = School.query.filter_by(school_id=school.school_id, phd=True, cycle_id=school.cycle_id).first()
                if not phd_check and not secondary_cost.reg_cost_confirmed and school.application_complete:
                    new_row = pd.DataFrame({'school_id': [school.school_id],
                                            'name': [school.name],
                                            'type': ['Reg'],
                                            'prog_type': [school.school_type]})
                    schools_to_add_secondary_cost = pd.concat([schools_to_add_secondary_cost, new_row],
                                                              ignore_index=True)

    # Check if PhD applicant for message about MD/DO-only consideration
    if School.query.filter_by(cycle_id=cycle.id, phd=True).first():
        phd_applicant = True
    else:
        phd_applicant = False

    # Grab list of programs types for filtering
    program_types = []
    if School.query.filter_by(cycle_id=cycle.id, school_type='MD', phd=True).first():
        program_types.append('MD-PhD')
    if School.query.filter_by(cycle_id=cycle.id, school_type='DO', phd=True).first():
        program_types.append('DO-PhD')
    if School.query.filter_by(cycle_id=cycle.id, school_type='MD', phd=False).first():
        program_types.append('MD')
    if School.query.filter_by(cycle_id=cycle.id, school_type='DO', phd=False).first():
        program_types.append('DO')

    # if it's the current cycle, get the most recent dates
    missing_hard_delay_cutoff = []
    if cycle.cycle_year == form_options.VALID_CYCLES[0]:
        # Get the most recent dates
        dates = {}
        for school in schools:
            school_stats = School_Stats.query.filter_by(school_id=school[1].school_id).first()
            name = school[0].name
            dates[name] = {}
            if school[0].phd == True:
                dates[name]['interview'] = school_stats.phd_interview_date.strftime("%m-%d-%y") if school_stats.phd_interview_date is not None else None 
                dates[name]['waitlist'] = school_stats.phd_waitlist_date.strftime("%m-%d-%y") if school_stats.phd_waitlist_date is not None else None
                dates[name]['acceptance'] = school_stats.phd_acceptance_date.strftime("%m-%d-%y") if school_stats.phd_acceptance_date is not None else None
                if not school_stats.phd_interview_date and not school_stats.phd_waitlist_date and not school_stats.phd_acceptance_date:
                    dates[name]= None
            else:
                dates[name]['interview'] = school_stats.reg_interview_date.strftime("%m-%d-%y") if school_stats.reg_interview_date is not None else None
                dates[name]['waitlist'] = school_stats.reg_waitlist_date.strftime("%m-%d-%y") if school_stats.reg_waitlist_date is not None else None
                dates[name]['acceptance'] = school_stats.reg_acceptance_date.strftime("%m-%d-%y") if school_stats.reg_acceptance_date is not None else None
                if not school_stats.reg_interview_date and not school_stats.reg_waitlist_date and not school_stats.reg_acceptance_date:
                    dates[name]= None

        # Update any entered new hard deadlines
        for item in request.form:
            if item.startswith("hard_delay_collect-"):
                school_details = item.split('-')
                edit_hard_deadline = School.query.filter_by(id=school_details[1]).first()
                if request.form.get(item):
                    try:
                        edit_hard_deadline.hard_secondary_submission_days = int(request.form.get(item))
                    except:
                        flash('Your strict deadline must be entered as an integer number of days (e.g. enter 14 NOT 14 days).', category='error')
                else:
                    edit_hard_deadline.hard_secondary_submission_days = -1
        db.session.commit()

        secondary_submission_order = {"school": [], "profile": [], "hard_soft": [], "recommended_submission": []}
        for school, profile in schools:
            # Find missing hard deadlines
            if school.secondary_received and not school.application_complete and not school.hard_secondary_submission_days:
                missing_hard_delay_cutoff.append(school)

            if school.application_complete:
                continue

            # Process list ordering
            secondary_submission_order["school"].append(school)
            secondary_submission_order["profile"].append(profile)

            # Grab school stats entry
            school_stats = School_Stats.query.filter_by(school_id=school.school_id).first()

            # Process if hard deadline
            if school.hard_secondary_submission_days and school.hard_secondary_submission_days != -1:
                deadline = school.secondary_received + timedelta(days=school.hard_secondary_submission_days)
                secondary_submission_order["recommended_submission"].append(deadline)
                secondary_submission_order["hard_soft"].append("hard")
            else:
                if school.phd == False:
                    deadline = school_stats.last_complete_reg_for_ii
                else:
                    deadline = school_stats.last_complete_phd_for_ii
                secondary_submission_order["recommended_submission"].append(deadline)
                secondary_submission_order["hard_soft"].append("soft")
        secondary_suggestion_order = pd.DataFrame(secondary_submission_order).sort_values(by=["recommended_submission", "hard_soft"])
        if len(secondary_suggestion_order) > 0 and not secondary_suggestion_order["recommended_submission"].isnull().all():
            secondary_suggestion_order["recommended_submission"] = secondary_suggestion_order["recommended_submission"].dt.strftime('%b %d')
            secondary_suggestion_unknown = secondary_suggestion_order[secondary_suggestion_order["recommended_submission"].isnull()].reset_index(drop=True)
            secondary_suggestion_order = secondary_suggestion_order.dropna(subset=["recommended_submission"]).reset_index(drop=True)
        elif len(secondary_suggestion_order) > 0:
            secondary_suggestion_unknown = secondary_suggestion_order[
                secondary_suggestion_order["recommended_submission"].isnull()].reset_index(drop=True)
            secondary_suggestion_order = secondary_suggestion_order.dropna(
                subset=["recommended_submission"]).reset_index(drop=True)
        else:
            secondary_suggestion_unknown = pd.DataFrame()
    else:
        dates = None
        secondary_suggestion_order = None
        secondary_suggestion_unknown = None


    return render_template('lists.html', user=current_user, cycle=cycle, schools=schools, phd_applicant=phd_applicant,
                           usmd_school_list=form_options.get_md_schools('USA'),
                           camd_school_list=form_options.get_md_schools('CAN'),
                           do_school_list=form_options.get_do_schools(), program_types=program_types, today=datetime.today(),
                           most_recent=dates, schools_to_add_secondary_cost=schools_to_add_secondary_cost,
                           curr_cycle=form_options.VALID_CYCLES[0], missing_hard_delay_cutoff=missing_hard_delay_cutoff,
                           secondary_suggestion_order=secondary_suggestion_order, secondary_suggestion_unknown=secondary_suggestion_unknown)





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

                # Check to make sure dates are in range
                for column in cycle_data.columns[1:len(cycle_data.columns)]:
                    # Check minimum date
                    if pd.Series(pd.to_datetime(cycle_data[column].dropna()) < pd.to_datetime(
                            str(cycle.cycle_year - 1) + '-05-01')).any():
                        flash('Your spreadsheet contains dates before the beginning of the ' + str(cycle.cycle_year) +
                              ' cycle. Please check your dates and make sure that all dates are entered in the "MM/DD/YYYY" format.',
                              category='error')
                        return redirect(url_for('dashboard.cycles'))
                    # Check maximum date
                    if pd.Series(pd.to_datetime(cycle_data[column].dropna()) > pd.to_datetime(
                            str(cycle.cycle_year) + '-08-31')).any():
                        flash('Your spreadsheet contains dates beyond the end of the ' + str(cycle.cycle_year) +
                              ' cycle. Please check your dates and make sure that all dates are entered in the "MM/DD/YYYY" format.',
                              category='error')
                        return redirect(url_for('dashboard.cycles'))
                    # Check for future dates
                    if pd.Series(pd.to_datetime(cycle_data[column].dropna()) > datetime.today()).any():
                        flash('Your spreadsheet contains future dates. Please remove them and try again.',
                              category='error')
                        return redirect(url_for('dashboard.cycles'))

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

                # Check to make sure dates are in range
                for column in cycle_data.columns[1:len(cycle_data.columns)]:
                    # Check minimum date
                    if pd.Series(pd.to_datetime(cycle_data[column].dropna()) < pd.to_datetime(str(cycle.cycle_year-1) + '-05-01')).any():
                        flash('Your spreadsheet contains dates before the beginning of the ' + str(cycle.cycle_year) +
                              ' cycle. Please check your dates and make sure that all dates are entered in the "MM/DD/YYYY" format.',
                              category='error')
                        return redirect(url_for('dashboard.cycles'))
                    # Check maximum date
                    if pd.Series(pd.to_datetime(cycle_data[column].dropna()) > pd.to_datetime(str(cycle.cycle_year) + '-08-31')).any():
                        flash('Your spreadsheet contains dates beyond the end of the ' + str(cycle.cycle_year) +
                              ' cycle. Please check your dates and make sure that all dates are entered in the "MM/DD/YYYY" format.',
                              category='error')
                        return redirect(url_for('dashboard.cycles'))
                    # Check for future dates
                    if pd.Series(pd.to_datetime(cycle_data[column].dropna()) > datetime.today()).any():
                        flash('Your spreadsheet contains future dates. Please remove them and try again.',
                              category='error')
                        return redirect(url_for('dashboard.cycles'))

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
                    school_id = School_Profiles_Data.query.filter_by(school=school_name).first().school_id
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
                        pre_int_hold = row['pre_int_hold']
                        if pd.isnull(pre_int_hold): pre_int_hold = None
                    except Exception:
                        pre_int_hold = None
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
                    school = School.query.filter_by(school_id=school_id, phd=dual_degree_phd, cycle_id=cycle_id).first()
                    if school:
                        if primary: school.primary = primary
                        if secondary_received: school.secondary_received = secondary_received
                        if application_complete: school.application_complete = application_complete
                        if pre_int_hold: school.pre_int_hold = pre_int_hold
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
                                              pre_int_hold=pre_int_hold,
                                              interview_received=interview_received, interview_date=interview_date,
                                              rejection=rejection, waitlist=waitlist, acceptance=acceptance,
                                              withdrawn=withdrawn, school_id=school_id))
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
    cycle_data = (pd.read_sql(School.query.filter_by(cycle_id=cycle_id).statement, db.get_engine()))

    # Adjust the names to be more legible
    def adjust_name(row):
        adjusted = f"{row['name']}"
        if row['phd'] == 1:
            adjusted += f" {row['school_type']}-PhD"
        return adjusted

    cycle_data['name'] = cycle_data.apply(adjust_name, axis=1)
    # Drop unnecessary columns
    cycle_data = cycle_data.drop(['id', 'cycle_id', 'user_id', 'school_type', 'phd', 'school_id', 'hard_secondary_submission_days'], axis=1)

    # Rename headers
    cycle_data = cycle_data.set_axis(['Name', "Primary Submitted", "Secondary Received", "Application Complete",
                                      "Pre-Interview Hold", "Interview Received", "Interview Date", "Rejection",
                                      "Waitlist", "Acceptance", "Withdrawn", "Note"], axis=1)

    csv = cycle_data.to_csv(index=False, encoding='utf-8')
    # Generate response/download
    response = Response(csv, mimetype='text/csv')
    response.headers.set("Content-Disposition", "attachment", filename=f'{cycle.cycle_year}_school_list.csv')
    return response


@dashboard.route('/suggestions', methods=['GET', 'POST'])
@login_required
def suggestions():
    if request.method == 'POST':
        form_type = request.form.get('form_type')
        content = request.form.get('content')
        if form_type and content:
            # Send email to us with suggestion
            email = Message(f'{form_type} on {date.today().strftime("%B %d, %Y")}',
                            sender=(f'CycleTrack {form_type}',
                                    f'admin@cycletrack.org'),
                            recipients=['admin@cycletrack.org'],
                            reply_to=current_user.email)
            email.body = f'Form Type: {form_type}\n\n{content}'
            mail.send(email)

            flash(
                f'Your {form_type.lower()} has been received. We may contact you if we have further questions.',
                category='success')
            return redirect(url_for('dashboard.cycles'))
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
            for profile_item in User_Profiles.query.filter_by(cycle_id=cycle.id).all():
                db.session.delete(profile_item)
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
    cycle_data = pd.read_sql(School.query.filter_by(cycle_id=cycle.id).statement, db.get_engine())
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

    app_types.append("All")

    # Vis Generation
    vis_type = request.form.get('vis_type')
    # Default to no graph and no settings saved
    save_settings = {'vis_type': None, 'app_type': None, 'color_type': None, 'plot_title': None, 'filters': None,
                     'map_type': None, 'demographics': None, 'anonymize_demographics': None, 'custom_text': None,
                     'hide_names': None, 'organize_y': None}
    graphJSON = None
    sankeymatic = None
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
        hide_names = request.form.get("hide_names")
        organize_y = request.form.get("organize_y")
        no_action = request.form.get("no_action")
        # Default to no stats
        if demographics and not anonymize_demographics:
            if not cycle.mcat_total and not cycle.cgpa and not cycle.sgpa and not cycle.home_state:
                flash('You have not added your demographics yet. Please add them using the "cycles" page.',
                      category='error')
                stats = None
            else:
                stats = {'mcat': cycle.mcat_total, 'cgpa': cycle.cgpa, 'sgpa': cycle.sgpa, 'state': cycle.home_state}
        elif demographics and anonymize_demographics:
            if not cycle.mcat_total and not cycle.cgpa and not cycle.sgpa and not cycle.home_state:
                flash('You have not added your demographics yet. Please add them using the "cycles" page.',
                      category='error')
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
                         'no_action': no_action,
                         'anonymize_demographics': anonymize_demographics, 'filters': {}, 'custom_text': custom_text,
                         'hide_names':hide_names, 'organize_y': organize_y}

        # Grab filters
        filter_types = {'primary': None, 'secondary_received': None, 'application_complete': None,
                        'interview_received': None, 'interview_date': None, 'rejection': None, 'waitlist': None,
                        'acceptance': None, 'withdrawn': None}

        # Apply data filters and save
        if request.form.get(f'exclude-selection'):
            filters = request.form.getlist('exclude-selection')
            filters = [element.replace("exclude-", "") for element in filters]
            for filter in filters:
                cycle_data = cycle_data.drop([filter], axis=1)
                save_settings['filters'][filter] = True
        
        # Filter by PhD
        if app_type == "All":
            cycle_data = cycle_data
        elif app_type == 'Dual Degree':
            cycle_data = cycle_data[cycle_data['phd'] == True]
        else:
            cycle_data = cycle_data[cycle_data['phd'] == False]

        # Filter MD or DO
        if app_type == "All":
            cycle_data = combine_app_types.combine(cycle_data)
        elif app_type == 'MD' or app_type == 'MD Only':
            cycle_data = cycle_data[cycle_data['school_type'] == 'MD']
        elif app_type == 'DO' or app_type == 'DO Only':
            cycle_data = cycle_data[cycle_data['school_type'] == 'DO']

        # Drop extra information
        cycle_data.drop(['id', 'cycle_id', 'user_id', 'school_type', 'phd', 'note', 'school_id', 'pre_int_hold', 'hard_secondary_submission_days'], axis=1, inplace=True)
        # Drop empty columns
        cycle_data = cycle_data.dropna(axis=1, how='all')

        # Get visualization JSON
        if len(cycle_data.columns) > 1:
            if vis_type.lower() == 'dot':
                graphJSON = dot.generate(cycle_data, plot_title, stats, color=color_type.lower(),
                                         custom_text=save_settings['custom_text'],hide_school_names=hide_names,
                                         organize=save_settings['organize_y'])
            elif vis_type.lower() == 'line':
                graphJSON = line.generate(cycle_data, plot_title, stats, color=color_type.lower(),
                                          custom_text=save_settings['custom_text'])
            elif vis_type.lower() == 'bar':
                graphJSON = bar.generate(cycle_data, plot_title, stats, color=color_type.lower(),
                                         custom_text=save_settings['custom_text'])
            elif vis_type.lower() == 'sankey':
                graphJSON, sankeymatic = sankey.generate(cycle_data, plot_title, stats, color=color_type.lower(),no_action = no_action,
                                            custom_text=save_settings['custom_text'])
            elif vis_type.lower() == 'map':
                graphJSON = map.generate(cycle_data, plot_title, stats, app_type=app_type.lower(), color=color_type.lower(),
                                         map_scope=map_type.lower(), custom_text=save_settings['custom_text'])
            elif vis_type.lower() == 'timeline':
                graphJSON = horz_bar.generate(cycle_data, cycle.cycle_year, plot_title, stats, color=color_type.lower(),
                                        custom_text=save_settings['custom_text'],hide_school_names=hide_names,
                                        organize=save_settings['organize_y'])
        else:
            flash(f'Your selected school list for {cycle.cycle_year} does not have any dates yet!', category='error')

    return render_template('visualizations.html', user=current_user, cycle=cycle, app_types=app_types,
                           vis_types=form_options.VIS_TYPES, color_types=form_options.COLOR_TYPES, graphJSON=graphJSON,
                           save_settings=save_settings, map_types=form_options.MAP_TYPES, filter_options = form_options.FILTER_OPTIONS_VIS,
                           organize_y_options=form_options.ORGANIZE_Y_OPTIONS, sankeymatic=sankeymatic)


@dashboard.route('/gpa', methods=['GET'])
@login_required
def gpa():
    # Grab course list
    user_courses = Courses.query.filter_by(user_id=current_user.id).order_by(Courses.year.asc(), Courses.term.asc(), Courses.course.asc())

    # Create dictionaries for GPAs
    amcas_gpa = {'cumulative': gpa_calculators.amcas_gpa(user_courses, 'cumulative'),
                 'science': gpa_calculators.amcas_gpa(user_courses, 'science'),
                 'nonscience': gpa_calculators.amcas_gpa(user_courses, 'nonscience')
                 }

    aacomas_gpa = {'cumulative': gpa_calculators.aacomas_gpa(user_courses, 'cumulative'),
                 'science': gpa_calculators.aacomas_gpa(user_courses, 'science'),
                 'nonscience': gpa_calculators.aacomas_gpa(user_courses, 'nonscience')
                 }

    tmdsas_gpa = {'cumulative': gpa_calculators.tmdsas_gpa(user_courses, 'cumulative'),
                   'science': gpa_calculators.tmdsas_gpa(user_courses, 'science'),
                   'nonscience': gpa_calculators.tmdsas_gpa(user_courses, 'nonscience')
                   }

    # Create GPA graph
    if len(user_courses.all()) > 0:
        graphJSON = gpa_graph.generate(user_courses)
    else:
        graphJSON = None

    return render_template('gpa_calc.html', user=current_user, grades=form_options.GRADE_OPTIONS,
                           classifications=form_options.COURSE_CLASSIFICATIONS, terms=form_options.COURSE_TERMS,
                           years=form_options.COURSE_YEARS, user_courses=user_courses.all(),
                           amcas_science=form_options.AMCAS_SCIENCE, program_types=form_options.PROGRAM_TYPES,
                           amcas_gpa=amcas_gpa, aacomas_gpa=aacomas_gpa, tmdsas_gpa=tmdsas_gpa, graphJSON=graphJSON)

@dashboard.route('/add_course', methods=['POST'])
@login_required
def add_course():
    # Handle adding classes
    if request.form.get('add_course'):
        # Make sure have all other info
        if request.form.get('course') and request.form.get('credits') and request.form.get('grade') \
                and request.form.get('classification') and request.form.get('term') and request.form.get('year') \
                and request.form.get('prog_type'):

            # Check that credits is a number
            try:
                float(request.form.get('credits'))
            except ValueError as e:
                flash('The number of credits must be a number.', category='error')
                return redirect(url_for('dashboard.gpa'))

            new_course = Courses(course=request.form.get('course'), credits=request.form.get('credits'),
                                 classification=request.form.get('classification'),
                                 year=request.form.get('year'), grade=request.form.get('grade'),
                                 user_id=current_user.id, program_type=request.form.get('prog_type'))
            # Assign terms
            if request.form.get('term') == 'Summer':
                new_course.term = 0
            elif request.form.get('term') == 'Fall':
                new_course.term = 1
            elif request.form.get('term') == 'Winter':
                new_course.term = 2
            elif request.form.get('term') == 'Spring':
                new_course.term = 3

            # Assign AACOMAS science
            if request.form.get('aacomas_science'):
                new_course.aacomas_science = True
            else:
                new_course.aacomas_science = False
            # Assign TMDSAS science
            if request.form.get('tmdsas_science'):
                new_course.tmdsas_science = True
            else:
                new_course.tmdsas_science = False
            # Check if quarter
            if request.form.get('quarter'):
                new_course.quarter = True
            else:
                new_course.quarter = False
            db.session.add(new_course)
            db.session.commit()
        else:
            flash('Please make sure to fill in all fields when entering a course.', category='error')

    # Handle editing classes
    if request.form.get('edit_course'):
        if request.form.get('course') and request.form.get('credits') and request.form.get('course_id'):
            # Check that credits is a number
            try:
                float(request.form.get('credits'))
            except ValueError as e:
                flash('The number of credits must be a number.', category='error')
                return redirect(url_for('dashboard.gpa'))

            # Find course
            course = Courses.query.filter_by(id=request.form.get('course_id')).first()

            # Edit properties to new values
            course.course = request.form.get('course')
            course.credits = request.form.get('credits')
            course.classification = request.form.get('classification')
            course.year = request.form.get('year')
            course.grade = request.form.get('grade')
            course.program_type = request.form.get('prog_type')
            # Assign term
            if request.form.get('term') == 'Summer':
                course.term = 0
            elif request.form.get('term') == 'Fall':
                course.term = 1
            elif request.form.get('term') == 'Winter':
                course.term = 2
            elif request.form.get('term') == 'Spring':
                course.term = 3
            # Assign AACOMAS science
            if request.form.get('aacomas_science'):
                course.aacomas_science = True
            else:
                course.aacomas_science = False
            # Assign TMDSAS science
            if request.form.get('tmdsas_science'):
                course.tmdsas_science = True
            else:
                course.tmdsas_science = False
            # Check if quarter
            if request.form.get('quarter'):
                course.quarter = True
            else:
                course.quarter = False

            db.session.commit()
        else:
            flash('Please make sure the course name and number of credits are not blank.', category='error')
    return redirect(url_for('dashboard.gpa'))


@dashboard.route('/delete-class', methods=['POST'])
def delete_class():
    course = json.loads(request.data)
    courseId = course['courseId']
    course = Courses.query.get(courseId)
    if course:
        db.session.delete(course)
        db.session.commit()
        return jsonify({})

