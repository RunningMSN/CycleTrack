import pandas as pd
import statistics
from datetime import datetime, timedelta
import os
import traceback
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


def update_stats(app):
    '''Updates the statistics for all schools.'''
    with app.app_context():
        from .. import db
        from ..models import School_Profiles_Data, School, School_Stats, Cycle
        for school in School_Profiles_Data.query.all():
            try:
                # Query info about the school
                query = db.session.query(School, Cycle).filter(School.name == school.school).join(Cycle,
                                                                                                  School.cycle_id == Cycle.id)
                reg_data = pd.read_sql(query.filter(School.phd == False).statement, db.get_engine())
                phd_data = pd.read_sql(query.filter(School.phd == True).statement, db.get_engine())

                # Grab the school stats entry and run all calculations
                school_stats_entry = School_Stats.query.filter_by(school_id=school.school_id).first()

                # If there isn't an entry in school stats, create one
                if not school_stats_entry:
                    school_stats_entry = School_Stats(school_id=school.school_id)
                    db.session.add(school_stats_entry)

                # Run calculations
                school_stats_entry.last_updated = datetime.now()
                school_stats_entry.reg_apps_count = count_apps(reg_data)
                school_stats_entry.reg_interviews_count = count_interviews(reg_data)
                school_stats_entry.reg_perc_interviewed, school_stats_entry.reg_perc_interviewed_n = percent_interviewed(
                    reg_data)
                school_stats_entry.reg_med_interviewed_cgpa, school_stats_entry.reg_med_interviewed_cgpa_range, school_stats_entry.reg_med_interviewed_cgpa_n = cgpa_interviewed(
                    reg_data)
                school_stats_entry.reg_med_interviewed_sgpa, school_stats_entry.reg_med_interviewed_sgpa_range, school_stats_entry.reg_med_interviewed_sgpa_n = sgpa_interviewed(
                    reg_data)
                school_stats_entry.reg_med_interviewed_mcat, school_stats_entry.reg_med_interviewed_mcat_range, school_stats_entry.reg_med_interviewed_mcat_n = mcat_interviewed(
                    reg_data)
                school_stats_entry.reg_med_days_secondary_ii, school_stats_entry.reg_med_days_secondary_ii_range, school_stats_entry.reg_med_days_secondary_ii_n = secondary_to_ii(
                    reg_data)
                school_stats_entry.reg_med_days_interview_waitlist, school_stats_entry.reg_med_days_interview_waitlist_range, school_stats_entry.reg_med_days_interview_waitlist_n = interview_to_waitlist(
                    reg_data)
                school_stats_entry.reg_med_days_interview_rejection, school_stats_entry.reg_med_days_interview_rejection_range, school_stats_entry.reg_med_days_interview_rejection_n = interview_to_rejection(
                    reg_data)
                school_stats_entry.reg_med_days_interview_accepted, school_stats_entry.reg_med_days_interview_accepted_range, school_stats_entry.reg_med_days_interview_accepted_n = interview_to_acceptance(
                    reg_data)
                school_stats_entry.reg_med_days_waitlist_accepted, school_stats_entry.reg_med_days_waitlist_accepted_range, school_stats_entry.reg_med_days_waitlist_accepted_n = waitlist_to_acceptance(
                    reg_data)
                school_stats_entry.reg_acceptance_count = count_acceptance(reg_data)
                school_stats_entry.reg_perc_accepted_interviewed, school_stats_entry.reg_perc_accepted_interviewed_n = percent_interviewed_accepted(
                    reg_data)
                school_stats_entry.reg_perc_accepted_waitlist, school_stats_entry.reg_perc_accepted_waitlist_n = percent_waitlist_accepted(
                    reg_data)
                school_stats_entry.reg_med_accepted_cgpa, school_stats_entry.reg_med_accepted_cgpa_range, school_stats_entry.reg_med_accepted_cgpa_n = cgpa_accepted(
                    reg_data)
                school_stats_entry.reg_med_accepted_sgpa, school_stats_entry.reg_med_accepted_sgpa_range, school_stats_entry.reg_med_accepted_sgpa_n = sgpa_accepted(
                    reg_data)
                school_stats_entry.reg_med_accepted_mcat, school_stats_entry.reg_med_accepted_mcat_range, school_stats_entry.reg_med_accepted_mcat_n = mcat_accepted(
                    reg_data)
                school_stats_entry.phd_apps_count = count_apps(phd_data)
                school_stats_entry.phd_interviews_count = count_interviews(phd_data)
                school_stats_entry.phd_perc_interviewed, school_stats_entry.phd_perc_interviewed_n = percent_interviewed(
                    phd_data)
                school_stats_entry.phd_med_interviewed_cgpa, school_stats_entry.phd_med_interviewed_cgpa_range, school_stats_entry.phd_med_interviewed_cgpa_n = cgpa_interviewed(
                    phd_data)
                school_stats_entry.phd_med_interviewed_sgpa, school_stats_entry.phd_med_interviewed_sgpa_range, school_stats_entry.phd_med_interviewed_sgpa_n = sgpa_interviewed(
                    phd_data)
                school_stats_entry.phd_med_interviewed_mcat, school_stats_entry.phd_med_interviewed_mcat_range, school_stats_entry.phd_med_interviewed_mcat_n = mcat_interviewed(
                    phd_data)
                school_stats_entry.phd_med_days_secondary_ii, school_stats_entry.phd_med_days_secondary_ii_range, school_stats_entry.phd_med_days_secondary_ii_n = secondary_to_ii(
                    phd_data)
                school_stats_entry.phd_med_days_interview_waitlist, school_stats_entry.phd_med_days_interview_waitlist_range, school_stats_entry.phd_med_days_interview_waitlist_n = interview_to_waitlist(
                    phd_data)
                school_stats_entry.phd_med_days_interview_rejection, school_stats_entry.phd_med_days_interview_rejection_range, school_stats_entry.phd_med_days_interview_rejection_n = interview_to_rejection(
                    phd_data)
                school_stats_entry.phd_med_days_interview_accepted, school_stats_entry.phd_med_days_interview_accepted_range, school_stats_entry.phd_med_days_interview_accepted_n = interview_to_acceptance(
                    phd_data)
                school_stats_entry.phd_med_days_waitlist_accepted, school_stats_entry.phd_med_days_waitlist_accepted_range, school_stats_entry.phd_med_days_waitlist_accepted_n = waitlist_to_acceptance(
                    phd_data)
                school_stats_entry.phd_acceptance_count = count_acceptance(phd_data)
                school_stats_entry.phd_perc_accepted_interviewed, school_stats_entry.phd_perc_accepted_interviewed_n = percent_interviewed_accepted(
                    phd_data)
                school_stats_entry.phd_perc_accepted_waitlist, school_stats_entry.phd_perc_accepted_waitlist_n = percent_waitlist_accepted(
                    phd_data)
                school_stats_entry.phd_med_accepted_cgpa, school_stats_entry.phd_med_accepted_cgpa_range, school_stats_entry.phd_med_accepted_cgpa_n = cgpa_accepted(
                    phd_data)
                school_stats_entry.phd_med_accepted_sgpa, school_stats_entry.phd_med_accepted_sgpa_range, school_stats_entry.phd_med_accepted_sgpa_n = sgpa_accepted(
                    phd_data)
                school_stats_entry.phd_med_accepted_mcat, school_stats_entry.phd_med_accepted_mcat_range, school_stats_entry.phd_med_accepted_mcat_n = mcat_accepted(
                    phd_data)
                school_stats_entry.reg_interview_date, school_stats_entry.reg_waitlist_date, school_stats_entry.reg_acceptance_date, school_stats_entry.phd_interview_date, school_stats_entry.phd_waitlist_date, school_stats_entry.phd_acceptance_date = most_recent(reg_data,phd_data)

                # Generate graphs
                cycle_status_graphs(reg_data, phd_data, school_stats_entry)
                interview_acceptance_graphs(reg_data, phd_data, school_stats_entry)

                db.session.commit()
            except Exception as e:
                print(f"Error when updating: {school.official_name} ({school.school_id})")
                print(traceback.print_exc())

def count_apps(df):
    '''Returns total applications.'''
    return len(df)

def count_interviews(df):
    '''Returns number of interviews received.'''
    return len(df['interview_received'].dropna())

def percent_interviewed(df):
    '''Returns percent of completed applications that received an interview.'''
    percent_interviewed = None
    # Percent of applicants who complete app interviewed
    apps_interview = df[['application_complete', 'interview_received']].dropna(how='all')
    apps_interview = apps_interview[
        apps_interview['application_complete'].notna()]  # Ignore people who didn't fill in app complete
    if len(apps_interview['application_complete']) > 0:
        percent_interviewed = len(apps_interview['interview_received'].dropna()) / len(
            apps_interview['application_complete'].dropna()) * 100
    return percent_interviewed, len(apps_interview)

def cgpa_interviewed(df):
    '''Returns median cGPA, range, and count.'''
    interviewed_cgpa = df[['interview_received', 'cgpa']].dropna(how='any')['cgpa']
    n = len(interviewed_cgpa)
    median = None
    range = None
    if n > 0:
        median = statistics.median(interviewed_cgpa)
        range = f"{min(interviewed_cgpa):.2f} - {max(interviewed_cgpa):.2f}"
    return median, range, n

def sgpa_interviewed(df):
    '''Returns median sGPA, range, and count.'''
    interviewed_sgpa = df[['interview_received', 'sgpa']].dropna(how='any')['sgpa']
    n = len(interviewed_sgpa)
    median = None
    range = None
    if n > 0:
        median = statistics.median(interviewed_sgpa)
        range = f"{min(interviewed_sgpa):.2f} - {max(interviewed_sgpa):.2f}"
    return median, range, n

def mcat_interviewed(df):
    '''Returns median MCAT, range, and count.'''
    interviewed_mcat = df[['interview_received', 'mcat_total']].dropna(how='any')['mcat_total']
    n = len(interviewed_mcat)
    median = None
    range = None
    if n > 0:
        median = statistics.median(interviewed_mcat)
        range = f"{min(interviewed_mcat):.2f} - {max(interviewed_mcat):.2f}"
    return median, range, n

def secondary_to_ii(df):
    '''Returns median, range and number of entries of days from secondary receipt to interview.'''
    df['secondary_received'] = pd.to_datetime(df['secondary_received'])
    df['interview_received'] = pd.to_datetime(df['interview_received'])
    secondary_to_interview = (df['interview_received'] - df['secondary_received']).dropna().dt.days.tolist()
    n = len(secondary_to_interview)
    median = None
    range = None
    if n > 0:
        median = statistics.median(secondary_to_interview)
        range = f"{min(secondary_to_interview):.2f} - {max(secondary_to_interview):.2f}"
    return median, range, n

def interview_to_waitlist(df):
    '''Returns median, range and number of entries of days from interview to waitlist.'''
    df['interview_date'] = pd.to_datetime(df['interview_date'])
    df['waitlist'] = pd.to_datetime(df['waitlist'])
    int_to_wl = (df['waitlist'] - df['interview_date']).dropna().dt.days.tolist()
    n = len(int_to_wl)
    median = None
    range = None
    if n > 0:
        median = statistics.median(int_to_wl)
        range = f"{min(int_to_wl):.2f} - {max(int_to_wl):.2f}"
    return median, range, n

def interview_to_rejection(df):
    '''Returns median, range and number of entries of days from interview to rejection.'''
    df['interview_date'] = pd.to_datetime(df['interview_date'])
    df['rejection'] = pd.to_datetime(df['rejection'])
    int_to_r = (df['rejection'] - df['interview_date']).dropna().dt.days.tolist()
    n = len(int_to_r)
    median = None
    range = None
    if n > 0:
        median = statistics.median(int_to_r)
        range = f"{min(int_to_r):.2f} - {max(int_to_r):.2f}"
    return median, range, n

def interview_to_acceptance(df):
    '''Returns median, range and number of entries of days from interview to acceptance.'''
    df['interview_date'] = pd.to_datetime(df['interview_date'])
    df['acceptance'] = pd.to_datetime(df['acceptance'])
    int_to_a = (df['acceptance'] - df['interview_date']).dropna().dt.days.tolist()
    n = len(int_to_a)
    median = None
    range = None
    if n > 0:
        median = statistics.median(int_to_a)
        range = f"{min(int_to_a):.2f} - {max(int_to_a):.2f}"
    return median, range, n

def waitlist_to_acceptance(df):
    '''Returns median, range and number of entries of days from waitlist to acceptance.'''
    df['waitlist'] = pd.to_datetime(df['waitlist'])
    df['acceptance'] = pd.to_datetime(df['acceptance'])
    wl_to_a = (df['acceptance'] - df['waitlist']).dropna().dt.days.tolist()
    n = len(wl_to_a)
    median = None
    range = None
    if n > 0:
        median = statistics.median(wl_to_a)
        range = f"{min(wl_to_a):.2f} - {max(wl_to_a):.2f}"
    return median, range, n

def count_acceptance(df):
    '''Returns number of acceptances received.'''
    return len(df['acceptance'].dropna())

def percent_interviewed_accepted(df):
    '''Returns percent of interviewed applications that received an acceptance.'''
    percent_interviewed_accepted = None

    # Set rejected if did not self update, this is not perfect as rejecting users who potentially just stopped tracking
    def reject_by_time(row):
        if pd.isna(row['acceptance']) and datetime.today() > pd.Timestamp(f"{row['cycle_year']}-06-01"):
            row['rejection'] = datetime.today()
        return row
    df = df.apply(reject_by_time, axis=1)
    # Filter to only people who completed cycle
    df = df[df['acceptance'].notna() | df['rejection'].notna()]

    # Percent of applicants who complete app interviewed
    apps_interviewed_accepted = df[['acceptance', 'interview_received']].dropna(how='all')
    apps_interviewed_accepted = apps_interviewed_accepted[
        apps_interviewed_accepted['interview_received'].notna()]  # Ignore people who didn't fill in app complete
    if len(apps_interviewed_accepted['interview_received']) > 0:
        percent_interviewed_accepted = len(apps_interviewed_accepted['acceptance'].dropna()) / len(
            apps_interviewed_accepted['interview_received'].dropna()) * 100
    return percent_interviewed_accepted, len(apps_interviewed_accepted)

def percent_waitlist_accepted(df):
    '''Returns percent of waitlisted applications that received an acceptance.'''
    percent_waitlist_accepted = None
    # Percent of applicants who complete app interviewed
    apps_waitlist_accepted = df[['acceptance', 'waitlist']].dropna(how='all')
    apps_waitlist_accepted = apps_waitlist_accepted[
        apps_waitlist_accepted['waitlist'].notna()]  # Ignore people who didn't fill in app complete
    if len(apps_waitlist_accepted['waitlist']) > 0:
        percent_waitlist_accepted = len(apps_waitlist_accepted['acceptance'].dropna()) / len(
            apps_waitlist_accepted['waitlist'].dropna()) * 100
    return percent_waitlist_accepted, len(apps_waitlist_accepted)

def cgpa_accepted(df):
    '''Returns median cGPA, range, and count.'''
    accepted_cgpa = df[['acceptance', 'cgpa']].dropna(how='any')['cgpa']
    n = len(accepted_cgpa)
    median = None
    range = None
    if n > 0:
        median = statistics.median(accepted_cgpa)
        range = f"{min(accepted_cgpa):.2f} - {max(accepted_cgpa):.2f}"
    return median, range, n

def sgpa_accepted(df):
    '''Returns median sGPA, range, and count.'''
    accepted_sgpa = df[['acceptance', 'sgpa']].dropna(how='any')['sgpa']
    n = len(accepted_sgpa)
    median = None
    range = None
    if n > 0:
        median = statistics.median(accepted_sgpa)
        range = f"{min(accepted_sgpa):.2f} - {max(accepted_sgpa):.2f}"
    return median, range, n

def mcat_accepted(df):
    '''Returns median MCAT, range, and count.'''
    accepted_mcat = df[['acceptance', 'mcat_total']].dropna(how='any')['mcat_total']
    n = len(accepted_mcat)
    median = None
    range = None
    if n > 0:
        median = statistics.median(accepted_mcat)
        range = f"{min(accepted_mcat):.2f} - {max(accepted_mcat):.2f}"
    return median, range, n

