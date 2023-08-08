import numpy as np
import pandas as pd
import plotly
import plotly.graph_objects as go
import plotly.express as px
import json
from . import converters
from ..form_options import VALID_CYCLES, CURRENT_CYCLE

def convert_summary_bar_data(data,year):
    year = int(year)

    # Remove potentially future interview dates if withdrawn
    if "withdrawn" in data.columns.tolist():
        data["interview_date"] = data.apply(
            lambda row: row["interview_date"] if row["interview_date"] <= row["withdrawn"] else np.nan, axis=1)
        
    data = data[['primary','secondary_received', 'application_complete', 'interview_received',
       'interview_date', 'rejection', 'waitlist', 'acceptance']]
    
    # Change dates outside of daterange to null
    start_date = pd.to_datetime(str(year-1) + "-05-01")
    end_date = pd.to_datetime(str(year) + "-08-31")

    for col in data.columns:
        data.loc[(data[col] < start_date) | (data[col] > end_date), col] = pd.NaT

    # Obtain a range of all dates
    melted = data.melt(id_vars=data.columns[0], value_vars=data.columns[1:], var_name='actions', value_name='date').dropna()
    start_dates = min(melted['date'])
    end_dates = max(melted['date'])
    all_dates = pd.date_range(start=start_dates, end=end_dates)

    #names already removed
    names_removed = data

    # Generate initial dataframe to add to
    output = pd.DataFrame()
    output['Best Outcome'] = names_removed[names_removed <= all_dates[0]].dropna(axis=0, how='all').idxmax(axis=1)
    output['Date'] = all_dates[0]
    # Continue adding for all dates
    for date in all_dates[1:]:
        data = pd.DataFrame()
        data['Best Outcome'] = names_removed[names_removed <= date].dropna(axis=0, how='all').idxmax(axis=1)
        data['Date'] = date
        output = pd.concat([output,data])

    # Get counts for all dates
    output = output.groupby(['Date', 'Best Outcome']).size().reset_index(name='Count')
    output.to_csv(f'{year}.csv')
    return output

def generate_bar(cycle_data, title, year,color="default"):
    # Generate dataframe for plotly
    cycle_data = convert_summary_bar_data(cycle_data,year=year)
    fig = px.bar(cycle_data,
                 x='Date',
                 y='Count',
                 title=title,
                 color='Best Outcome',
                 color_discrete_map=converters.palette[color])
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

    fig.add_layout_image(
        dict(
        source="./static/images/CycleTrack_Plot_Watermark.png",
        xref="x domain",
        yref="y domain",
        x=1, y=1,
        sizex=0.15, sizey=0.15,
        xanchor="right", yanchor="bottom")
    )

    # Convert to JSON for plotting
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


#what is the distribution of time between secondary completion and interview invitation? INCOMPLETE
def generate_sec_to_ii(data):
    data = data[['application_complete', 'interview_received']]
    data['application_complete'] = pd.to_datetime(data['application_complete'])
    data['interview_received'] = pd.to_datetime(data['interview_received'])

    data = data.dropna(axis=0)
    print(data)

    differences = (data['interview_received']- data['application_complete']).dropna().dt.days.tolist()
    print(differences)

    fig = go.Figure()
    fig.add_trace(go.Histogram(x=differences,
                               opacity=0.75,
                               hovertemplate = "%{x} days"+"<br>%{y}<extra></extra>",))
    

    
    fig.update_layout(
        title="Time between Secondary Completion and Interview Invitation",
        yaxis_title="Application Count",
        xaxis_title="Days",
        margin=dict(l=20, r=20, t=40, b=20)
    )
    fig.add_layout_image(
        dict(
        source="./static/images/CycleTrack_Plot_Watermark.png",
        xref="x domain",
        yref="y domain",
        x=1, y=1,
        sizex=0.15, sizey=0.15,
        xanchor="right", yanchor="bottom")
    )


    # Convert to JSON for plotting
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON