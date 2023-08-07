from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user
from . import db, form_options
from .models import Cycle, School, School_Profiles_Data
from .visualizations import summary_graphs
import pandas as pd
from .form_options import VALID_CYCLES

summary = Blueprint('summary', __name__)

@summary.route('/summary', methods=['GET'])
def summary_home():
    #go through the valid cycles and only pull if there is more than 5 users

    # Render page
    return render_template('summary.html', user=current_user,years=VALID_CYCLES)

def summary_df(year):
    # Get info about all available schools
    query = db.session.query(Cycle, School).join(School, Cycle.id==School.cycle_id)
    reg_data = pd.read_sql(query.filter(School.phd == False).statement, db.session.bind)

    columns_to_drop = ['id', 'user_id', 'name', 'withdrawn',
       'note', 'id_1', 'user_id_1', 'gender', 'sex',
       'birth_month', 'birth_year', 'race_ethnicity', 'home_state', 'cgpa',
       'sgpa', 'mcat_total', 'mcat_cp', 'mcat_cars', 'mcat_bb', 'mcat_ps',
       'mentoring_message']

    df = reg_data.drop(columns_to_drop,axis=1)
    df = df[df['cycle_year']==int(year)]
    return df

@summary.route('/summary/<cycle_year>', methods=['GET'])
def summary_page(cycle_year):
    school_info = summary_df(cycle_year)

    reg_info = {'cycle_bar_json': summary_graphs.generate_bar(school_info,"Bar",year=cycle_year)}

    return render_template('summary_template.html', user=current_user,cycle_year = cycle_year, reg_info=reg_info)

    