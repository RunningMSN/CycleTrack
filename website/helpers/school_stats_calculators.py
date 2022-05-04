from .. import db
from ..models import School, School_Profiles_Data

def update_all_schools():
    '''This method updates the stats for all schools in the database.'''
    # Grab all school names
    schools = db.session.query(School_Profiles_Data.school).all()
    for school in schools:
        school_name = school.school
        # Update app counts
        count_apps_reg(school_name)
        count_apps_phd(school_name)
    return

def count_apps_reg(name):
    '''Update the count of MD/DO apps for a school.'''
    # Get school
    school_profile = School_Profiles_Data.query.filter_by(school=name).first()
    school_profile.reg_apps_count = School.query.filter_by(name=name, phd=False).count()
    db.session.commit()
    return

def count_apps_phd(name):
    '''Update the count of MD/DO-PhD apps for a school.'''
    # Get school
    school_profile = School_Profiles_Data.query.filter_by(school=name).first()
    school_profile.phd_apps_count = School.query.filter_by(name=name, phd=True).count()
    db.session.commit()
    return