import plotly
import plotly.express as px
import json
from . import converters

def generate(cycle_data):
    cycle_data = converters.convert_bar_df(cycle_data)
    fig = px.bar(cycle_data, x='Date', y='Count', color='Best Outcome')
    fig.update_traces(marker=dict(line=dict(width=0)))
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON