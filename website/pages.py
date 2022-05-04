from flask import Blueprint, render_template
from flask_login import current_user
from . import db
from .models import User, School
from .visualizations import agg_map
import pandas as pd

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
        graphJSON = agg_map.generate()
    else:
        graphJSON = None
    return render_template('index.html', user=current_user, user_count=user_count, school_count=school_count,
                           app_count=app_count, graphJSON=graphJSON)

@pages.route('/about')
def about():
    return render_template('about.html', user=current_user)

@pages.route('/privacy')
def privacy():
    return render_template('privacy.html', user=current_user)

@pages.route('/terms')
def terms():
    return render_template('terms.html', user=current_user)

@pages.route('/changelog')
def changelog():
    return render_template('changelog.html', user=current_user)