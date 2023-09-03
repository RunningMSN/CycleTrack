import pandas as pd
from .. import db, form_options
from ..helpers import gpa_calculators
import plotly.graph_objects as go
import plotly
import json

def generate(courses):
    '''Returns a plot of GPA over time using the supplied courses.'''
    # Convert to dataframe
    df = pd.read_sql(courses.statement, db.get_engine())
    # Store GPA data
    gpa_data = {'xlab': [], 'year': [], 'term': [], 'amcas_gpa': [], 'aacomas_gpa': [], 'tmdsas_gpa': []}
    # Grab unique years
    years = df['year'].unique()

    # Iterate through years
    for year in years:
        year_courses = df[df['year'] == year]
        # Grab unique terms
        terms = year_courses['term'].unique()

        # Get GPA for each term
        for term in terms:
            term_courses = courses.filter_by(year=year, term=int(term)).all()
            gpa_data['xlab'].append(form_options.COURSE_TERMS[term]+", "+year)
            gpa_data['year'].append(year)
            gpa_data['term'].append(term)
            gpa_data['amcas_gpa'].append(float(gpa_calculators.amcas_gpa(term_courses, 'cumulative')))
            gpa_data['aacomas_gpa'].append(float(gpa_calculators.aacomas_gpa(term_courses, 'cumulative')))
            gpa_data['tmdsas_gpa'].append(float(gpa_calculators.tmdsas_gpa(term_courses, 'cumulative')))

    # Convert to dataframe
    gpa_df = pd.DataFrame(gpa_data)

    # Generate plot
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=gpa_df['xlab'], y=gpa_df['tmdsas_gpa'],
                             mode='lines+markers', name='TMDSAS', opacity=0.9))
    fig.add_trace(go.Scatter(x=gpa_df['xlab'], y=gpa_df['aacomas_gpa'],
                             mode='lines+markers', name='AACOMAS', opacity=0.9))
    fig.add_trace(go.Scatter(x=gpa_df['xlab'], y=gpa_df['amcas_gpa'],
                             mode='lines+markers', name='AMCAS', opacity=0.9))

    fig.update_xaxes(type='category')
    fig.update_yaxes(range=[0, 4.5], fixedrange=True)
    fig.update_layout(
        title='Cumulative GPA Over Time'
    )
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON