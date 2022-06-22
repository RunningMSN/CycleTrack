
from flask_login import current_user
from .form_options import VALID_CYCLES
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, Response, Markup
from . import db, form_options, mail
from .models import User,Cycle, School, School_Profiles_Data, Courses
from datetime import datetime, date
import pandas as pd
from .helpers import import_list_funcs, categorize_stats, school_stats_calculators, gpa_calculators
from .visualizations import public_graphs
import hashlib

profile = Blueprint('profile', __name__)

@profile.route('/profile/')
def profile_home():
    '''I just put this here for ease of use. this part generates the custom URLs based on the userid and email
    user_ids = [user.id for user in User.query.all()]
    for userid in user_ids:
        user = User.query.filter_by(id=userid).first()
        user_email = user.email.split("@")[0]
        url = hashlib.sha1(f"{userid}{user_email}".encode()).hexdigest()
        user.url_hash = url
        db.session.commit()'''
    #page to access settings or view profile

    return render_template('profile.html',user=current_user)


@profile.route('/profile/settings')
def profile_settings():
    #public or private profile
    #which graphs to show
    #graph settings
    return render_template('profile.html',user=current_user)

@profile.route('/profile/<userurl>')
def profile_page(userurl):

    user = User.query.filter_by(url_hash=userurl).first()
    userid = user.id
    if user.public_profile == False:
        #in the future make it one html file
        return render_template("profile_private.html",user=current_user)
    else:
        cycle = Cycle.query.filter_by(user_id=int(userid)).first()
        cycle_year = Cycle.query.filter_by(id=cycle.id).first().cycle_year
        cycle_data = pd.read_sql(School.query.filter_by(cycle_id=cycle.id).statement, db.session.bind)
        

        reg_data = cycle_data[cycle_data['phd'] == False]
        phd_data = cycle_data[cycle_data['phd'] == True]

        reg_info = {'bar_json':public_graphs.public_bar(reg_data.drop(['id','cycle_id','user_id','school_type','phd','note'],axis=1),f"{cycle_year} Cycle"),
        'timeline_json': public_graphs.public_timeline(reg_data.drop(['id','cycle_id','user_id','school_type','phd','note'],axis=1),f"{cycle_year} Cycle")
        }

        phd_info = {'bar_json':public_graphs.public_bar(phd_data.drop(['id','cycle_id','user_id','school_type','phd','note'],axis=1),f"{cycle_year} Cycle"),
        'timeline_json': public_graphs.public_timeline(phd_data.drop(['id','cycle_id','user_id','school_type','phd','note'],axis=1),f"{cycle_year} Cycle")
        }

        return render_template('profile_template.html', user=current_user, user_info=user,phd_info=phd_info,
                            reg_info=reg_info, valid_cycles=VALID_CYCLES)

