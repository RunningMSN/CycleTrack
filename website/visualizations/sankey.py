import plotly
import json
from . import converters

def generate(cycle_data, title):
    '''Returns JSON for plotly line graph of the application cycle.'''
    # Drop names and interview days
    cycle_data = cycle_data.drop('name', axis=1)
    if 'interview_date' in cycle_data.columns:
        cycle_data = cycle_data.drop('interview_date', axis=1)

    df_nodes, df_links = converters.sankey_build_frames(cycle_data)

    # Sankey plot setup
    data_trace = dict(
        type='sankey',
        domain=dict(
            x=[0, 1],
            y=[0, 1]
        ),
        node=dict(
            line=dict(
                width=0
            ),
            label=df_nodes['label'],
            color=df_nodes['color']
        ),
        link=dict(
            source=df_links['Source'],
            target=df_links['Target'],
            value=df_links['size'],
            color=df_links['Link Color'],
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

    # Convert to JSON and return it for plotting
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON