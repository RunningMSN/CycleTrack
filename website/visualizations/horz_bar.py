import plotly
import plotly.express as px
import plotly.graph_objects as go
import json
import textwrap
from . import converters

def generate(cycle_data, title, stats, color="default",custom_text=None):
    df = converters.convert_horz_bar(cycle_data)

    fig = px.timeline(df, 
    x_start="start",
    x_end="stop",
    y="name",
    color="Outcome",
    custom_data=["label2"],
    color_discrete_map=converters.palette[color])

    est_height = len(df['name'].unique()) * 17

    if est_height < 250:
        wanted_height = 250
    else:
        wanted_height = est_height

    fig.update_layout(
        height=wanted_height,
        title=title,
        yaxis_type="category",
        margin=dict(l=20, r=20, t=40, b=20))
    
    # Label using more readable action names
    fig.for_each_trace(lambda t: t.update(name=converters.action_names[t.name],
                                          legendgroup=converters.action_names[t.name],
                                          hovertemplate=t.hovertemplate.replace(t.name, converters.action_names[t.name])
                                          )
                       )

    # Remove outlines
    fig.update_traces(marker=dict(line=dict(width=0)),legendgroup='group',
    hovertemplate="%{y}<br>%{customdata[0]}<br>Date: %{base|%m-%d-%Y} <extra></extra>")

    fig.update_yaxes(title=None, gridwidth=1)

    fig.add_layout_image(
            dict(
            source="./static/images/CycleTrack_Plot_Watermark.png",
            xref="x domain",
            yref="y domain",
            x=1, y=1,
            sizex=0.2, sizey=0.2,
            xanchor="right", yanchor="bottom"))
    if custom_text:
        wrapped_text = textwrap.fill(custom_text,30).replace('\n', '<br />')

    if stats and custom_text:
        fig.add_annotation(
            dict(
            xanchor="left",
            yanchor="bottom",
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.02,
            y=0,
            text=f'Demographics<br>MCAT: {stats["mcat"]}<br>cGPA: {stats["cgpa"]}<br>sGPA: {stats["sgpa"]}'
                 f'<br>State: {stats["state"]}<br><br>{wrapped_text}',
            align="left"
            )
        )
    else:
        if stats:
            fig.add_annotation(
            dict(
            xanchor="left",
            yanchor="bottom",
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.02,
            y=0.2,
            text=f'Demographics<br>MCAT: {stats["mcat"]}<br>cGPA: {stats["cgpa"]}<br>sGPA: {stats["sgpa"]}'
                 f'<br>State: {stats["state"]}',
            align="left"
            )
        )
        if custom_text:
            fig.add_annotation(
                dict(
                xanchor="left",
                yanchor="bottom",
                showarrow=False,
                xref='paper',
                yref='paper',
                x=1.02,
                y=0.2,
                text=f'{wrapped_text}',
                align="left"
                )
            )

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON