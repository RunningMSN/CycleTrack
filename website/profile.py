from flask_login import current_user, login_required
from .form_options import VALID_CYCLES
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, Response, Markup
from . import db, form_options, mail
from .models import User,Cycle, School, School_Profiles_Data, Courses, User_Profiles
from datetime import datetime, date
import pandas as pd
from .helpers import import_list_funcs, categorize_stats, school_stats_calculators, gpa_calculators
from .visualizations import public_graphs
import hashlib

profile = Blueprint('profile', __name__)

@profile.route('/profile', methods=['GET', 'POST'])
@login_required
def profile_home():
    #generates the custom URLs based on the userid and email
    '''user_ids = [x.id for x in User.query.all()]
    for userid in user_ids:
        user = User.query.filter_by(id=userid).first()
        user_email = user.email.split("@")[0]
        url = hashlib.sha1(f"{userid}{user_email}".encode()).hexdigest()
        db.session.add(User_Profiles(url_hash=url,user_id=userid,public_profile=False,block_type=None,cycle_id=None,
        vis_type=None,app_type=None,color=None,anonymize=False,hide_names=False))
        db.session.commit()'''
    userid = current_user.get_id()
    user = User.query.filter_by(id=userid).first()
    user_email = user.email.split("@")[0]
    url = hashlib.sha1(f"{userid}{user_email}".encode()).hexdigest()
    
    profile = User_Profiles.query.filter_by(user_id = userid)

    cycle_ids = current_user.cycles
    cycle_years = [Cycle.query.filter_by(id=x.id).first().cycle_year for x in cycle_ids]
    
    public_private = (request.form.get('public_private')=='Public')

    cycle_data = pd.read_sql(School.query.filter_by(user_id=userid).statement, db.session.bind)

    # Get application types
    # Dual Degree Types
    if any(cycle_data['phd']):
        app_types = ['Dual Degree']
        # If any MD/DO Only
        if not all(cycle_data['phd']):
            for type in cycle_data['school_type'].unique():
                app_types.append(f'{type} Only')
    # MD/DO Only
    else:
        app_types = list(cycle_data['school_type'].unique())
        if 'MD' in app_types and 'DO' in app_types: app_types.insert(0, 'MD or DO')
    print(request.form)
    #add block
    block_order = request.form.get('block_order')
    block_type = request.form.get('block_type')
    if block_type:
        print(block_type)
        if block_type.lower() == "graph":
            selected_cycle_year = request.form.get('cycle_year')
            cycle_id = Cycle.query.filter_by(cycle_year=selected_cycle_year).first().id

            #cycle = Cycle.query.filter_by(id=int(cycle_id)).first()
            cycle_data = pd.read_sql(School.query.filter_by(cycle_id=cycle_id).statement, db.session.bind)
            # Vis Generation
            vis_type = request.form.get('vis_type')

            # Grab Settings
            if request.form.get('plot_title'):
                plot_title = request.form.get('plot_title')
            else:
                plot_title = ""
            app_type = request.form.get("app_type")
            map_type = request.form.get("map_type")
            color_type = request.form.get("color_type")
            filter_values = request.form.get("filter_values")
            hide_names = request.form.get("hide_names")
            db.session.add(
                User_Profiles(user_id = userid,url_hash = url, public_profile = public_private,
                    block_order=block_order,block_type=block_type,
                    vis_type=vis_type,plot_title=plot_title,app_type=app_type,map_type=map_type,
                    color=color_type,filter_values=filter_values,hide_names=hide_names))
            db.session.commit()
        elif block_type.lower() == "textbox":
            text = request.form.get("textbox")
            db.session.add(
                User_Profiles(user_id = userid,url_hash = url, public_profile = public_private,
                    block_order=block_order,block_type=block_type,text=text))

    return render_template('profile.html',user=current_user,profile=profile,app_types=app_types,vis_types=form_options.VIS_TYPES, 
    color_types=form_options.COLOR_TYPES, map_types=form_options.MAP_TYPES,block_types=form_options.BLOCK_TYPES,cycle_years=cycle_years)

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

