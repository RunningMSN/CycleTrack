import plotly
import plotly.express as px
import plotly.graph_objects as go
import json
from . import converters

#leaving this for now in case we want to use it in the future
symbol_map = {
    'primary': 'circle', 
    'secondary_received': 'square', 
    'application_complete': 'diamond',
    'interview_received':'cross', 
    'interview_date': 'x', 
    'rejection': 'triangle-up',
    'waitlist': 'pentagon',
    'acceptance': 'hourglass', 
    'withdrawn': 'star'
    }

def generate(cycle_data, title, stats, color="default"):
    melted = cycle_data.melt(id_vars=cycle_data.columns[0], value_vars=cycle_data.columns[1:], var_name='Actions', value_name='date')
    
    actions = melted["Actions"].unique()
    
    fig = go.Figure()
    for action in actions:
        df = melted.loc[melted["Actions"]==action]
        fig.add_trace(go.Scatter(
            x = df["date"],
            y = df["name"],
            mode = "markers",
            name = converters.action_names[action],
            hoverinfo="none",
            marker = dict(
                color=converters.palette[color][action],
                size=10,
                #symbol = symbol_map[action],
                ),
            text = df["name"]+"<br>"+ converters.action_names[action],
            hovertemplate = "%{text}"+"<br>%{x}<extra></extra>",
        ))
    
    est_height = len(melted['name'].unique())*20

    if est_height < 250:
        wanted_height = 250
    else:
        wanted_height = est_height

    fig.update_layout(height=wanted_height,
    title=title,
    yaxis_type="category",
    margin=dict(l=20, r=20, t=40, b=20))
    fig.add_layout_image(
            dict(
            source="./static/images/CycleTrack_Plot_Watermark.png",
            xref="x domain",
            yref="y domain",
            x=1, y=1,
            sizex=0.2, sizey=0.2,
            xanchor="right", yanchor="bottom"))
    if stats:
        fig.add_annotation(
            dict(
            xanchor="left",
            yanchor="bottom",
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.05,
            y=0.25,
            text=f'Demographics<br>MCAT: {stats["mcat"]}<br>cGPA: {stats["cgpa"]}<br>sGPA: {stats["sgpa"]}'
                 f'<br>State: {stats["state"]}',
            align="left"
            )
        )

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON