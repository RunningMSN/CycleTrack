import plotly
import plotly.graph_objects as go
import json
from . import converters

def generate(cycle_data, title):
    '''Returns JSON for plotly line graph of the application cycle.'''
    cleaned_data = converters.convert_sums(cycle_data)
    fig = go.Figure()
    for column in cleaned_data.columns:
        # Removes any columns that never had any actions
        if not (cleaned_data[column] == 0).all():
            # Add trace for action
            fig.add_trace(go.Scatter(x=cleaned_data.index,
                                     y=cleaned_data[column],
                                     mode='lines',
                                     name=converters.action_names[column],
                                     marker=dict(color=converters.fig_colors[column])))
    fig.update_layout(
        title=title,
        yaxis_title="Count",
        legend_title="Actions",
        margin=dict(l=20, r=20, t=40, b=20)
    )
    # Convert to JSON and return it for plotting
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON