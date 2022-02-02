import plotly
import plotly.graph_objects as go
import json
from . import converters

def generate(cycle_data):
    '''Returns JSON for plotly line graph of the application cycle.'''
    # Get number of actions on each day
    cleaned_data = converters.convert_sums(cycle_data)
    fig = go.Figure()
    for column in cleaned_data.columns:
        # Removes any columns that never had any actions
        if not (cleaned_data[column] == 0).all():
            # Add trace for action
            fig.add_trace(go.Scatter(x=cleaned_data.index, y=cleaned_data[column], mode='lines',name=column))
    # Convert to JSON and return it for plotting
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON