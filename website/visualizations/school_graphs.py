import pandas as pd
import plotly
import plotly.graph_objects as go
import json
from . import converters
from ..form_options import VALID_CYCLES, CURRENT_CYCLE, STATE_ABBREV


def cycle_progress(data, cycle_year):
    # Select relevant columns and drop any empty rows
    data = data[['secondary_received', 'interview_received', 'acceptance','rejection','waitlist']]
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
                               name='Secondary',
                               xbins=dict(size=86400000),
                               autobinx=False,
                               marker_color = converters.palette["default"]["secondary_received"],
                               opacity=0.75,
                               hovertemplate = "%{x}<br>%{y}<extra></extra>",))
    fig.add_trace(go.Histogram(x=data.interview_received,
                               name='Interview',
                               xbins=dict(size=86400000),
                               autobinx=False,
                               marker_color = converters.palette["default"]["interview_received"],
                               opacity=0.75,
                               hovertemplate = "%{x}<br>%{y}<extra></extra>",))
    fig.add_trace(go.Histogram(x=data.rejection,
                               name='Rejection',
                               xbins=dict(size=86400000),
                               autobinx=False,
                               marker_color = converters.palette["default"]["rejection"],
                               opacity=0.75,
                               hovertemplate = "%{x}<br>%{y}<extra></extra>",))
    fig.add_trace(go.Histogram(x=data.waitlist,
                               name='Waitlist',
                               xbins=dict(size=86400000),
                               autobinx=False,
                               marker_color = converters.palette["default"]["waitlist"],
                               opacity=0.75,
                               hovertemplate = "%{x}<br>%{y}<extra></extra>",))
    fig.add_trace(go.Histogram(x=data.acceptance,
                               name='Acceptance',
                               xbins=dict(size=86400000),
                               autobinx=False,
                               marker_color = converters.palette["default"]["acceptance"],
                               opacity=0.75,
                               hovertemplate = "%{x}<br>%{y}<extra></extra>",))

    # Overlay both histograms
    fig.update_layout(barmode='overlay',
                      bargap=0,
                      margin=dict(l=0, r=0, t=0, b=0),
                      height=300,
                      autosize=True,
                      legend=dict(orientation="h", yanchor="bottom", y=1.02),
                      xaxis=dict(tickformat='%b %d'))
    
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
    fig.update_layout(barmode='overlay',
                      bargap=0,
                      margin=dict(l=0, r=0, t=0, b=0),
                      height=300,
                      autosize=True,
                      legend=dict(orientation="v", y=0.5),
                      xaxis=dict(tickformat='%b'))


    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def states_applied(df):
    counts = df['home_state'].value_counts().reset_index()
    if len(counts) == 0:
        return None
    else:
        counts.columns = ['home_state', 'count']
        # Don't show if <5 users
        if counts['count'].sum() < 5:
            return None
        else:
            counts['abbrev'] = counts['home_state'].map(STATE_ABBREV)
            total_count = counts['count'].sum()
            counts['percent'] = (counts['count'] / total_count) * 100
            counts['label'] = counts['percent'].apply(lambda x: f"{x:.1f}%")

            fig = go.Figure(data=go.Choropleth(
                locations=counts['abbrev'],
                z=counts['percent'].astype(float),
                locationmode='USA-states',
                colorscale='blues',
                colorbar=None,
                showscale=False,
                hoverinfo="text",
                text=counts['abbrev'] + ": " + counts['label']
            ))

            fig.update_layout(
                geo_scope='usa',
                margin=dict(l=0, r=0, t=0, b=0),
                height = 300
            )

            graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            return graphJSON

def mcat_vs_gpa(df):
    df = df[['cgpa', 'mcat_total', 'interview_received', 'acceptance']].dropna(subset=['cgpa', 'mcat_total'])

    if len(df) < 5:
        return None
    else:
        fig = go.Figure()
        # Add points where neither interview nor acceptance
        fig.add_trace(go.Scatter(
            x=df[(df['interview_received'].isnull()) & (df['acceptance'].isnull())]['cgpa'],
            y=df[(df['interview_received'].isnull()) & (df['acceptance'].isnull())]['mcat_total'],
            mode='markers',
            name='Applied',
            marker=dict(color='gray')
        ))

        # Add points where interview received
        fig.add_trace(go.Scatter(
            x=df[df['interview_received'].notna()]['cgpa'],
            y=df[df['interview_received'].notna()]['mcat_total'],
            mode='markers',
            name='Interview Received',
            marker=dict(color=converters.palette["default"]["interview_received"])
        ))

        # Add points where acceptance
        fig.add_trace(go.Scatter(
            x=df[df['acceptance'].notna()]['cgpa'],
            y=df[df['acceptance'].notna()]['mcat_total'],
            mode='markers',
            name='Accepted',
            marker=dict(color=converters.palette["default"]["acceptance"])
        ))

        # Update layout
        fig.update_layout(
            xaxis_title='cGPA',
            yaxis_title='MCAT',
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
            hovermode='closest',
            autosize=True,
            margin=dict(l=0, r=0, t=0, b=0),
            height=300
        )

        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON