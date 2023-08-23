import pandas as pd
import statistics
from datetime import datetime


def update_stats(app):
    '''Updates the statistics for all schools.'''
    with app.app_context():
        from .. import db
        from ..models import School_Profiles_Data, School, School_Stats, Cycle
        for school in School_Profiles_Data.query.all():
            # Query info about the school
            query = db.session.query(School, Cycle).filter(School.name == school.school).join(Cycle,
                                                                                              School.cycle_id == Cycle.id)
            reg_data = pd.read_sql(query.filter(School.phd == False).statement, db.session.bind)
            phd_data = pd.read_sql(query.filter(School.phd == True).statement, db.session.bind)

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
            school_stats_entry.reg_med_days_interview_waitlist, school_stats_entry.reg_med_days_interview_waitlist_range, school_stats_entry.reg_med_days_interview_waitlist_n = secondary_to_ii(
                reg_data)
            school_stats_entry.reg_med_days_interview_rejection, school_stats_entry.reg_med_days_interview_rejection_range, school_stats_entry.reg_med_days_interview_rejection_n = secondary_to_ii(
                reg_data)
            school_stats_entry.reg_med_days_interview_accepted, school_stats_entry.reg_med_days_interview_accepted_range, school_stats_entry.reg_med_days_interview_accepted_n = secondary_to_ii(
                reg_data)
            school_stats_entry.reg_med_days_waitlist_accepted, school_stats_entry.reg_med_days_waitlist_accepted_range, school_stats_entry.reg_med_days_waitlist_accepted_n = secondary_to_ii(
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
            school_stats_entry.phd_med_days_interview_waitlist, school_stats_entry.phd_med_days_interview_waitlist_range, school_stats_entry.phd_med_days_interview_waitlist_n = secondary_to_ii(
                phd_data)
            school_stats_entry.phd_med_days_interview_rejection, school_stats_entry.phd_med_days_interview_rejection_range, school_stats_entry.phd_med_days_interview_rejection_n = secondary_to_ii(
                phd_data)
            school_stats_entry.phd_med_days_interview_accepted, school_stats_entry.phd_med_days_interview_accepted_range, school_stats_entry.phd_med_days_interview_accepted_n = secondary_to_ii(
                phd_data)
            school_stats_entry.phd_med_days_waitlist_accepted, school_stats_entry.phd_med_days_waitlist_accepted_range, school_stats_entry.phd_med_days_waitlist_accepted_n = secondary_to_ii(
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

            db.session.commit()


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