def interview_acceptance_graphs(reg_df, phd_df, school_stats_entry):
    '''Saves interview and acceptance graphs into explorer_graphs'''
    from ..visualizations import school_graphs
    school_id = school_stats_entry.school_id
    # MD/DO
    reg_interviews = school_graphs.interview_acceptance_histogram(reg_df, 'interview_received')
    reg_acceptances = school_graphs.interview_acceptance_histogram(reg_df, 'acceptance')
    # PhD
    phd_interviews = school_graphs.interview_acceptance_histogram(phd_df, 'interview_received')
    phd_acceptances = school_graphs.interview_acceptance_histogram(phd_df, 'acceptance')
    # Dictionary of graphs with names
    graphs = {f'interviews_{school_id}_reg': reg_interviews,
              f'acceptances_{school_id}_reg': reg_acceptances,
              f'interviews_{school_id}_phd': phd_interviews,
              f'acceptances_{school_id}_phd': phd_acceptances}
    # Write graphs
    for key, value in graphs.items():
        # Skip empty graphs
        if value is not None:
            # Path to graph
            path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "static", "explorer_graphs", f"{key}.JSON")
            # Remove existing graphs
            if os.path.exists(path):
                os.remove(path)
            # Add new graph
            with open(path, "w") as graph_file:
                graph_file.write(value)
    # Keep track if graphs are generated
    if reg_interviews == None:
        school_stats_entry.reg_interviews_graph = False
    else:
        school_stats_entry.reg_interviews_graph = True
    if reg_acceptances == None:
        school_stats_entry.reg_acceptance_graph = False
    else:
        school_stats_entry.reg_acceptance_graph = True
    if phd_interviews == None:
        school_stats_entry.phd_interviews_graph = False
    else:
        school_stats_entry.phd_interviews_graph = True
    if phd_acceptances == None:
        school_stats_entry.phd_acceptance_graph = False
    else:
        school_stats_entry.phd_acceptance_graph = True

def cycle_status_graphs(reg_df, phd_df, school_stats_entry):
    '''Saves cycle status graphs into explorer_graphs.'''
    from ..visualizations import school_graphs
    from ..form_options import VALID_CYCLES
    school_id = school_stats_entry.school_id
    # Current year
    curr_year_reg = school_graphs.cycle_progress(reg_df[reg_df['cycle_year'] == VALID_CYCLES[0]],
                                 VALID_CYCLES[0])
    curr_year_phd = school_graphs.cycle_progress(phd_df[phd_df['cycle_year'] == VALID_CYCLES[0]],
                                 VALID_CYCLES[0])
    # Past year
    past_year_reg = school_graphs.cycle_progress(reg_df[reg_df['cycle_year'] == VALID_CYCLES[1]],
                                 VALID_CYCLES[1])
    past_year_phd = school_graphs.cycle_progress(phd_df[phd_df['cycle_year'] == VALID_CYCLES[1]],
                                 VALID_CYCLES[1])
    # Dictionary of graphs with names
    graphs = {f'status_{school_id}_reg_curr': curr_year_reg,
              f'status_{school_id}_phd_curr': curr_year_phd,
              f'status_{school_id}_reg_prev': past_year_reg,
              f'status_{school_id}_phd_prev': past_year_phd}
    # Write graphs
    for key, value in graphs.items():
        # Skip empty graphs
        if value is not None:
            # Path to graph
            #path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "static", "explorer_graphs", f"{key}.JSON")

            path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static", "explorer_graphs", f"{key}.JSON")

            # Remove existing graphs
            if os.path.exists(path):
                os.remove(path)
            # Add new graph
            with open(path, "w") as graph_file:
                graph_file.write(value)

    # Keep track if generated graphs
    if curr_year_reg == None:
        school_stats_entry.reg_cycle_status_curr_graph = False
    else:
        school_stats_entry.reg_cycle_status_curr_graph = True
    if curr_year_phd == None:
        school_stats_entry.phd_cycle_status_curr_graph = False
    else:
        school_stats_entry.phd_cycle_status_curr_graph = True
    if past_year_reg == None:
        school_stats_entry.reg_cycle_status_prev_graph = False
    else:
        school_stats_entry.reg_cycle_status_prev_graph = True
    if past_year_phd == None:
        school_stats_entry.phd_cycle_status_prev_graph = False
    else:
        school_stats_entry.phd_cycle_status_prev_graph = True


def most_recent(reg_df,phd_df):
    '''Returns the most recent dates of interview and waitlist and acceptance for the school: regular and phd.'''
    import numpy as np
    from ..form_options import VALID_CYCLES
    # Most recent cycle
    reg_df = reg_df[reg_df['cycle_year'] == VALID_CYCLES[0]]
    phd_df = phd_df[phd_df['cycle_year'] == VALID_CYCLES[0]]
    # Most recent interview date reg
    reg_interviews = reg_df['interview_received'].dropna().max()
    reg_interviews = reg_interviews.to_pydatetime()
    # Most recent waitlist date reg
    reg_waitlist = reg_df['waitlist'].dropna().max()
    reg_waitlist = reg_waitlist.to_pydatetime()
    # Most recent acceptance date reg
    reg_acceptances = reg_df['acceptance'].dropna().max()
    reg_acceptances = reg_acceptances.to_pydatetime()
    # Most recent interview date phd
    phd_interviews = phd_df['interview_received'].dropna().max()
    phd_interviews = phd_interviews.to_pydatetime()
    # Most recent waitlist date phd
    phd_waitlist = phd_df['waitlist'].dropna().max()
    phd_waitlist = phd_waitlist.to_pydatetime()
    # Most recent acceptance date phd
    phd_acceptances = phd_df['acceptance'].dropna().max()
    phd_acceptances = phd_acceptances.to_pydatetime()

    if pd.isna(reg_interviews):
        reg_interviews = None
    if pd.isna(reg_waitlist):
        reg_waitlist = None
    if pd.isna(reg_acceptances):
        reg_acceptances = None
    if pd.isna(phd_interviews):
        phd_interviews = None
    if pd.isna(phd_waitlist):
        phd_waitlist = None
    if pd.isna(phd_acceptances):
        phd_acceptances = None
    
    return reg_interviews, reg_waitlist, reg_acceptances, phd_interviews, phd_waitlist, phd_acceptances


def update_map(app):
    from ..visualizations import agg_map
    with app.app_context():
        agg_map = agg_map.generate(app)
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static", "agg_map", "map.JSON")

        # Remove existing graphs
        if os.path.exists(path):
            os.remove(path)
        # Add new graph
        with open(path, "w") as graph_file:
            graph_file.write(agg_map)


def remove_unused_accounts(app):
    with app.app_context():
        from .. import db
        from ..models import User, Cycle
        unverified = User.query.filter_by(email_verified=False)
        for user in unverified:
            # Don't delete users with a create date if they have data
            cycle_found = Cycle.query.filter_by(user_id=user.id).first()
            if not cycle_found:
                # Check that creation date is more than 2 weeks old
                if (user.create_date is None) or (datetime.today() >= user.create_date + timedelta(days=14)):
                    # Delete the user because no cycle found
                    db.session.delete(user)
        db.session.commit()

def next_historic_interview(app):
    with app.app_context():
        from .. import db, form_options
        from ..models import School, Cycle, School_Profiles_Data, School_Stats
        today = datetime.today()

        for school in School_Profiles_Data.query.all():
            school_stats_entry = School_Stats.query.filter_by(school_id=school.school_id).first()

            # Query for all entries
            query = db.session.query(School, Cycle).filter(School.name == school.school, School.interview_received.isnot(None), School.application_complete.isnot(None)).join(Cycle,School.cycle_id == Cycle.id)
            # Filter to current and past year
            query = query.filter(Cycle.cycle_year.in_(form_options.VALID_CYCLES[0:2]))

            # PROCESS FOR REGULAR APPLICATIONS
            reg = pd.read_sql(query.filter(School.phd == False).statement, db.get_engine())
            # Check if currently interviewing for this cycle
            if len(reg) >0:
                school_stats_entry.reg_interviewing = reg['interview_received'].max() > datetime.strptime(
                    f"{form_options.VALID_CYCLES[0] - 1}-06-01", '%Y-%m-%d')
            else:
                school_stats_entry.reg_interviewing = False
            # Need at least 5 recorded interviews to find suggested dates
            if len(reg) > 5:
                # Adjust so that everything in current year
                reg[['interview_received', 'application_complete']] = reg.apply(
                    lambda row: pd.Series({
                        'interview_received': row['interview_received'] + pd.DateOffset(years=1) if row['cycle_year'] ==
                                                                                                    form_options.VALID_CYCLES[
                                                                                                        1] else row[
                            'interview_received'],
                        'application_complete': row['application_complete'] + pd.DateOffset(years=1) if row[
                                                                                                            'cycle_year'] ==
                                                                                                        form_options.VALID_CYCLES[
                                                                                                            1] else row[
                            'application_complete']
                    }),
                    axis=1
                )

                # Find next future interview with applications complete after today with buffer of 4 days
                reg_future = reg[(reg['interview_received'] > today) & (reg['application_complete'] > (today)-timedelta(days=4))]
                if len(reg_future) > 0:
                    # Grab minimum next interview date
                    min_interview_date = reg_future['interview_received'].min()
                    # Get all data of apps complete up to min interview date
                    min_date_rows = reg[reg['interview_received'] <= min_interview_date]
                    # Find maximum application submitted date for that interview
                    max_complete_index = min_date_rows['application_complete'].idxmax()
                    row = min_date_rows.loc[max_complete_index]
                    # Save data
                    school_stats_entry.next_reg_historic_ii = row['interview_received']
                    school_stats_entry.last_complete_reg_for_ii = row['application_complete']
                else:
                    school_stats_entry.next_reg_historic_ii = None
                    school_stats_entry.last_complete_reg_for_ii = None
            else:
                school_stats_entry.next_reg_historic_ii = None
                school_stats_entry.last_complete_reg_for_ii = None

                # PROCESS FOR PHD APPLICATIONS
                phd = pd.read_sql(query.filter(School.phd == True).statement, db.get_engine())
                # Check if currently interviewing for this cycle
                if len(phd) > 0:
                    school_stats_entry.phd_interviewing = reg['interview_received'].max() > datetime.strptime(
                        f"{form_options.VALID_CYCLES[0] - 1}-06-01", '%Y-%m-%d')
                else:
                    school_stats_entry.phd_interviewing = False
                # Need at least 5 recorded interviews to find suggested dates
                if len(phd) > 5:
                    # Adjust so that everything in current year
                    phd[['interview_received', 'application_complete']] = phd.apply(
                        lambda row: pd.Series({
                            'interview_received': row['interview_received'] + pd.DateOffset(years=1) if row[
                                                                                                            'cycle_year'] ==
                                                                                                        form_options.VALID_CYCLES[
                                                                                                            1] else row[
                                'interview_received'],
                            'application_complete': row['application_complete'] + pd.DateOffset(years=1) if row[
                                                                                                                'cycle_year'] ==
                                                                                                            form_options.VALID_CYCLES[
                                                                                                                1] else
                            row[
                                'application_complete']
                        }),
                        axis=1
                    )

                    # Find next future interview with applications complete after today with buffer of 4 days
                    phd_future = phd[(phd['interview_received'] > today) & (
                                phd['application_complete'] > (today) - timedelta(days=4))]
                    if len(phd_future) > 0:
                        # Grab minimum next interview date
                        min_interview_date = phd_future['interview_received'].min()
                        # Get all data of apps complete up to min interview date
                        min_date_rows = phd[phd['interview_received'] <= min_interview_date]
                        # Find maximum application submitted date for that interview
                        max_complete_index = min_date_rows['application_complete'].idxmax()
                        row = min_date_rows.loc[max_complete_index]
                        # Save data
                        school_stats_entry.next_phd_historic_ii = row['interview_received']
                        school_stats_entry.last_complete_phd_for_ii = row['application_complete']
                    else:
                        school_stats_entry.next_phd_historic_ii = None
                        school_stats_entry.last_complete_phd_for_ii = None
                else:
                    school_stats_entry.next_phd_historic_ii = None
                    school_stats_entry.last_complete_phd_for_ii = None

            db.session.commit()