from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user
from . import db, form_options
from .models import Cycle, School
from .visualizations import school_table, school_graphs
import pandas as pd
from .helpers import school_info_calcs
import statistics

explorer = Blueprint('explorer', __name__)

@explorer.route('/explorer', methods=['GET', 'POST'])
def explorer_home():
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

@explorer.route('/explorer/<school_name>')
def explore_school(school_name):
    # Find school
    school_name = school_name.replace('%20', ' ')
    if school_name not in form_options.MD_SCHOOL_LIST and school_name not in form_options.DO_SCHOOL_LIST:
        flash(f'Could not find {school_name}. Please navigate to your school using the explorer.', category='error')
        return redirect(url_for('explorer.explorer'))

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
