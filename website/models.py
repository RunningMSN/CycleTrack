from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    cycles = db.relationship('Cycle')
    email_verified = db.Column(db.Boolean, default=False)
    create_date = db.Column(db.DateTime(timezone=True), nullable=True)
    last_visited = db.Column(db.DateTime(timezone=True), nullable=True)
    public_profile = db.Column(db.Boolean, default=False)
    url_hash = db.Column(db.String(150))
    privacy_announce = db.Column(db.Boolean, default=False)

class Cycle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cycle_year = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    schools = db.relationship('School')
    gender = db.Column(db.String(150), nullable=True)
    other_gender = db.Column(db.String(150), nullable=True)
    sex = db.Column(db.String(150), nullable=True)
    other_sex = db.Column(db.String(150), nullable=True)
    birth_month = db.Column(db.Integer, nullable=True)
    birth_year = db.Column(db.Integer, nullable=True)
    age = db.Column(db.Integer, nullable=True)
    race_ethnicity = db.Column(db.String(150), nullable=True)
    other_race_ethnicity = db.Column(db.String(150), nullable=True)
    home_state = db.Column(db.String(150), nullable=True)
    cgpa = db.Column(db.Float, nullable=True)
    sgpa = db.Column(db.Float, nullable=True)
    mcat_total = db.Column(db.Integer, nullable=True)
    mcat_cp = db.Column(db.Integer, nullable=True)
    mcat_cars = db.Column(db.Integer, nullable=True)
    mcat_bb = db.Column(db.Integer, nullable=True)
    mcat_ps = db.Column(db.Integer, nullable=True)
    mentoring_message = db.Column(db.Boolean, default=False)
    casper = db.Column(db.Integer, nullable=True)
    preview = db.Column(db.Integer, nullable=True)

class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cycle_id = db.Column(db.Integer, db.ForeignKey('cycle.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(150))
    school_type = db.Column(db.String(150)) # MD/DO
    phd = db.Column(db.Boolean) # Dual degree w/ PhD or not
    primary = db.Column(db.DateTime(timezone=True), nullable=True)
    secondary_received = db.Column(db.DateTime(timezone=True), nullable=True)
    application_complete = db.Column(db.DateTime(timezone=True), nullable=True)
    pre_int_hold = db.Column(db.DateTime(timezone=True), nullable=True)
    interview_received = db.Column(db.DateTime(timezone=True), nullable=True)
    interview_date = db.Column(db.DateTime(timezone=True), nullable=True)
    rejection = db.Column(db.DateTime(timezone=True), nullable=True)
    waitlist = db.Column(db.DateTime(timezone=True), nullable=True)
    acceptance = db.Column(db.DateTime(timezone=True), nullable=True)
    withdrawn = db.Column(db.DateTime(timezone=True), nullable=True)
    note = db.Column(db.Text(), nullable=True)
    school_id = db.Column(db.Integer, db.ForeignKey('school__profiles__data.school_id'))

class School_Profiles_Data(db.Model):
    school = db.Column(db.String(150), primary_key=True)
    city = db.Column(db.String(150))
    state = db.Column(db.String(150))
    country = db.Column(db.String(150))
    envt_type = db.Column(db.String(150))
    private_public = db.Column(db.String(150))
    lat = db.Column(db.Float)
    long = db.Column(db.Float)
    md_or_do = db.Column(db.String(150))
    logo_file_name = db.Column(db.String(150))
    msar_choosedo_link = db.Column(db.String(150))
    reg_website = db.Column(db.String(150))
    phd_website = db.Column(db.String(150))
    lor_reg_link = db.Column(db.String(150))
    lor_phd_link = db.Column(db.String(150))
    school_id = db.Column(db.Integer)
    official_name = db.Column(db.String(150))


class School_Stats(db.Model):
    school_id = db.Column(db.Integer, db.ForeignKey('school__profiles__data.school_id'), primary_key=True)
    last_updated = db.Column(db.DateTime(timezone=True))
    reg_apps_count = db.Column(db.Integer())
    reg_interviews_count = db.Column(db.Integer())
    reg_perc_interviewed = db.Column(db.Float)
    reg_perc_interviewed_n = db.Column(db.Integer())
    reg_med_interviewed_cgpa = db.Column(db.Float)
    reg_med_interviewed_cgpa_range = db.Column(db.String(150))
    reg_med_interviewed_cgpa_n = db.Column(db.Integer())
    reg_med_interviewed_sgpa = db.Column(db.Float)
    reg_med_interviewed_sgpa_range = db.Column(db.String(150))
    reg_med_interviewed_sgpa_n = db.Column(db.Integer())
    reg_med_interviewed_mcat = db.Column(db.Float)
    reg_med_interviewed_mcat_range = db.Column(db.String(150))
    reg_med_interviewed_mcat_n = db.Column(db.Integer())
    reg_med_days_secondary_ii = db.Column(db.Integer())
    reg_med_days_secondary_ii_range = db.Column(db.String(150))
    reg_med_days_secondary_ii_n = db.Column(db.Integer())
    reg_med_days_interview_waitlist = db.Column(db.Integer())
    reg_med_days_interview_waitlist_range = db.Column(db.String(150))
    reg_med_days_interview_waitlist_n = db.Column(db.Integer())
    reg_med_days_interview_rejection = db.Column(db.Integer())
    reg_med_days_interview_rejection_range = db.Column(db.String(150))
    reg_med_days_interview_rejection_n = db.Column(db.Integer())
    reg_acceptance_count = db.Column(db.Integer())
    reg_perc_accepted_interviewed = db.Column(db.Float)
    reg_perc_accepted_interviewed_n = db.Column(db.Integer())
    reg_perc_accepted_waitlist = db.Column(db.Float)
    reg_perc_accepted_waitlist_n = db.Column(db.Integer())
    reg_med_accepted_cgpa = db.Column(db.Float)
    reg_med_accepted_cgpa_range = db.Column(db.String(150))
    reg_med_accepted_cgpa_n = db.Column(db.Integer())
    reg_med_accepted_sgpa = db.Column(db.Float)
    reg_med_accepted_sgpa_range = db.Column(db.String(150))
    reg_med_accepted_sgpa_n = db.Column(db.Integer())
    reg_med_accepted_mcat = db.Column(db.Float)
    reg_med_accepted_mcat_range = db.Column(db.String(150))
    reg_med_accepted_mcat_n = db.Column(db.Integer())
    reg_med_days_interview_accepted = db.Column(db.Integer())
    reg_med_days_interview_accepted_range = db.Column(db.String(150))
    reg_med_days_interview_accepted_n = db.Column(db.Integer())
    reg_med_days_waitlist_accepted = db.Column(db.Integer())
    reg_med_days_waitlist_accepted_range = db.Column(db.String(150))
    reg_med_days_waitlist_accepted_n = db.Column(db.Integer())
    phd_apps_count = db.Column(db.Integer())
    phd_interviews_count = db.Column(db.Integer())
    phd_perc_interviewed = db.Column(db.Float)
    phd_perc_interviewed_n = db.Column(db.Integer())
    phd_med_interviewed_cgpa = db.Column(db.Float)
    phd_med_interviewed_cgpa_range = db.Column(db.String(150))
    phd_med_interviewed_cgpa_n = db.Column(db.Integer())
    phd_med_interviewed_sgpa = db.Column(db.Float)
    phd_med_interviewed_sgpa_range = db.Column(db.String(150))
    phd_med_interviewed_sgpa_n = db.Column(db.Integer())
    phd_med_interviewed_mcat = db.Column(db.Float)
    phd_med_interviewed_mcat_range = db.Column(db.String(150))
    phd_med_interviewed_mcat_n = db.Column(db.Integer())
    phd_med_days_secondary_ii = db.Column(db.Integer())
    phd_med_days_secondary_ii_range = db.Column(db.String(150))
    phd_med_days_secondary_ii_n = db.Column(db.Integer())
    phd_med_days_interview_waitlist = db.Column(db.Integer())
    phd_med_days_interview_waitlist_range = db.Column(db.String(150))
    phd_med_days_interview_waitlist_n = db.Column(db.Integer())
    phd_med_days_interview_rejection = db.Column(db.Integer())
    phd_med_days_interview_rejection_range = db.Column(db.String(150))
    phd_med_days_interview_rejection_n = db.Column(db.Integer())
    phd_acceptance_count = db.Column(db.Integer())
    phd_perc_accepted_interviewed = db.Column(db.Float)
    phd_perc_accepted_interviewed_n = db.Column(db.Integer())
    phd_perc_accepted_waitlist = db.Column(db.Float)
    phd_perc_accepted_waitlist_n = db.Column(db.Integer())
    phd_med_accepted_cgpa = db.Column(db.Float)
    phd_med_accepted_cgpa_range = db.Column(db.String(150))
    phd_med_accepted_cgpa_n = db.Column(db.Integer())
    phd_med_accepted_sgpa = db.Column(db.Float)
    phd_med_accepted_sgpa_range = db.Column(db.String(150))
    phd_med_accepted_sgpa_n = db.Column(db.Integer())
    phd_med_accepted_mcat = db.Column(db.Float)
    phd_med_accepted_mcat_range = db.Column(db.String(150))
    phd_med_accepted_mcat_n = db.Column(db.Integer())
    phd_med_days_interview_accepted = db.Column(db.Integer())
    phd_med_days_interview_accepted_range = db.Column(db.String(150))
    phd_med_days_interview_accepted_n = db.Column(db.Integer())
    phd_med_days_waitlist_accepted = db.Column(db.Integer())
    phd_med_days_waitlist_accepted_range = db.Column(db.String(150))
    phd_med_days_waitlist_accepted_n = db.Column(db.Integer())
    reg_cycle_status_curr_graph = db.Column(db.Boolean)
    reg_cycle_status_prev_graph = db.Column(db.Boolean)
    reg_interviews_graph = db.Column(db.Boolean)
    reg_acceptance_graph = db.Column(db.Boolean)
    phd_cycle_status_curr_graph = db.Column(db.Boolean)
    phd_cycle_status_prev_graph = db.Column(db.Boolean)
    phd_interviews_graph = db.Column(db.Boolean)
    phd_acceptance_graph = db.Column(db.Boolean)
    reg_interview_date = db.Column(db.DateTime(timezone=True), nullable=True)
    reg_waitlist_date = db.Column(db.DateTime(timezone=True), nullable=True)
    reg_acceptance_date = db.Column(db.DateTime(timezone=True), nullable=True)
    phd_interview_date = db.Column(db.DateTime(timezone=True), nullable=True)
    phd_waitlist_date = db.Column(db.DateTime(timezone=True), nullable=True)
    phd_acceptance_date = db.Column(db.DateTime(timezone=True), nullable=True)


class Courses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    course = db.Column(db.String(150))
    classification = db.Column(db.String(150))
    credits = db.Column(db.Integer())
    grade = db.Column(db.String(150))
    year = db.Column(db.String(150))
    term = db.Column(db.Integer()) # 0 = summer, 1 = fall, 2 = winter, 3 = spring
    aacomas_science = db.Column(db.Boolean)
    tmdsas_science = db.Column(db.Boolean)
    program_type = db.Column(db.String(150))
    quarter = db.Column(db.Boolean)

class User_Profiles(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    block_order = db.Column(db.Integer,nullable=True)
    block_type = db.Column(db.String(20), nullable=True)
    cycle_id = db.Column(db.Integer, db.ForeignKey('cycle.id'), nullable=True)
    cycle_year = db.Column(db.Integer, nullable=True)
    vis_type = db.Column(db.String(20), nullable=True)
    plot_title = db.Column(db.Text,nullable=True)
    app_type = db.Column(db.String(20), nullable=True)
    map_type = db.Column(db.String(20), nullable=True)
    color = db.Column(db.String(20), nullable=True)
    filter_values = db.Column(db.Text,nullable=True)
    hide_names = db.Column(db.Boolean, default=False)
    text = db.Column(db.Text, nullable=True)

class Secondary_Costs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('school__profiles__data.school_id'))
    cycle_year = db.Column(db.Integer)
    reg_cost = db.Column(db.Integer)
    reg_cost_confirmed = db.Column(db.Boolean)
    phd_cost = db.Column(db.Integer)
    phd_cost_confirmed = db.Column(db.Boolean)
    reg_to_phd = db.Column(db.Integer)
    reg_to_phd_confirmed = db.Column(db.Boolean)
    contributors = db.Column(db.String(20))