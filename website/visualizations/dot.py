import plotly
import plotly.express as px
import json

def generate(data):
    '''Returns JSON for plotly dot graph of the application cycle.'''
    melted = data.melt(id_vars=data.columns[0], value_vars=data.columns[1:], var_name='Actions', value_name='date')
    fig = px.scatter(melted, x='date', y='name', color='Actions',
                     labels={
                         'date': 'Date',
                         'name':''
                     },
                     title="Application Cycle")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON