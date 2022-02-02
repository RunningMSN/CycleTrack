import plotly
import plotly.express as px
import json

def generate(cycle_data):
    '''Returns JSON for plotly dot graph of the application cycle.'''
    melted = cycle_data.melt(id_vars=cycle_data.columns[0], value_vars=cycle_data.columns[1:], var_name='Actions', value_name='date')
    fig = px.scatter(melted, x='date', y='name', color='Actions',
                     labels={
                         'date': 'Date',
                         'name':''
                     },
                     title="Application Cycle")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON