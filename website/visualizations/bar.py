import plotly
import plotly.express as px
import json
from . import converters

def generate(cycle_data):
    # Generate dataframe for plotly
    cycle_data = converters.convert_bar_df(cycle_data)
    fig = px.bar(cycle_data,
                 x='Date',
                 y='Count',
                 title='Application Cycle',
                 color='Best Outcome',
                 color_discrete_map=converters.fig_colors)
    # Remove outlines
    fig.update_traces(marker=dict(line=dict(width=0)))
    # Label using more readable action names
    fig.for_each_trace(lambda t: t.update(name=converters.action_names[t.name],
                                          legendgroup=converters.action_names[t.name],
                                          hovertemplate=t.hovertemplate.replace(t.name, converters.action_names[t.name])
                                          )
                       )
    # Remove gaps between bars
    fig.update_layout(bargap=0, margin=dict(l=20, r=20, t=40, b=20))
    # Convert to JSON for plotting
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON