import plotly
import plotly.graph_objects as go
import json
import textwrap
from . import converters

def generate(cycle_data, title, stats, color="default",custom_text=None):
    '''Returns JSON for plotly line graph of the application cycle.'''
    cleaned_data = converters.convert_sums(cycle_data)
    fig = go.Figure()
    for column in cleaned_data.columns:
        # Removes any columns that never had any actions
        if not (cleaned_data[column] == 0).all():
            # Add trace for action
            fig.add_trace(go.Scatter(x=cleaned_data.index,
                                     y=cleaned_data[column],
                                     mode='lines',
                                     name=converters.action_names[column],
                                     marker=dict(color=converters.palette[color][column])))
    fig.update_layout(
        title=title,
        yaxis_title="Count",
        legend_title="Actions",
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
    # Convert to JSON and return it for plotting
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON