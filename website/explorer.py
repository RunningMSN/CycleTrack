from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user
from . import db, form_options
from .models import Cycle, School, School_Profiles_Data, School_Stats
from .visualizations import school_graphs, cycle_summary
import pandas as pd
from .form_options import VALID_CYCLES
from datetime import timedelta

explorer = Blueprint('explorer', __name__)

@explorer.route('/explorer', methods=['GET'])
def explorer_home():
    # Get info about all available schools
    all_schools = School_Profiles_Data.query.all()

    # If user is logged in, grab their schools
    applied_schools = []
    current_applicant = False
    if current_user.is_authenticated:
        # Grab most recent cycle
        cycle = db.session.query(Cycle).filter_by(user_id = current_user.id).order_by(Cycle.id.desc()).first()
        if cycle.cycle_year in [VALID_CYCLES[0], VALID_CYCLES[1]]:
            schools = pd.read_sql(School.query.filter_by(cycle_id=cycle.id).statement, db.get_engine())
            applied_schools = schools["name"].tolist()
            if len(applied_schools) > 0:
                current_applicant = True

    build_df = {'name': [], 'type': [], 'reg_apps': [],
                'phd_apps': [], 'logo_link': [], 'city': [], 'state': [], 'country': [], 'envt': [], 'pub_pri': [],
                'applied_to': []}

    for school in all_schools:
        school_stats = School_Stats.query.filter_by(school_id=school.school_id).first()

        # Grab number of applications
        reg_num = school_stats.reg_apps_count
        phd_num = school_stats.phd_apps_count
        if not reg_num:
            reg_num = 0
        if not phd_num:
            phd_num =0

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
            if school.school in applied_schools:
                build_df['applied_to'].append(True)
            else:
                build_df['applied_to'].append(False)

    # Generate dataframe
    df = pd.DataFrame(build_df).sort_values('name')

    if len(df) == 0:
        df = None
    # Render page
    return render_template('explorer.html', user=current_user, state_options=sorted(form_options.STATES_WITH_SCHOOLS),
                           state_abbrev=form_options.STATE_ABBREV,schools=df, current_applicant = current_applicant)

@explorer.route('/explorer/school/<school_name>')
def explore_school(school_name):
    # Find school
    school_name = school_name.replace('%20', ' ')
    if school_name not in form_options.get_md_schools() and school_name not in form_options.get_do_schools():
        flash(f'Could not find {school_name}. Please navigate to your school using the explorer.', category='error')
        return redirect(url_for('explorer.explorer_home'))

    # Grab school information
    school_info = School_Profiles_Data.query.filter_by(school=school_name).first()
    school_stats = School_Stats.query.filter_by(school_id=school_info.school_id).first()

    # Dictionaries with all information about the school
    reg_info = {'app_count': school_stats.reg_apps_count,
                'cycle_status_json': school_stats.reg_cycle_status_curr_graph,
                'cycle_status_json_prev': school_stats.reg_cycle_status_prev_graph,
                'interview_graph': school_stats.reg_interviews_graph,
                'acceptance_graph': school_stats.reg_acceptance_graph,
                'interview_count': school_stats.reg_interviews_count,
                'n_percent_interviewed': school_stats.reg_perc_interviewed_n,
                'percent_interviewed': school_stats.reg_perc_interviewed,
                'n_interviewed_cgpa': school_stats.reg_med_interviewed_cgpa_n,
                'interviewed_cgpa': school_stats.reg_med_interviewed_cgpa,
                'interviewed_cgpa_range': school_stats.reg_med_interviewed_cgpa_range,
                'n_interviewed_sgpa': school_stats.reg_med_interviewed_sgpa_n,
                'interviewed_sgpa': school_stats.reg_med_interviewed_sgpa,
                'interviewed_sgpa_range': school_stats.reg_med_interviewed_sgpa_range,
                'n_interviewed_mcat': school_stats.reg_med_interviewed_mcat_n,
                'interviewed_mcat': school_stats.reg_med_interviewed_mcat,
                'interviewed_mcat_range': school_stats.reg_med_interviewed_mcat_range,
                'secondary_to_ii': school_stats.reg_med_days_secondary_ii,
                'secondary_to_ii_n': school_stats.reg_med_days_secondary_ii_n,
                'secondary_to_ii_range': school_stats.reg_med_days_secondary_ii_range,
                'interview_to_wl': school_stats.reg_med_days_interview_waitlist,
                'interview_to_wl_n': school_stats.reg_med_days_interview_waitlist_n,
                'interview_to_wl_range': school_stats.reg_med_days_interview_waitlist_range,
                'interview_to_r': school_stats.reg_med_days_interview_rejection,
                'interview_to_r_range': school_stats.reg_med_days_interview_rejection_range,
                'interview_to_r_n': school_stats.reg_med_days_interview_rejection_n,
                'acceptance_count': school_stats.reg_acceptance_count,
                'n_percent_interview_accepted': school_stats.reg_perc_accepted_interviewed_n,
                'percent_interview_accepted': school_stats.reg_perc_accepted_interviewed,
                'n_percent_waitlist_accepted': school_stats.reg_perc_accepted_waitlist_n,
                'percent_waitlist_accepted': school_stats.reg_perc_accepted_waitlist,
                'n_accepted_cgpa': school_stats.reg_med_accepted_cgpa_n,
                'accepted_cgpa': school_stats.reg_med_accepted_cgpa,
                'accepted_cgpa_range': school_stats.reg_med_accepted_cgpa_range,
                'n_accepted_sgpa': school_stats.reg_med_accepted_sgpa_n,
                'accepted_sgpa': school_stats.reg_med_accepted_sgpa,
                'accepted_sgpa_range': school_stats.reg_med_accepted_sgpa_range,
                'n_accepted_mcat': school_stats.reg_med_accepted_mcat_n,
                'accepted_mcat': school_stats.reg_med_accepted_mcat,
                'accepted_mcat_range': school_stats.reg_med_accepted_mcat_range,
                'interview_to_a': school_stats.reg_med_days_interview_accepted,
                'interview_to_a_range': school_stats.reg_med_days_interview_accepted_range,
                'interview_to_a_n': school_stats.reg_med_days_interview_accepted_n,
                'wl_to_a': school_stats.reg_med_days_waitlist_accepted,
                'wl_to_a_range': school_stats.reg_med_days_waitlist_accepted_range,
                'wl_to_a_n': school_stats.reg_med_days_waitlist_accepted_n}

    phd_info = {'app_count': school_stats.phd_apps_count,
                'cycle_status_json': school_stats.phd_cycle_status_curr_graph,
                'cycle_status_json_prev': school_stats.phd_cycle_status_prev_graph,
                'interview_graph': school_stats.phd_interviews_graph,
                'acceptance_graph': school_stats.phd_acceptance_graph,
                'interview_count': school_stats.phd_interviews_count,
                'n_percent_interviewed': school_stats.phd_perc_interviewed_n,
                'percent_interviewed': school_stats.phd_perc_interviewed,
                'n_interviewed_cgpa': school_stats.phd_med_interviewed_cgpa_n,
                'interviewed_cgpa': school_stats.phd_med_interviewed_cgpa,
                'interviewed_cgpa_range': school_stats.phd_med_interviewed_cgpa_range,
                'n_interviewed_sgpa': school_stats.phd_med_interviewed_sgpa_n,
                'interviewed_sgpa': school_stats.phd_med_interviewed_sgpa,
                'interviewed_sgpa_range': school_stats.phd_med_interviewed_sgpa_range,
                'n_interviewed_mcat': school_stats.phd_med_interviewed_mcat_n,
                'interviewed_mcat': school_stats.phd_med_interviewed_mcat,
                'interviewed_mcat_range': school_stats.phd_med_interviewed_mcat_range,
                'secondary_to_ii': school_stats.phd_med_days_secondary_ii,
                'secondary_to_ii_n': school_stats.phd_med_days_secondary_ii_n,
                'secondary_to_ii_range': school_stats.phd_med_days_secondary_ii_range,
                'interview_to_wl': school_stats.phd_med_days_interview_waitlist,
                'interview_to_wl_n': school_stats.phd_med_days_interview_waitlist_n,
                'interview_to_wl_range': school_stats.phd_med_days_interview_waitlist_range,
                'interview_to_r': school_stats.phd_med_days_interview_rejection,
                'interview_to_r_range': school_stats.phd_med_days_interview_rejection_range,
                'interview_to_r_n': school_stats.phd_med_days_interview_rejection_n,
                'acceptance_count': school_stats.phd_acceptance_count,
                'n_percent_interview_accepted': school_stats.phd_perc_accepted_interviewed_n,
                'percent_interview_accepted': school_stats.phd_perc_accepted_interviewed,
                'n_percent_waitlist_accepted': school_stats.phd_perc_accepted_waitlist_n,
                'percent_waitlist_accepted': school_stats.phd_perc_accepted_waitlist,
                'n_accepted_cgpa': school_stats.phd_med_accepted_cgpa_n,
                'accepted_cgpa': school_stats.phd_med_accepted_cgpa,
                'accepted_cgpa_range': school_stats.phd_med_accepted_cgpa_range,
                'n_accepted_sgpa': school_stats.phd_med_accepted_sgpa_n,
                'accepted_sgpa': school_stats.phd_med_accepted_sgpa,
                'accepted_sgpa_range': school_stats.phd_med_accepted_sgpa_range,
                'n_accepted_mcat': school_stats.phd_med_accepted_mcat_n,
                'accepted_mcat': school_stats.phd_med_accepted_mcat,
                'accepted_mcat_range': school_stats.phd_med_accepted_mcat_range,
                'interview_to_a': school_stats.phd_med_days_interview_accepted,
                'interview_to_a_range': school_stats.phd_med_days_interview_accepted_range,
                'interview_to_a_n': school_stats.phd_med_days_interview_accepted_n,
                'wl_to_a': school_stats.phd_med_days_waitlist_accepted,
                'wl_to_a_range': school_stats.phd_med_days_waitlist_accepted_range,
                'wl_to_a_n': school_stats.phd_med_days_waitlist_accepted_n}

    app_counts = {'reg': school_stats.reg_apps_count, 'phd': school_stats.phd_apps_count}

    last_updated = school_stats.last_updated.strftime("%m/%d/%Y %H:%M:%S CST")

    return render_template('school_template.html', user=current_user, school_info=school_info, reg_info=reg_info,
                           phd_info=phd_info, valid_cycles=VALID_CYCLES, last_updated=last_updated, school_id=school_stats.school_id)


@explorer.route('/explorer/summary/<year>')
def explore_summary(year):
    # Make sure the summary is an integer.
    try:
        year = int(year)
    except:
        flash(f'An error occurred. Please try again, if you believe this is a mistake, please submit a bug report.', category='error')
        return redirect(url_for('explorer.explorer_home'))

    # Check that the year is within the past 2 cycles.
    if not (year == form_options.VALID_CYCLES[0] or year == form_options.VALID_CYCLES[1]):
        flash(f'{year} is not available. Please make sure you are viewing a valid summary page.', category='error')
        return redirect(url_for('explorer.explorer_home'))

    map = cycle_summary.map(year)

    return render_template('cycle_summary.html', user=current_user, year=year)