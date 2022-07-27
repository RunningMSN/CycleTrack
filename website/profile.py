from flask_login import current_user, login_required
from numpy import number
from .form_options import VALID_CYCLES
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, Response, Markup
from . import db, form_options
from .models import User,Cycle, School, User_Profiles
import pandas as pd
from .visualizations import dot, line, bar, sankey, map, horz_bar
import json
import uuid
import markdown
from markdown.extensions import Extension

class EscapeHtml(Extension):
    def extendMarkdown(self, md, md_globals):
        del md.preprocessors['html_block']
        del md.inlinePatterns['html']

profile = Blueprint('profile', __name__)

@profile.route('/profile', methods=['GET', 'POST'])
@login_required
def profile_home():
    userid = current_user.get_id()
    user = User.query.filter_by(id=userid).first()
    
    
    user_profile = db.session.query(User_Profiles,User).filter(User_Profiles.user_id==userid) \
        .join(User, User.id == User_Profiles.user_id)

    if user_profile.first():
        url = user_profile.first()[0].url_hash
    else:
        url = str(uuid.uuid5(uuid.NAMESPACE_URL, userid))

    cycle_ids = current_user.cycles
    cycle_years = [Cycle.query.filter_by(id=x.id).first().cycle_year for x in cycle_ids]

    cycle_data = pd.read_sql(School.query.filter_by(user_id=userid).statement, db.session.bind)

    # Handle editing publish settings
    if request.form.get('profile_publish_setting'):
        if request.form.get('profile_publish_setting') == '1':
            current_user.public_profile = True
        else:
            current_user.public_profile = False
        db.session.commit()

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

    #edit blocks
    block_id = request.form.get("edit_block")
    if block_id:
        block = User_Profiles.query.get(block_id)
        block_order = request.form.get('block_order')
        block.block_order = block_order
        block_type = request.form.get('block_type')
        
        if block_type.lower() == "graph":
            selected_cycle_year = request.form.get('cycle_year')
            if selected_cycle_year:
                block.cycle_year = selected_cycle_year
                block.cycle_id = Cycle.query.filter_by(user_id=userid).first().id
            else:
                block.cycle_year = None
                block.cycle_id = None
            vis_type = request.form.get('vis_type')
            if vis_type:
                block.vis_type = vis_type
            plot_title = request.form.get('plot_title')
            block.plot_title = plot_title
            app_type = request.form.get("app_type")
            if app_type:
                block.app_type = app_type
            map_type = request.form.get("map_type")
            if map_type:
                block.map_type = map_type
            color_type = request.form.get("color_type")
            if color_type:
                block.color = color_type
            filter_values = ", ".join(request.form.getlist("filter_values"))
            block.filter_values = filter_values
            hide_names = request.form.get("hide_names")
            block.hide_names = (hide_names == 'true')
        elif block_type.lower() == "text":
            text = request.form.get("textbox")
            block.text = text
        db.session.commit()

    elif request.form.get("add_block"):
        #add block
        block_order = request.form.get('block_order')
        block_type = request.form.get('block_type')
        if block_type:
            if block_type.lower() == "graph":
                if User_Profiles.query.filter_by(user_id=userid, block_type="Graph").count() >= 6:
                    flash("You have reached the limit on the number of graphs that can be on your profile", category='error')
                else:
                    selected_cycle_year = request.form.get('cycle_year')
                    cycle_id = Cycle.query.filter_by(user_id=userid).first().id
                    #cycle_data = pd.read_sql(School.query.filter_by(cycle_id=cycle_id).statement, db.session.bind)
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
                    filter_values = ", ".join(request.form.getlist("filter_values"))
                    hide_names = (request.form.get("hide_names") == 'true')
                    db.session.add(
                        User_Profiles(user_id = userid,url_hash = url,
                            block_order=block_order,block_type=block_type,cycle_id=cycle_id,cycle_year=selected_cycle_year,
                            vis_type=vis_type,plot_title=plot_title,app_type=app_type,map_type=map_type,
                            color=color_type,filter_values=filter_values,hide_names=hide_names))
                    db.session.commit()
            elif block_type.lower() == "text":
                if User_Profiles.query.filter_by(user_id=userid, block_type="Text").count() >= 10:
                    flash("You have reached the limit on the number of text blocks that can be on your profile.", category='error')
                else:
                    text = request.form.get("textbox")
                    db.session.add(
                        User_Profiles(user_id = userid,url_hash = url,
                            block_order=block_order,block_type=block_type,text=text))
                    db.session.commit()
    elif request.form.get("delete_block"):
        #reindex the profile
        profile = User_Profiles.query.filter_by(user_id=userid).order_by(User_Profiles.block_order)
        for x,row in enumerate(profile):
            row.block_order = x+1
        db.session.commit()

    blocks = [x[0] for x in user_profile.order_by(User_Profiles.block_order.asc())]

    return render_template('profile.html',user=current_user,profile=user_profile,blocks=blocks,app_types=app_types,
                           hashurl=url, vis_types=form_options.VIS_TYPES,
                           color_types=form_options.COLOR_TYPES, profile_types=form_options.PROFILE_TYPES,
                           filter_options=form_options.FILTER_OPTIONS,
                           map_types=form_options.MAP_TYPES, block_types=form_options.BLOCK_TYPES,
                           cycle_years=cycle_years, markdown=markdown.markdown, EscapeHtml=EscapeHtml,
                           number_of_graph_blocks=User_Profiles.query.filter_by(user_id=userid, block_type="Graph").count(),
                           number_of_text_blocks=User_Profiles.query.filter_by(user_id=userid, block_type="Text").count())

@profile.route('/profile/<userurl>')
def profile_page(userurl):
    user = User_Profiles.query.filter_by(url_hash=userurl).first()
    if user:
        userid = user.user_id

        user_profile = db.session.query(User_Profiles, User).filter(User_Profiles.user_id == userid) \
            .join(User, User.id == User_Profiles.user_id)

        blocks = [x[0] for x in user_profile.order_by(User_Profiles.block_order.asc())]
        types = []
        graphs = []
        ids = []
        for block in blocks:
            ids.append(block.block_order)
            # block type
            block_type = block.block_type
            if block_type == "Graph":
                types.append("graph")
                graphJSON = None
                # cycle data
                cycle_id = block.cycle_id
                cycle_data = pd.read_sql(School.query.filter_by(cycle_id=cycle_id).statement, db.session.bind)
                # app type
                app_type = block.app_type
                # vis type
                vis_type = block.vis_type
                # plot title
                plot_title = block.plot_title

                map_type = block.map_type

                color_type = block.color

                hide_names = block.hide_names

                if block.filter_values:
                    filter_list = block.filter_values.split(", ")
                    filter_replacement = {"Primary Submitted": "primary", "Secondary Recieved": "secondary_received",
                                          "Application Complete": "application_complete",
                                          "Interview Recieved": "interview_received",
                                          "Interview Complete": "interview_date",
                                          "Rejection": "rejection", "Waitlist": "waitlist", "Acceptance": "acceptance",
                                          "Withdrawn": "withdrawn"}
                    replaced_filters = [x if x not in filter_replacement else filter_replacement[x] for x in
                                        filter_list]
                    for x in replaced_filters:
                        cycle_data = cycle_data.drop([x],axis=1)

                # Filter by PhD
                if app_type == 'Dual Degree':
                    cycle_data = cycle_data[cycle_data['phd'] == True]
                else:
                    cycle_data = cycle_data[cycle_data['phd'] == False]

                # Filter MD or DO
                if app_type == 'MD' or app_type == 'MD Only':
                    cycle_data = cycle_data[cycle_data['school_type'] == 'MD']
                elif app_type == 'DO' or app_type == 'DO Only':
                    cycle_data = cycle_data[cycle_data['school_type'] == 'DO']
                # Drop extra information
                cycle_data = cycle_data.drop(['id', 'cycle_id', 'user_id', 'school_type', 'phd', 'note'], axis=1)
                # Drop empty columns
                cycle_data = cycle_data.dropna(axis=1, how='all')

                if len(cycle_data.columns) > 1:
                    if vis_type.lower() == 'dot':
                        graphJSON = dot.generate(cycle_data, plot_title, stats=False, color=color_type.lower(),
                                                 hide_school_names=hide_names)
                    elif vis_type.lower() == 'line':
                        graphJSON = line.generate(cycle_data, plot_title, stats=False, color=color_type.lower())
                    elif vis_type.lower() == 'bar':
                        graphJSON = bar.generate(cycle_data, plot_title, stats=False, color=color_type.lower())
                    elif vis_type.lower() == 'sankey':
                        graphJSON = sankey.generate(cycle_data, plot_title, stats=False, color=color_type.lower())
                    elif vis_type.lower() == 'map':
                        graphJSON = map.generate(cycle_data, plot_title, stats=False, color=color_type.lower(),
                                                 map_scope=map_type.lower())
                    elif vis_type.lower() == 'timeline':
                        graphJSON = horz_bar.generate(cycle_data, plot_title, stats=False, color=color_type.lower(),
                                                      hide_school_names=hide_names)
                    graphs.append(graphJSON)
                else:
                    graphJSON = None
            elif block_type == "Text":
                types.append("text")
                converted_markdown = markdown.markdown(block.text, extensions=[EscapeHtml()])
                graphs.append(converted_markdown)
        return render_template('profile_template.html', user=current_user, public_setting=user.public_profile,
                               profile_user_id = user.user_id, blocks_data=zip(ids,types,graphs))
    else:
        return render_template('profile_template.html', user=current_user, public_setting=False,
                               profile_user_id=-1)

@profile.route('/delete-block',methods=["POST"])
def delete_block():
    block = json.loads(request.data)
    block_id = block['blockId']
    block = User_Profiles.query.get(block_id)
    if block:
        if block.user_id == current_user.id:
            db.session.delete(block)
            db.session.commit()
    return jsonify({})

@profile.route('/reorder-block',methods=["POST"])
def reorder_block():
    block = json.loads(request.data)
    block_id = block['blockId']
    direction = block['direction']

    this_block = User_Profiles.query.filter_by(id=block_id).first()
    total_blocks = User_Profiles.query.filter_by(user_id=current_user.id).count()

    # Check to make sure operation is in bounds, if it is, perform swap
    if direction == 'up':
        if not this_block.block_order == 1:
            other_block = User_Profiles.query.filter_by(user_id=current_user.id,
                                                        block_order = this_block.block_order - 1).first()
            this_block.block_order = this_block.block_order - 1
            other_block.block_order = other_block.block_order + 1
    elif direction == 'down':
        if not this_block.block_order == total_blocks:
            other_block = User_Profiles.query.filter_by(user_id=current_user.id,
                                                        block_order=this_block.block_order + 1).first()
            this_block.block_order = this_block.block_order + 1
            other_block.block_order = other_block.block_order - 1
    db.session.commit()
    return jsonify({})
                
