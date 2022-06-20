from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user
from . import db, form_options
from .models import Cycle, School, School_Profiles_Data
from .visualizations import school_graphs
import pandas as pd
from .helpers import school_info_calcs, school_stats_calculators
from .form_options import VALID_CYCLES

explorer = Blueprint('explorer', __name__)

@explorer.route('/explorer', methods=['GET'])
def explorer_home():
    # Get info about all available schools
    all_schools = School_Profiles_Data.query.all()

    build_df = {'name': [], 'type': [], 'reg_apps': [], 'reg_med_mcat': [], 'reg_med_gpa': [],
                'phd_apps': [], 'logo_link': [], 'city': [], 'state': [], 'country': [], 'envt': [], 'pub_pri': []}

    for school in all_schools:
        # Grab number of applications
        reg_num = school.reg_apps_count
        phd_num = school.phd_apps_count
        # Skip the school if no applications
        if reg_num > 0 or phd_num > 0:
            build_df['reg_apps'].append(reg_num)
            build_df['phd_apps'].append(phd_num)

            # Grab information about school
            build_df['name'].append(school.school)
            build_df['type'].append(school.md_or_do)
            build_df['logo_link'].append(school.logo_file_name)
            build_df['city'].append(school.city)
            build_df['state'].append(school.state)
            build_df['country'].append(school.country)
            build_df['envt'].append(school.envt_type)
            build_df['pub_pri'].append(school.private_public)

            # TODO: Eventually add this back in
            build_df['reg_med_mcat'].append(0)
            build_df['reg_med_gpa'].append(0)

    # Generate dataframe
    df = pd.DataFrame(build_df).sort_values('name')

    if len(df) == 0:
        df = None
    # Render page
    return render_template('explorer.html', user=current_user, state_options=sorted(form_options.STATES_WITH_SCHOOLS),
                           state_abbrev=form_options.STATE_ABBREV,schools=df)

@explorer.route('/explorer/<school_name>')
def explore_school(school_name):
    # Find school
    school_name = school_name.replace('%20', ' ')
    if school_name not in form_options.get_md_schools() and school_name not in form_options.get_do_schools():
        flash(f'Could not find {school_name}. Please navigate to your school using the explorer.', category='error')
        return redirect(url_for('explorer.explorer'))

    # Grab school information
    school_info = School_Profiles_Data.query.filter_by(school=school_name).first()

    # Query info about the school
    query = db.session.query(School, Cycle).filter(School.name == school_name).join(Cycle, School.cycle_id == Cycle.id)
    reg_data = pd.read_sql(query.filter(School.phd == False).statement, db.session.bind)
    phd_data = pd.read_sql(query.filter(School.phd == True).statement, db.session.bind)

    # Dictionaries with all information about the school
    reg_info = {'cycle_status_json': school_graphs.cycle_progress(reg_data[reg_data['cycle_year'] == VALID_CYCLES[0]]),
                'cycle_status_json_prev': school_graphs.cycle_progress(reg_data[reg_data['cycle_year'] == VALID_CYCLES[1]]),
                'interview_graph': school_graphs.interview_acceptance_histogram(reg_data, 'interview_received'),
                'acceptance_graph': school_graphs.interview_acceptance_histogram(reg_data, 'acceptance')}
    phd_info = {'cycle_status_json': school_graphs.cycle_progress(phd_data[phd_data['cycle_year'] == VALID_CYCLES[0]]),
                'cycle_status_json_prev': school_graphs.cycle_progress(phd_data[phd_data['cycle_year'] == VALID_CYCLES[1]]),
                'interview_graph': school_graphs.interview_acceptance_histogram(phd_data, 'interview_received'),
                'acceptance_graph': school_graphs.interview_acceptance_histogram(phd_data, 'acceptance')}

    # Calculate interview information
    school_info_calcs.interview_calculations(reg_data, reg_info)
    school_info_calcs.interview_calculations(phd_data, phd_info)

    # Calculate acceptance information
    school_info_calcs.acceptance_calculations(reg_data, reg_info)
    school_info_calcs.acceptance_calculations(phd_data, phd_info)

    return render_template('school_template.html', user=current_user, school_info=school_info, reg_info=reg_info,
                           phd_info=phd_info, valid_cycles=VALID_CYCLES)

@explorer.route('/update_all')
def update_all():
    school_stats_calculators.update_all_schools()
    flash('Updated the stats for all schools in the database.', category='success')
    return redirect(url_for('pages.index'))