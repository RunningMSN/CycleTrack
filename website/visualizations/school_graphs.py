import plotly
import plotly.graph_objects as go
import json
from ..models import Cycle, School
from . import converters
import pandas as pd


def cycle_progress(data):
    # Select relevant columns and drop any empty rows
    data = data[['secondary_received', 'interview_received', 'acceptance']]
    data = data.dropna(axis=0, how='all')

    # No data to display
    if len(data) == 0:
        return None

    # Build traces
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=data.secondary_received,
                               name='Secondary Received',
                               xbins=dict(size=86400000),
                               autobinx=False,
                               marker_color = converters.fig_colors["secondary_received"],
                               opacity=0.75))
    fig.add_trace(go.Histogram(x=data.interview_received,
                               name='Interview Received',
                               xbins=dict(size=86400000),
                               autobinx=False,
                               marker_color = converters.fig_colors["interview_received"],
                               opacity=0.75))
    fig.add_trace(go.Histogram(x=data.acceptance,
                               name='Acceptance Received',
                               xbins=dict(size=86400000),
                               autobinx=False,
                               marker_color = converters.fig_colors["acceptance"],
                               opacity=0.75))

    # Overlay both histograms
    fig.update_layout(barmode='overlay', bargap=0, margin=dict(l=0, r=0, t=0, b=0), height=200, autosize=True)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
