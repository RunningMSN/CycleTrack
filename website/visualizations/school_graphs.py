import pandas as pd
import plotly
import plotly.graph_objects as go
import json
from . import converters
from ..form_options import VALID_CYCLES, CURRENT_CYCLE


def cycle_progress(data, cycle_year):
    # Select relevant columns and drop any empty rows
    data = data[['secondary_received', 'interview_received', 'acceptance','rejection']]
    data = data.dropna(axis=0, how='all')

    min = pd.to_datetime(str(cycle_year-1) + "-05-01")
    max = pd.to_datetime(str(cycle_year) + "-08-31")

    # Make sure data is in range
    for column in data.columns:
        data = data.mask(data[column] < min)
        data = data.mask(data[column] > max)

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
                               opacity=0.75,
                               hovertemplate = "%{x}<br>%{y}<extra></extra>",))
    fig.add_trace(go.Histogram(x=data.rejection,
                               name='Rejection',
                               xbins=dict(size=86400000),
                               autobinx=False,
                               marker_color = converters.palette["default"]["rejection"],
                               opacity=0.75,
                               hovertemplate = "%{x}<br>%{y}<extra></extra>",))
    fig.add_trace(go.Histogram(x=data.interview_received,
                               name='Interview Received',
                               xbins=dict(size=86400000),
                               autobinx=False,
                               marker_color = converters.palette["default"]["interview_received"],
                               opacity=0.75,
                               hovertemplate = "%{x}<br>%{y}<extra></extra>",))
    fig.add_trace(go.Histogram(x=data.acceptance,
                               name='Acceptance Received',
                               xbins=dict(size=86400000),
                               autobinx=False,
                               marker_color = converters.palette["default"]["acceptance"],
                               opacity=0.75,
                               hovertemplate = "%{x}<br>%{y}<extra></extra>",))

    # Overlay both histograms
    fig.update_layout(barmode='overlay', bargap=0, margin=dict(l=0, r=0, t=0, b=0), height=200, autosize=True, legend=dict(y=0.5))
    
    # Find the maximum number of date repeated in each column; current threshold for log scale on any date is 10 actions
    max_count = data.apply(pd.Series.value_counts).max()
    if (max_count > 10).any():
        fig.update_yaxes(type="log")

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def interview_acceptance_histogram(df, column_name):
    # Generate all traces for the past 3 cycles (including current)
    trace_1 = df[df['cycle_year'] == VALID_CYCLES[0]][column_name].dropna()
    trace_2 = df[df['cycle_year'] == VALID_CYCLES[1]][column_name].dropna()
    trace_2 = trace_2.apply(lambda x: x + pd.DateOffset(years=1))
    trace_3 = df[df['cycle_year'] == VALID_CYCLES[2]][column_name].dropna()
    trace_3 = trace_3.apply(lambda x: x + pd.DateOffset(years=2))

    # If no data return
    if len(trace_1) == 0 and len(trace_2) == 0 and len(trace_3) == 0:
        return None

    # Make sure data is in range
    min = pd.to_datetime(str(VALID_CYCLES[0] - 1) + "-05-01")
    max = pd.to_datetime(str(VALID_CYCLES[0]) + "-08-31")

    trace_1 = trace_1[trace_1 >= min]
    trace_1 = trace_1[trace_1 <= max]
    trace_2 = trace_2[trace_2 >= min]
    trace_2 = trace_2[trace_2 <= max]
    trace_3 = trace_3[trace_3 >= min]
    trace_3 = trace_3[trace_3 <= max]

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

    # center legend vertically
    fig.update_layout(legend=dict(y=0.5))

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
