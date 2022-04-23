import plotly
import plotly.graph_objects as go
import json
from . import converters
from ..form_options import VALID_CYCLES, CURRENT_CYCLE


def cycle_progress(data):
    # Select relevant columns and drop any empty rows
    data = data[data['cycle_year'] == CURRENT_CYCLE]
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
                               marker_color = converters.palette["default"]["secondary_received"],
                               opacity=0.75))
    fig.add_trace(go.Histogram(x=data.interview_received,
                               name='Interview Received',
                               xbins=dict(size=86400000),
                               autobinx=False,
                               marker_color = converters.palette["default"]["interview_received"],
                               opacity=0.75))
    fig.add_trace(go.Histogram(x=data.acceptance,
                               name='Acceptance Received',
                               xbins=dict(size=86400000),
                               autobinx=False,
                               marker_color = converters.palette["default"]["acceptance"],
                               opacity=0.75))

    # Overlay both histograms
    fig.update_layout(barmode='overlay', bargap=0, margin=dict(l=0, r=0, t=0, b=0), height=200, autosize=True)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def interview_acceptance_histogram(df, column_name):
    # Generate all traces for the past 3 cycles (including current)
    trace_1 = df[df['cycle_year'] == VALID_CYCLES[0]][column_name].dropna()
    trace_2 = df[df['cycle_year'] == VALID_CYCLES[1]][column_name].dropna()
    trace_2 = trace_2.apply(lambda x: x.replace(year=x.year + 1))
    trace_3 = df[df['cycle_year'] == VALID_CYCLES[2]][column_name].dropna()
    trace_3 = trace_3.apply(lambda x: x.replace(year=x.year + 2))

    # If no data return
    if len(trace_1) == 0 and len(trace_2) == 0 and len(trace_3) == 0:
        return None

    fig = go.Figure()
    fig.add_trace(go.Histogram(x=trace_1,
                               name=str(VALID_CYCLES[0]),
                               xbins=dict(size=86400000),
                               autobinx=False,
                               opacity=0.75,
                               hoverinfo='skip'))
    fig.add_trace(go.Histogram(x=trace_2,
                               name=str(VALID_CYCLES[1]),
                               xbins=dict(size=86400000),
                               autobinx=False,
                               opacity=0.75,
                               hoverinfo='skip'))
    fig.add_trace(go.Histogram(x=trace_3,
                               name=VALID_CYCLES[2],
                               xbins=dict(size=86400000),
                               autobinx=False,
                               opacity=0.75,
                               hoverinfo='skip'))

    # Overlay both histograms
    fig.update_layout(barmode='overlay', bargap=0, margin=dict(l=0, r=0, t=0, b=0), height=200, autosize=True)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON