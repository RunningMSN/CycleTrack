import plotly
import plotly.express as px
import json
from . import converters

def generate(cycle_data, title, stats, color="default"):
    # Generate dataframe for plotly
    cycle_data = converters.convert_bar_df(cycle_data)
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

    # Convert to JSON for plotting
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON