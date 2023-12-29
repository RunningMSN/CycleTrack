import pandas as pd
import plotly
import json
from . import converters
import textwrap
import plotly.graph_objects as go
import datetime

def generate(cycle_data, title, stats, color="default",no_action=False,custom_text=None):
    '''Returns JSON for plotly Sankey graph of the application cycle.'''
    # Drop names and interview days
    cycle_data = cycle_data.drop('name', axis=1)
    if 'interview_date' in cycle_data.columns:
        cycle_data = cycle_data.drop('interview_date', axis=1)

    # if there is only 1 value per row, make the no_action column today's date. Otherwise, set it to none
    if no_action:
        cycle_data['no_action'] = cycle_data.apply(lambda row: datetime.date.today() if row.count() == 1 else pd.NaT, axis=1)
        

    df_nodes, df_links, sankeymatic = converters.sankey_build_frames(cycle_data,color,no_action)

    # Sankey plot setup
    data_trace = dict(
        type='sankey',
        arrangement = 'freeform',
        domain=dict(
            x=[0, 1],
            y=[0, 1]
        ),
        node=dict(
            line=dict(
                width=0
            ),
            label=df_nodes['label'],
            color=df_nodes['color'],
            pad = 30,
            
            hovertemplate='%{label} <extra></extra> '
        ),
        link=dict(
            source=df_links['Source'],
            label=df_links['Source'],
            target=df_links['Target'],
            value=df_links['size'],
            color=df_links['Link Color'],
            hoverinfo="none",
        )
    )

    layout = dict(title=title,
                  images=[dict(
                      source="./static/images/CycleTrack_Plot_Watermark.png",
                      xref="x domain",
                      yref="y domain",
                      x=1, y=1.15,
                      sizex=0.15, sizey=0.15,
                      xanchor="right", yanchor="bottom")])

    fig = dict(data=[data_trace], layout=layout)

    fig = go.Figure(fig)


    if custom_text:
        wrapped_text = textwrap.fill(custom_text,55).replace('\n', '<br />')

    if stats and custom_text:
        fig.add_annotation(
            dict(
            xanchor="center",
            yanchor="top",
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.5,
            y=0,
            text=f'Demographics<br>MCAT: {stats["mcat"]} | cGPA: {stats["cgpa"]} | sGPA: {stats["sgpa"]} | '
                 f'State: {stats["state"]}<br>{wrapped_text}',
            align="center"
            )
        )
    else:
        if stats:
            fig.add_annotation(
            dict(
            xanchor="center",
            yanchor="bottom",
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.5,
            y=-0.1,
            text=f'Demographics<br>MCAT: {stats["mcat"]} | cGPA: {stats["cgpa"]} | sGPA: {stats["sgpa"]} | '
                 f'State: {stats["state"]}',
            align="center"
            )
        )
        if custom_text:
            fig.add_annotation(
                dict(
                xanchor="center",
                yanchor="bottom",
                showarrow=False,
                xref='paper',
                yref='paper',
                x=0.5,
                y=-0.1,
                text=f'{wrapped_text}',
                align="left"
                )
            )


    # Convert to JSON and return it for plotting
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON, sankeymatic