import plotly
import plotly.graph_objects as go
import json
from ..models import School_Profiles_Data, School_Stats
from .. import db
from flask import url_for
import pandas as pd

def generate(app):
    '''Generates aggregate map of all schools currently in CycleTrack.'''
    school_info = pd.read_sql(School_Profiles_Data.query.statement, db.get_engine())
    school_stats = pd.read_sql(School_Stats.query.statement, db.get_engine())
    school_info = school_info.set_index('school_id')
    school_stats = school_stats.set_index('school_id')
    data = school_info.join(school_stats, on='school_id', lsuffix='', rsuffix='_stats', how='inner')

    # Restrict to USA
    data = data[data['country'] == 'USA']

    # Get app counts
    data['apps_count'] = data['reg_apps_count'] + data['phd_apps_count']
    # Only include schools with apps
    data = data[data['apps_count'] > 0]

    # Generate links for URLS
    with app.test_request_context():
        data['url'] = url_for('explorer.explorer_home', school=data['school'], _external=True)

    #data['url'] = url_for('explorer.explorer_home')+'/'+data['school']

    # Generate marker colors
    data['color'] = data.apply(lambda row: marker_color(row), axis=1)

    # Data for marker size
    min_apps = min(data['apps_count'])
    max_apps = max(data['apps_count'])
    MAX_SIZE = 20
    MIN_SIZE = 7

    fig = go.Figure(data=go.Scattergeo(
        lon = data['long'],
        lat = data['lat'],
        mode = 'markers',
        marker=dict(
            size=(marker_size(data['apps_count'], max_apps, min_apps, MAX_SIZE, MIN_SIZE)),
            color=data['color'],
            line=dict(width=0),
            opacity=0.7
        ),
        hoverinfo = "text",
        text = data['intermediate_name'] + '<br>Applications: ' + (data['apps_count']).astype(str),
        customdata = data['url']
    ))

    fig.update_layout(
        geo_scope='usa',
        height=500,
        margin = dict(l=0,r=0,t=0,b=10),
        clickmode="event"
    )

    fig.update_geos(resolution=110)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def marker_size(app_count,max_apps,min_apps,max_size,min_size):
    '''Calculates marker size depending on number of applications.'''
    return ((app_count - min_apps) / (max_apps - min_apps)) * (max_size - min_size) + min_size

def marker_color(row):
    '''Returns marker colors for MD or DO schools.'''
    if row['md_or_do'] == 'MD':
        return '#1900ff'
    else:
        return '#ff5500'